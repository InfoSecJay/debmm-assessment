const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// ── Read JSON data (extracted from Excel via Python) ──
const jsonPath = process.argv[2];
const outPath = process.argv[3] || "debmm-report.pptx";

if (!jsonPath) {
  console.error("Usage: node scorer/generate_report.js <data.json> [output.pptx]");
  process.exit(1);
}

const data = JSON.parse(fs.readFileSync(jsonPath, "utf-8"));

const org = data.org;
const assessor = data.assessor;
const assessDate = data.date || new Date().toISOString().split("T")[0];
const overallScore = data.overallScore;
const achievedTier = data.achievedTier;
const completion = data.completion;
const tiers = data.tiers;
const criteria = data.criteria;

const debmmCore = criteria.filter((c) => c.section === "DEBMM Core");
const enrichment = criteria.filter((c) => c.section === "Enrichment");
const passing = criteria.filter((c) => c.status.includes("Pass")).length;
const failing = criteria.filter((c) => c.status.includes("Below")).length;

// ── Colors ──
const C = {
  bgDark: "0B1120",
  bgCard: "111A2E",
  bgCardAlt: "162038",
  border: "1E2D4A",
  textPrimary: "E2E8F0",
  textSecondary: "8B9DC3",
  textMuted: "5A6F94",
  green: "10B981",
  blue: "3B82F6",
  yellow: "F59E0B",
  orange: "F97316",
  cyan: "06B6D4",
  purple: "8B5CF6",
  red: "EF4444",
  white: "FFFFFF",
};

const tierColors = {
  T0: C.green,
  T1: C.blue,
  T2: C.yellow,
  T3: C.orange,
  T4: C.purple,
};

const levelColors = {
  Optimized: C.green,
  Managed: C.blue,
  Defined: C.yellow,
  Repeatable: C.orange,
  Initial: C.red,
};

function getLevelColor(level) {
  return levelColors[level] || C.textMuted;
}

function getScoreColor(score) {
  if (score >= 4.5) return C.green;
  if (score >= 3.5) return C.cyan;
  if (score >= 3.0) return C.yellow;
  if (score >= 2.0) return C.orange;
  return C.red;
}

// Fresh shadow factory (pptxgenjs mutates objects)
const mkShadow = () => ({
  type: "outer",
  blur: 4,
  offset: 2,
  angle: 135,
  color: "000000",
  opacity: 0.3,
});

// ── Build Presentation ──
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10" x 5.625"
pres.author = assessor;
pres.title = "DEBMM Assessment Report";

// ================================================================
// SLIDE 1: Title Slide
// ================================================================
const s1 = pres.addSlide();
s1.background = { color: C.bgDark };

// Top accent bar
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0,
  y: 0,
  w: 10,
  h: 0.06,
  fill: { color: C.cyan },
});

// Section label
s1.addText("DETECTION ENGINEERING BEHAVIOR MATURITY MODEL", {
  x: 0.6,
  y: 1.2,
  w: 8.8,
  h: 0.4,
  fontSize: 11,
  fontFace: "Consolas",
  color: C.cyan,
  charSpacing: 3,
  margin: 0,
});

// Main title
s1.addText("DEBMM Assessment Report", {
  x: 0.6,
  y: 1.65,
  w: 8.8,
  h: 0.8,
  fontSize: 36,
  fontFace: "Calibri",
  bold: true,
  color: C.white,
  margin: 0,
});

// Subtitle — org and date
const subtitleParts = [org || "Organization", assessDate].filter(Boolean);
s1.addText(subtitleParts.join("  ·  "), {
  x: 0.6,
  y: 2.5,
  w: 8.8,
  h: 0.4,
  fontSize: 16,
  fontFace: "Calibri",
  color: C.textSecondary,
  margin: 0,
});

// Bottom info bar
s1.addShape(pres.shapes.RECTANGLE, {
  x: 0,
  y: 4.6,
  w: 10,
  h: 1.025,
  fill: { color: C.bgCard },
});

const infoItems = [
  { label: "OVERALL SCORE", value: overallScore.toFixed(2) + " / 5.00" },
  { label: "ACHIEVED TIER", value: achievedTier },
  { label: "COMPLETION", value: completion },
  {
    label: "PASS / FAIL",
    value: `${passing} Pass  ·  ${failing} Below Target`,
  },
];

infoItems.forEach((item, i) => {
  const ix = 0.6 + i * 2.35;
  s1.addText(item.label, {
    x: ix,
    y: 4.72,
    w: 2.2,
    h: 0.25,
    fontSize: 9,
    fontFace: "Consolas",
    color: C.textMuted,
    margin: 0,
  });
  s1.addText(item.value, {
    x: ix,
    y: 4.98,
    w: 2.2,
    h: 0.35,
    fontSize: 14,
    fontFace: "Calibri",
    bold: true,
    color: C.textPrimary,
    margin: 0,
  });
});

// ================================================================
// SLIDE 2: Executive Summary — verdict + narrative + focus areas
// ================================================================
function buildExecSummary(d) {
  const achieved = d.achievedTier || "";
  const tierMatch = achieved.match(/Tier (\d+)/);
  const tierNum = tierMatch ? parseInt(tierMatch[1], 10) : -1;
  const tierNames = {
    0: "Foundation",
    1: "Basic",
    2: "Intermediate",
    3: "Advanced",
    4: "Expert",
  };
  const total = d.criteria.length;
  const passCt = d.criteria.filter((c) => c.status.includes("Pass")).length;
  const failCt = d.criteria.filter((c) => c.status.includes("Below")).length;

  // Focus areas: scoped to DEBMM Core criteria in the NEXT tier that are below 3.0.
  // These are the immediate blockers to advancement — matches the tier-capping logic.
  const nextTierName = tierNum >= 0 && tierNum < 4 ? tierNames[tierNum + 1] : tierNames[0];
  const nextBlockers = d.criteria
    .filter(
      (c) =>
        c.section === "DEBMM Core" &&
        c.category === nextTierName &&
        c.score < 3.0
    )
    .sort((a, b) => a.score - b.score);

  // Other below-3.0 criteria (in tiers above next, or in enrichment) — surfaced in the count
  // so the narrative is complete, but not shown in the headline focus list.
  const otherBlockers = d.criteria
    .filter((c) => c.score < 3.0 && !nextBlockers.includes(c))
    .sort((a, b) => a.score - b.score);

  let narrative;
  let action;

  if (tierNum === 4) {
    narrative = `Top of the maturity model. All ${total} criteria meet or exceed the Defined threshold (3.0).`;
    action = `Maintain optimization. Drive remaining scores toward 5.0 where strategic priorities apply.`;
  } else if (tierNum >= 0) {
    const nextNum = tierNum + 1;
    const blockerCt = nextBlockers.length;
    const otherCt = otherBlockers.length;
    const otherSuffix =
      otherCt > 0 ? ` (${otherCt} additional criterion below 3.0 in higher tiers.)` : "";

    if (blockerCt === 0) {
      narrative = `${achieved} achieved with all ${nextTierName} criteria above the Defined threshold. The next tier is unlocked by raising scores in higher-tier criteria.${otherSuffix}`;
      action = `Strengthen higher-tier criteria to advance beyond Tier ${nextNum}: ${nextTierName}.`;
    } else if (blockerCt === 1) {
      narrative = `${achieved} achieved. A single ${nextTierName} criterion is below 3.0 — once it crosses the threshold, Tier ${nextNum}: ${nextTierName} unlocks.${otherSuffix}`;
      action = `Focus the next quarter on the criterion below to unlock Tier ${nextNum}: ${nextTierName}.`;
    } else {
      narrative = `${achieved} achieved with ${passCt} of ${total} criteria meeting the Defined threshold. ${blockerCt} ${nextTierName} criteria below 3.0 are the immediate blockers to advancement.${otherSuffix}`;
      action = `Bring the ${blockerCt} ${nextTierName} criteria below to ≥3.0 to unlock Tier ${nextNum}: ${nextTierName}.`;
    }
  } else {
    const t0Blockers = d.criteria.filter(
      (c) => c.section === "DEBMM Core" && c.category === "Foundation" && c.score < 3.0
    );
    narrative = `${achieved || "Below Foundation"} — ${failCt} criteria below 3.0 across the assessment. ${t0Blockers.length} Foundation criteria are the gating items.`;
    action = `Prioritize Foundation criteria first: rule development, maintenance, roadmaps, threat modeling.`;
  }

  // The list shown on the slide IS scoped to next-tier blockers so it matches the narrative.
  return {
    achieved,
    narrative,
    action,
    blockers: nextBlockers,
    passCt,
    failCt,
    total,
    tierNum,
    nextTierName,
  };
}

const exec = buildExecSummary(data);

const sExec = pres.addSlide();
sExec.background = { color: C.bgDark };

// Top accent
sExec.addShape(pres.shapes.RECTANGLE, {
  x: 0,
  y: 0,
  w: 10,
  h: 0.06,
  fill: { color: C.cyan },
});

// Section label
sExec.addText("EXECUTIVE SUMMARY", {
  x: 0.6,
  y: 0.25,
  w: 8,
  h: 0.3,
  fontSize: 10,
  fontFace: "Consolas",
  color: C.textMuted,
  charSpacing: 2,
  margin: 0,
});

// Title
sExec.addText("Where You Stand", {
  x: 0.6,
  y: 0.55,
  w: 8,
  h: 0.5,
  fontSize: 24,
  fontFace: "Calibri",
  bold: true,
  color: C.white,
  margin: 0,
});

// ── Verdict card (top half, full width) ──
const verdictY = 1.15;
const verdictH = 1.25;
sExec.addShape(pres.shapes.RECTANGLE, {
  x: 0.6,
  y: verdictY,
  w: 8.8,
  h: verdictH,
  fill: { color: C.bgCard },
  shadow: mkShadow(),
});

// Tier color accent strip on the left
const verdictColor = (() => {
  if (exec.tierNum === 4) return C.purple;
  if (exec.tierNum === 3) return C.orange;
  if (exec.tierNum === 2) return C.yellow;
  if (exec.tierNum === 1) return C.blue;
  if (exec.tierNum === 0) return C.green;
  return C.red;
})();
sExec.addShape(pres.shapes.RECTANGLE, {
  x: 0.6,
  y: verdictY,
  w: 0.1,
  h: verdictH,
  fill: { color: verdictColor },
});

// "ACHIEVED TIER" label
sExec.addText("ACHIEVED TIER", {
  x: 0.9,
  y: verdictY + 0.12,
  w: 4,
  h: 0.22,
  fontSize: 10,
  fontFace: "Consolas",
  color: C.textMuted,
  charSpacing: 2,
  margin: 0,
});

// Tier name (large)
sExec.addText(exec.achieved || "Not Yet Achieved", {
  x: 0.9,
  y: verdictY + 0.32,
  w: 7.8,
  h: 0.6,
  fontSize: 28,
  fontFace: "Calibri",
  bold: true,
  color: verdictColor,
  margin: 0,
});

// Score line
sExec.addText(
  `${overallScore.toFixed(2)} / 5.00   ·   ${exec.passCt} of ${exec.total} criteria above 3.0`,
  {
    x: 0.9,
    y: verdictY + 0.92,
    w: 7.8,
    h: 0.28,
    fontSize: 13,
    fontFace: "Calibri",
    color: C.textSecondary,
    margin: 0,
  }
);

// ── Narrative block ──
sExec.addText(exec.narrative, {
  x: 0.6,
  y: verdictY + verdictH + 0.15,
  w: 8.8,
  h: 0.5,
  fontSize: 11,
  fontFace: "Calibri",
  color: C.textPrimary,
  margin: 0,
});

// ── Action / next step (highlighted) ──
sExec.addText(`→ ${exec.action}`, {
  x: 0.6,
  y: verdictY + verdictH + 0.62,
  w: 8.8,
  h: 0.32,
  fontSize: 11,
  fontFace: "Calibri",
  bold: true,
  color: C.cyan,
  margin: 0,
});

// ── Focus areas list (only if there are blockers in the next tier) ──
const focusY = 3.4;
if (exec.blockers.length > 0) {
  sExec.addText(
    `FOCUS AREAS — ${exec.nextTierName.toUpperCase()} CRITERIA TO ADDRESS`,
    {
      x: 0.6,
      y: focusY,
      w: 8.8,
      h: 0.22,
      fontSize: 9,
      fontFace: "Consolas",
      color: C.textMuted,
      charSpacing: 2,
      margin: 0,
    }
  );

  // Show up to 3 next-tier blockers; remainder summarized in footnote
  const focusItems = exec.blockers.slice(0, 3);
  const itemH = 0.5;
  focusItems.forEach((b, i) => {
    const iy = focusY + 0.32 + i * itemH;
    // Score pill
    sExec.addShape(pres.shapes.RECTANGLE, {
      x: 0.6,
      y: iy + 0.05,
      w: 0.55,
      h: 0.22,
      fill: { color: getScoreColor(b.score) },
    });
    sExec.addText(b.score.toFixed(2), {
      x: 0.6,
      y: iy + 0.05,
      w: 0.55,
      h: 0.22,
      fontSize: 9,
      fontFace: "Consolas",
      bold: true,
      color: C.bgDark,
      align: "center",
      valign: "middle",
      margin: 0,
    });
    // Criterion name (line 1)
    sExec.addText(b.criterion, {
      x: 1.3,
      y: iy + 0.02,
      w: 8.0,
      h: 0.24,
      fontSize: 11,
      fontFace: "Calibri",
      bold: true,
      color: C.textPrimary,
      margin: 0,
    });
    // Target description (line 2) — what "Defined" looks like for this criterion
    if (b.target) {
      sExec.addText(`Target: ${b.target}`, {
        x: 1.3,
        y: iy + 0.24,
        w: 8.0,
        h: 0.22,
        fontSize: 9,
        fontFace: "Calibri",
        color: C.textSecondary,
        italic: true,
        margin: 0,
      });
    }
  });

  // Footnote if list was truncated
  if (exec.blockers.length > focusItems.length) {
    const more = exec.blockers.length - focusItems.length;
    sExec.addText(
      `+ ${more} more — see Slide 4 for the full criteria breakdown.`,
      {
        x: 0.6,
        y: focusY + 0.32 + focusItems.length * itemH + 0.05,
        w: 8.8,
        h: 0.22,
        fontSize: 9,
        fontFace: "Calibri",
        italic: true,
        color: C.textMuted,
        margin: 0,
      }
    );
  }
} else {
  sExec.addText(
    `All ${exec.nextTierName} criteria meet the Defined threshold. Advancement requires raising scores in higher-tier criteria.`,
    {
      x: 0.6,
      y: focusY + 0.2,
      w: 8.8,
      h: 0.6,
      fontSize: 12,
      fontFace: "Calibri",
      color: C.green,
      margin: 0,
    }
  );
}

// ================================================================
// SLIDE 3: Tier Progression + KPI Summary
// ================================================================
const s2 = pres.addSlide();
s2.background = { color: C.bgDark };

// Top accent
s2.addShape(pres.shapes.RECTANGLE, {
  x: 0,
  y: 0,
  w: 10,
  h: 0.06,
  fill: { color: C.cyan },
});

// Section label
s2.addText("01  TIER PROGRESSION", {
  x: 0.6,
  y: 0.25,
  w: 8,
  h: 0.3,
  fontSize: 10,
  fontFace: "Consolas",
  color: C.textMuted,
  charSpacing: 2,
  margin: 0,
});

// Title
s2.addText("DEBMM Tier Overview", {
  x: 0.6,
  y: 0.55,
  w: 8,
  h: 0.5,
  fontSize: 24,
  fontFace: "Calibri",
  bold: true,
  color: C.white,
  margin: 0,
});

// 5 Tier KPI cards across the top
const cardW = 1.68;
const cardGap = 0.15;
const cardStartX = 0.6;
const cardY = 1.25;
const cardH = 1.5;

tiers.forEach((t, i) => {
  const cx = cardStartX + i * (cardW + cardGap);
  const tc = tierColors[t.id] || C.textMuted;

  // Card background
  s2.addShape(pres.shapes.RECTANGLE, {
    x: cx,
    y: cardY,
    w: cardW,
    h: cardH,
    fill: { color: C.bgCard },
    shadow: mkShadow(),
  });

  // Top color accent
  s2.addShape(pres.shapes.RECTANGLE, {
    x: cx,
    y: cardY,
    w: cardW,
    h: 0.05,
    fill: { color: tc },
  });

  // Tier label
  s2.addText(`${t.id} — ${t.name}`, {
    x: cx + 0.12,
    y: cardY + 0.15,
    w: cardW - 0.24,
    h: 0.22,
    fontSize: 8,
    fontFace: "Consolas",
    color: C.textMuted,
    margin: 0,
  });

  // Score
  s2.addText(t.score.toFixed(2), {
    x: cx + 0.12,
    y: cardY + 0.38,
    w: cardW - 0.24,
    h: 0.42,
    fontSize: 28,
    fontFace: "Consolas",
    bold: true,
    color: tc,
    margin: 0,
  });

  // Level
  s2.addText(t.level, {
    x: cx + 0.12,
    y: cardY + 0.78,
    w: cardW - 0.24,
    h: 0.2,
    fontSize: 11,
    fontFace: "Calibri",
    color: C.textSecondary,
    margin: 0,
  });

  // Progress bar background
  s2.addShape(pres.shapes.RECTANGLE, {
    x: cx + 0.12,
    y: cardY + 1.1,
    w: cardW - 0.24,
    h: 0.08,
    fill: { color: C.bgDark },
  });

  // Progress bar fill
  const pct = Math.min(t.score / 5, 1);
  s2.addShape(pres.shapes.RECTANGLE, {
    x: cx + 0.12,
    y: cardY + 1.1,
    w: (cardW - 0.24) * pct,
    h: 0.08,
    fill: { color: tc },
  });

  // Progression status
  s2.addText(t.progression, {
    x: cx + 0.12,
    y: cardY + 1.24,
    w: cardW - 0.24,
    h: 0.18,
    fontSize: 8,
    fontFace: "Calibri",
    color: t.progression === "Complete" ? C.green : C.textMuted,
    margin: 0,
  });
});

// ── Bottom section: Summary stats ──
const statY = 3.05;
s2.addText("ASSESSMENT SUMMARY", {
  x: 0.6,
  y: statY,
  w: 8,
  h: 0.25,
  fontSize: 10,
  fontFace: "Consolas",
  color: C.textMuted,
  charSpacing: 2,
  margin: 0,
});

// Summary cards row
const summCards = [
  {
    label: "Overall Score",
    value: overallScore.toFixed(2),
    sub: "out of 5.00",
    color: C.cyan,
  },
  {
    label: "Achieved Tier",
    value: achievedTier.replace("Tier ", "T"),
    sub: "",
    color: C.cyan,
  },
  { label: "Passing", value: String(passing), sub: "criteria", color: C.green },
  {
    label: "Below Target",
    value: String(failing),
    sub: "criteria",
    color: failing > 0 ? C.red : C.green,
  },
  {
    label: "DEBMM Core Avg",
    value: (
      debmmCore.reduce((a, c) => a + c.score, 0) / debmmCore.length
    ).toFixed(2),
    sub: "",
    color: C.cyan,
  },
  {
    label: "Enrichment Avg",
    value: (
      enrichment.reduce((a, c) => a + c.score, 0) / enrichment.length
    ).toFixed(2),
    sub: "",
    color: C.green,
  },
];

const scW = 1.35;
const scGap = 0.12;
summCards.forEach((sc, i) => {
  const sx = 0.6 + i * (scW + scGap);
  const sy = statY + 0.35;

  s2.addShape(pres.shapes.RECTANGLE, {
    x: sx,
    y: sy,
    w: scW,
    h: 1.1,
    fill: { color: C.bgCard },
    shadow: mkShadow(),
  });

  s2.addText(sc.label, {
    x: sx + 0.1,
    y: sy + 0.1,
    w: scW - 0.2,
    h: 0.18,
    fontSize: 8,
    fontFace: "Consolas",
    color: C.textMuted,
    margin: 0,
  });

  // Auto-size: shrink font if value text is long
  const valFontSize = sc.value.length > 10 ? 13 : sc.value.length > 6 ? 18 : 24;
  s2.addText(sc.value, {
    x: sx + 0.1,
    y: sy + 0.32,
    w: scW - 0.2,
    h: 0.42,
    fontSize: valFontSize,
    fontFace: "Consolas",
    bold: true,
    color: sc.color,
    valign: "middle",
    margin: 0,
  });

  if (sc.sub) {
    s2.addText(sc.sub, {
      x: sx + 0.1,
      y: sy + 0.75,
      w: scW - 0.2,
      h: 0.18,
      fontSize: 9,
      fontFace: "Calibri",
      color: C.textSecondary,
      margin: 0,
    });
  }
});

// Bottom bar - tier progression visual
const barY = 4.8;
s2.addShape(pres.shapes.RECTANGLE, {
  x: 0,
  y: barY,
  w: 10,
  h: 0.825,
  fill: { color: C.bgCard },
});

s2.addText("TIER PROGRESSION", {
  x: 0.6,
  y: barY + 0.08,
  w: 3,
  h: 0.18,
  fontSize: 8,
  fontFace: "Consolas",
  color: C.textMuted,
  charSpacing: 2,
  margin: 0,
});

const segW = 1.68;
tiers.forEach((t, i) => {
  const sx = 0.6 + i * (segW + 0.08);
  const sy = barY + 0.32;

  let segColor = C.bgCardAlt;
  let borderColor = C.border;
  let labelColor = C.textMuted;

  if (t.progression === "Complete") {
    segColor = "0D2818";
    borderColor = C.green;
    labelColor = C.green;
  } else if (t.progression === "Current") {
    segColor = "0B1F2E";
    borderColor = C.cyan;
    labelColor = C.cyan;
  } else if (t.progression === "In Progress") {
    segColor = "1A1708";
    borderColor = C.yellow;
    labelColor = C.yellow;
  }

  s2.addShape(pres.shapes.RECTANGLE, {
    x: sx,
    y: sy,
    w: segW,
    h: 0.4,
    fill: { color: segColor },
    line: { color: borderColor, width: 1 },
  });

  s2.addText(`${t.id}  ${t.name}`, {
    x: sx + 0.1,
    y: sy + 0.02,
    w: segW - 0.2,
    h: 0.2,
    fontSize: 9,
    fontFace: "Consolas",
    bold: true,
    color: labelColor,
    margin: 0,
  });

  s2.addText(t.progression, {
    x: sx + 0.1,
    y: sy + 0.2,
    w: segW - 0.2,
    h: 0.16,
    fontSize: 8,
    fontFace: "Calibri",
    color: labelColor,
    margin: 0,
  });
});

// ================================================================
// SLIDE 3: DEBMM Core Criteria Detail
// ================================================================
const s3 = pres.addSlide();
s3.background = { color: C.bgDark };

s3.addShape(pres.shapes.RECTANGLE, {
  x: 0,
  y: 0,
  w: 10,
  h: 0.06,
  fill: { color: C.cyan },
});

s3.addText("02  DEBMM CORE", {
  x: 0.6,
  y: 0.2,
  w: 8,
  h: 0.25,
  fontSize: 10,
  fontFace: "Consolas",
  color: C.textMuted,
  charSpacing: 2,
  margin: 0,
});

s3.addText("Core Criteria Breakdown", {
  x: 0.6,
  y: 0.45,
  w: 8,
  h: 0.4,
  fontSize: 22,
  fontFace: "Calibri",
  bold: true,
  color: C.white,
  margin: 0,
});

// Table header
const tblHeaderY = 0.95;
const colX = [0.6, 3.2, 5.6, 6.7, 7.65, 8.6];
const colLabels = ["Criterion", "Category", "Level", "Score", "Bar", "Status"];
const colW = [2.6, 2.4, 1.1, 0.95, 0.95, 0.8];

// Header background
s3.addShape(pres.shapes.RECTANGLE, {
  x: 0.5,
  y: tblHeaderY,
  w: 9.0,
  h: 0.28,
  fill: { color: C.bgCard },
});

colLabels.forEach((lbl, i) => {
  s3.addText(lbl.toUpperCase(), {
    x: colX[i],
    y: tblHeaderY + 0.02,
    w: colW[i],
    h: 0.24,
    fontSize: 7,
    fontFace: "Consolas",
    color: C.textMuted,
    charSpacing: 1,
    margin: 0,
  });
});

// Data rows
const rowH = 0.21;
const startY = tblHeaderY + 0.3;

debmmCore.forEach((c, i) => {
  const ry = startY + i * (rowH + 0.01);
  const isBelow = c.status.includes("Below");
  const sc = getScoreColor(c.score);

  // Alternating row bg
  if (i % 2 === 0) {
    s3.addShape(pres.shapes.RECTANGLE, {
      x: 0.5,
      y: ry - 0.02,
      w: 9.0,
      h: rowH + 0.02,
      fill: { color: C.bgCard },
    });
  }

  // Criterion name
  s3.addText(c.criterion, {
    x: colX[0],
    y: ry,
    w: colW[0],
    h: rowH,
    fontSize: 9,
    fontFace: "Calibri",
    color: isBelow ? C.red : C.textPrimary,
    margin: 0,
  });

  // Category
  s3.addText(c.category, {
    x: colX[1],
    y: ry,
    w: colW[1],
    h: rowH,
    fontSize: 9,
    fontFace: "Calibri",
    color: C.textSecondary,
    margin: 0,
  });

  // Level badge
  s3.addShape(pres.shapes.RECTANGLE, {
    x: colX[2],
    y: ry + 0.02,
    w: 0.95,
    h: 0.18,
    fill: { color: C.bgCardAlt },
  });
  s3.addText(c.level, {
    x: colX[2],
    y: ry + 0.02,
    w: 0.95,
    h: 0.18,
    fontSize: 7,
    fontFace: "Consolas",
    bold: true,
    color: getLevelColor(c.level),
    align: "center",
    valign: "middle",
    margin: 0,
  });

  // Score
  s3.addText(c.score.toFixed(2), {
    x: colX[3],
    y: ry,
    w: colW[3],
    h: rowH,
    fontSize: 10,
    fontFace: "Consolas",
    bold: true,
    color: sc,
    align: "center",
    margin: 0,
  });

  // Score bar
  const barW = 0.85;
  s3.addShape(pres.shapes.RECTANGLE, {
    x: colX[4],
    y: ry + 0.07,
    w: barW,
    h: 0.08,
    fill: { color: C.bgDark },
  });
  s3.addShape(pres.shapes.RECTANGLE, {
    x: colX[4],
    y: ry + 0.07,
    w: barW * Math.min(c.score / 5, 1),
    h: 0.08,
    fill: { color: sc },
  });

  // Status icon
  s3.addText(isBelow ? "✗" : "✓", {
    x: colX[5],
    y: ry,
    w: colW[5],
    h: rowH,
    fontSize: 11,
    fontFace: "Calibri",
    bold: true,
    color: isBelow ? C.red : C.green,
    align: "center",
    margin: 0,
  });
});

// ================================================================
// SLIDE 4: Enrichment Criteria
// ================================================================
const s4 = pres.addSlide();
s4.background = { color: C.bgDark };

s4.addShape(pres.shapes.RECTANGLE, {
  x: 0,
  y: 0,
  w: 10,
  h: 0.06,
  fill: { color: C.cyan },
});

s4.addText("03  ENRICHMENT", {
  x: 0.6,
  y: 0.2,
  w: 8,
  h: 0.25,
  fontSize: 10,
  fontFace: "Consolas",
  color: C.textMuted,
  charSpacing: 2,
  margin: 0,
});

s4.addText("People, Process & Governance", {
  x: 0.6,
  y: 0.45,
  w: 8,
  h: 0.4,
  fontSize: 22,
  fontFace: "Calibri",
  bold: true,
  color: C.white,
  margin: 0,
});

// Enrichment as cards (2 columns x 3 rows)
const enrCardW = 4.1;
const enrCardH = 1.0;
const enrGap = 0.15;
const enrStartY = 1.05;

enrichment.forEach((c, i) => {
  const col = i % 2;
  const row = Math.floor(i / 2);
  const cx = 0.6 + col * (enrCardW + enrGap);
  const cy = enrStartY + row * (enrCardH + enrGap);
  const sc = getScoreColor(c.score);
  const lc = getLevelColor(c.level);

  // Card bg
  s4.addShape(pres.shapes.RECTANGLE, {
    x: cx,
    y: cy,
    w: enrCardW,
    h: enrCardH,
    fill: { color: C.bgCard },
    shadow: mkShadow(),
  });

  // Left accent
  s4.addShape(pres.shapes.RECTANGLE, {
    x: cx,
    y: cy,
    w: 0.06,
    h: enrCardH,
    fill: { color: lc },
  });

  // Category label
  s4.addText(c.category.toUpperCase(), {
    x: cx + 0.2,
    y: cy + 0.1,
    w: enrCardW - 1.2,
    h: 0.18,
    fontSize: 7,
    fontFace: "Consolas",
    color: C.textMuted,
    charSpacing: 1,
    margin: 0,
  });

  // Criterion name
  s4.addText(c.criterion, {
    x: cx + 0.2,
    y: cy + 0.3,
    w: enrCardW - 1.2,
    h: 0.25,
    fontSize: 12,
    fontFace: "Calibri",
    bold: true,
    color: C.textPrimary,
    margin: 0,
  });

  // Level badge
  s4.addShape(pres.shapes.RECTANGLE, {
    x: cx + 0.2,
    y: cy + 0.65,
    w: 0.8,
    h: 0.22,
    fill: { color: C.bgCardAlt },
  });
  s4.addText(c.level, {
    x: cx + 0.2,
    y: cy + 0.65,
    w: 0.8,
    h: 0.22,
    fontSize: 8,
    fontFace: "Consolas",
    bold: true,
    color: lc,
    align: "center",
    valign: "middle",
    margin: 0,
  });

  // Status text
  s4.addText(c.status, {
    x: cx + 1.1,
    y: cy + 0.65,
    w: 1.2,
    h: 0.22,
    fontSize: 8,
    fontFace: "Calibri",
    color: c.status.includes("Pass") ? C.green : C.red,
    valign: "middle",
    margin: 0,
  });

  // Score (big, right side)
  s4.addText(c.score.toFixed(2), {
    x: cx + enrCardW - 1.1,
    y: cy + 0.15,
    w: 0.95,
    h: 0.55,
    fontSize: 28,
    fontFace: "Consolas",
    bold: true,
    color: sc,
    align: "center",
    valign: "middle",
    margin: 0,
  });

  // Score bar
  s4.addShape(pres.shapes.RECTANGLE, {
    x: cx + enrCardW - 1.1,
    y: cy + 0.78,
    w: 0.9,
    h: 0.08,
    fill: { color: C.bgDark },
  });
  s4.addShape(pres.shapes.RECTANGLE, {
    x: cx + enrCardW - 1.1,
    y: cy + 0.78,
    w: 0.9 * Math.min(c.score / 5, 1),
    h: 0.08,
    fill: { color: sc },
  });
});

// Bottom summary bar
const enrBarY = 4.6;
s4.addShape(pres.shapes.RECTANGLE, {
  x: 0,
  y: enrBarY,
  w: 10,
  h: 1.025,
  fill: { color: C.bgCard },
});

// People avg
const peopleOrg = enrichment.filter((c) =>
  c.category.includes("People")
);
const processGov = enrichment.filter((c) =>
  c.category.includes("Process")
);
const poAvg =
  peopleOrg.reduce((a, c) => a + c.score, 0) / peopleOrg.length;
const pgAvg =
  processGov.reduce((a, c) => a + c.score, 0) / processGov.length;
const enrAvg =
  enrichment.reduce((a, c) => a + c.score, 0) / enrichment.length;

const enrStats = [
  { label: "ENRICHMENT AVG", value: enrAvg.toFixed(2), color: C.cyan },
  { label: "PEOPLE & ORG", value: poAvg.toFixed(2), color: C.green },
  { label: "PROCESS & GOV", value: pgAvg.toFixed(2), color: C.blue },
  {
    label: "ALL PASSING",
    value: enrichment.every((c) => c.status.includes("Pass")) ? "YES" : "NO",
    color: enrichment.every((c) => c.status.includes("Pass"))
      ? C.green
      : C.red,
  },
];

enrStats.forEach((st, i) => {
  const sx = 0.6 + i * 2.35;
  s4.addText(st.label, {
    x: sx,
    y: enrBarY + 0.15,
    w: 2.1,
    h: 0.2,
    fontSize: 9,
    fontFace: "Consolas",
    color: C.textMuted,
    margin: 0,
  });
  s4.addText(st.value, {
    x: sx,
    y: enrBarY + 0.4,
    w: 2.1,
    h: 0.4,
    fontSize: 22,
    fontFace: "Consolas",
    bold: true,
    color: st.color,
    margin: 0,
  });
});

// ================================================================
// Write file
// ================================================================
pres.writeFile({ fileName: outPath }).then(() => {
  console.log("DEBMM report generated: " + outPath);
});
