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

// Kicker (subdued lead-in, not a decorative monospace eyebrow)
s1.addText("Detection Engineering Maturity Assessment", {
  x: 0.6,
  y: 1.4,
  w: 8.8,
  h: 0.32,
  fontSize: 13,
  fontFace: "Calibri",
  color: C.textSecondary,
  margin: 0,
});

// Main title
s1.addText("DEBMM Assessment Report", {
  x: 0.6,
  y: 1.75,
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
  { label: "Overall score", value: overallScore.toFixed(2) + " / 5.00" },
  { label: "Achieved tier", value: achievedTier },
  { label: "Completion", value: completion },
  {
    label: "Pass / fail",
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
    fontSize: 11,
    fontFace: "Calibri",
    italic: true,
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

  // Per-tier narrative — same text the Excel Results Dashboard uses, so the
  // deck and the workbook tell the same story. Each paragraph names what is
  // working at the achieved tier AND what specifically to focus on to unlock
  // the next tier.
  const tierExplanations = {
    "Below Foundation":
      "Your organization has not yet achieved Tier 0 (Foundation). One or more foundational criteria — such as structured rule development, rule maintenance, roadmap documentation, or threat modeling — score below the Defined level (3.0). Focus on establishing basic, repeatable processes in these areas before advancing to higher tiers.",
    "Tier 0: Foundation":
      "Your organization has achieved Tier 0 (Foundation). All foundational criteria meet the Defined level — you have documented processes for rule development, maintenance, roadmaps, and threat modeling. To reach Tier 1, ensure baseline rules, telemetry quality, threat landscape reviews, and release testing also reach the Defined level.",
    "Tier 1: Basic":
      "Your organization has achieved Tier 1 (Basic). You have solid foundations and basic detection capabilities in place, including baseline rules, telemetry coverage, and release testing at the Defined level. To advance to Tier 2, focus on systematic false positive reduction, formal gap analysis, and internal testing and validation.",
    "Tier 2: Intermediate":
      "Your organization has achieved Tier 2 (Intermediate). Your detection program has mature processes for rule development, telemetry management, false positive reduction, and gap analysis. To advance to Tier 3, invest in false negative triage, external validation (e.g., purple team exercises), and coverage of advanced TTPs.",
    "Tier 3: Advanced":
      "Your organization has achieved Tier 3 (Advanced). You have a highly capable detection program with systematic FN reduction, external validation, and behavioral detection of advanced TTPs. To reach Tier 4, develop proactive threat hunting capabilities, adopt hypothesis-driven hunting workflows, and integrate automation and AI across the detection lifecycle.",
    "Tier 4: Expert":
      "Your organization has achieved Tier 4 (Expert) — the highest DEBMM tier. Your detection engineering program is mature across all dimensions: proactive threat hunting, automation of key lifecycle stages, and continuous improvement driven by data. Focus on sustaining this level and contributing to the broader detection engineering community.",
  };
  const narrative = tierExplanations[achieved] || tierExplanations["Below Foundation"];

  // Short action sentence — kept for the next-tier card
  let action;
  if (tierNum === 4) {
    action = "Maintain optimization. Drive remaining scores toward 5.0 where strategic priorities apply.";
  } else if (tierNum >= 0) {
    const nextNum = tierNum + 1;
    const blockerCt = nextBlockers.length;
    if (blockerCt === 0) {
      action = `Strengthen higher-tier criteria to advance beyond Tier ${nextNum}: ${nextTierName}.`;
    } else {
      const word = blockerCt === 1 ? "criterion" : "criteria";
      action = `Bring the ${blockerCt} ${nextTierName} ${word} below to ≥3.0 to unlock Tier ${nextNum}: ${nextTierName}.`;
    }
  } else {
    action = "Prioritize Foundation criteria first: rule development, maintenance, roadmaps, threat modeling.";
  }

  // Top current strengths — surfaced in the exec summary opposite the focus areas
  // so the slide tells "what's working" alongside "what to fix."
  const strengths = d.criteria
    .filter((c) => c.score >= 4.0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 5);

  // The list shown on the slide IS scoped to next-tier blockers so it matches the narrative.
  return {
    achieved,
    narrative,
    action,
    blockers: nextBlockers,
    strengths,
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

// Title (compact — single line, paired with takeaway banner below)
sExec.addText("Executive Summary", {
  x: 0.6,
  y: 0.25,
  w: 8,
  h: 0.45,
  fontSize: 22,
  fontFace: "Calibri",
  bold: true,
  color: C.white,
  margin: 0,
});

// ── Tier-specific narrative banner ──
// Same per-tier paragraph the Excel Results Dashboard shows, so the deck and
// the workbook tell the same story. Names what's working at the achieved tier
// AND what specifically to focus on to unlock the next tier.
const narrativeY = 0.78;
const narrativeH = 0.92;
sExec.addShape(pres.shapes.RECTANGLE, {
  x: 0.6,
  y: narrativeY,
  w: 8.8,
  h: narrativeH,
  fill: { color: C.bgCard },
});
sExec.addShape(pres.shapes.RECTANGLE, {
  x: 0.6,
  y: narrativeY,
  w: 0.08,
  h: narrativeH,
  fill: { color: tierAccentColor(exec.tierNum) },
});
sExec.addText(exec.narrative, {
  x: 0.85,
  y: narrativeY + 0.05,
  w: 8.45,
  h: narrativeH - 0.10,
  fontSize: 11,
  fontFace: "Calibri",
  color: C.textPrimary,
  valign: "top",
  margin: 0,
});

// ── Three-column hero: Maturity | Coverage | Next tier ──
const heroY = 1.85;
const heroH = 1.65;
const heroLeftX = 0.6;
const heroColW = 2.83;
const heroGap = 0.15;

function tierAccentColor(n) {
  if (n === 4) return C.purple;
  if (n === 3) return C.orange;
  if (n === 2) return C.yellow;
  if (n === 1) return C.blue;
  if (n === 0) return C.green;
  return C.red;
}
const verdictColor = tierAccentColor(exec.tierNum);

function drawHeroColumn(slide, x, y, w, h, accent, label, contentFn) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: C.bgCard },
    shadow: mkShadow(),
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.08, h,
    fill: { color: accent },
  });
  slide.addText(label, {
    x: x + 0.22, y: y + 0.14, w: w - 0.32, h: 0.22,
    fontSize: 10, fontFace: "Calibri", italic: true, color: C.textMuted, margin: 0,
  });
  contentFn(x + 0.22, y + 0.40, w - 0.32);
}

// Column 1 — Maturity (Verdict)
drawHeroColumn(sExec, heroLeftX, heroY, heroColW, heroH, verdictColor, "Maturity", (cx, cy, cw) => {
  // Tier badge: large name in tier color
  sExec.addText(exec.achieved || "Not Yet Achieved", {
    x: cx, y: cy, w: cw, h: 0.5,
    fontSize: 22, fontFace: "Calibri", bold: true, color: verdictColor, margin: 0,
  });
  // Score
  sExec.addText(`${overallScore.toFixed(2)} / 5.00`, {
    x: cx, y: cy + 0.50, w: cw, h: 0.28,
    fontSize: 14, fontFace: "Calibri", color: C.textPrimary, margin: 0,
  });
  // Tier stepper — visual journey across all 5 tiers
  const stepperY = cy + 0.92;
  const stepCount = 5;
  const stepRadius = 0.10;
  const stepGap = (cw - stepCount * stepRadius * 2) / (stepCount - 1);
  for (let t = 0; t < stepCount; t++) {
    const sx = cx + t * (stepRadius * 2 + stepGap);
    let dotColor;
    let textColor;
    if (t < exec.tierNum) {
      dotColor = tierAccentColor(t); textColor = tierAccentColor(t);
    } else if (t === exec.tierNum) {
      dotColor = tierAccentColor(t); textColor = tierAccentColor(t);
    } else {
      dotColor = C.bgCardAlt; textColor = C.textMuted;
    }
    // Connector line to next dot (drawn before the dot so the dot sits on top)
    if (t < stepCount - 1) {
      const lineColor = (t < exec.tierNum) ? tierAccentColor(t) : C.bgCardAlt;
      sExec.addShape(pres.shapes.RECTANGLE, {
        x: sx + stepRadius * 2, y: stepperY + stepRadius - 0.015,
        w: stepGap, h: 0.03,
        fill: { color: lineColor },
      });
    }
    // Dot
    sExec.addShape(pres.shapes.OVAL, {
      x: sx, y: stepperY,
      w: stepRadius * 2, h: stepRadius * 2,
      fill: { color: dotColor },
    });
    // T0..T4 label below
    sExec.addText(`T${t}`, {
      x: sx - 0.08, y: stepperY + stepRadius * 2 + 0.06, w: stepRadius * 2 + 0.16, h: 0.2,
      fontSize: 9, fontFace: "Calibri", color: textColor, align: "center", margin: 0,
    });
  }
});

// Column 2 — Coverage (Implications)
drawHeroColumn(sExec, heroLeftX + heroColW + heroGap, heroY, heroColW, heroH, C.cyan, "Coverage", (cx, cy, cw) => {
  // Big stat
  sExec.addText(`${exec.passCt} of ${exec.total}`, {
    x: cx, y: cy, w: cw, h: 0.5,
    fontSize: 22, fontFace: "Calibri", bold: true, color: C.textPrimary, margin: 0,
  });
  sExec.addText("criteria meet the Defined threshold", {
    x: cx, y: cy + 0.50, w: cw, h: 0.22,
    fontSize: 10, fontFace: "Calibri", italic: true, color: C.textMuted, margin: 0,
  });
  // Progress bar (cyan filled to passCt/total)
  const pct = exec.total > 0 ? exec.passCt / exec.total : 0;
  const barY = cy + 0.85;
  const barH = 0.16;
  sExec.addShape(pres.shapes.RECTANGLE, {
    x: cx, y: barY, w: cw, h: barH,
    fill: { color: C.bgDark },
  });
  sExec.addShape(pres.shapes.RECTANGLE, {
    x: cx, y: barY, w: cw * pct, h: barH,
    fill: { color: C.cyan },
  });
  // Percentage label
  sExec.addText(`${Math.round(pct * 100)}%`, {
    x: cx, y: barY + barH + 0.04, w: cw, h: 0.22,
    fontSize: 11, fontFace: "Calibri", bold: true, color: C.cyan, margin: 0,
  });
  // Failing count caption (right-aligned next to the percentage)
  if (exec.failCt > 0) {
    sExec.addText(
      `${exec.failCt} ${exec.failCt === 1 ? "criterion" : "criteria"} below threshold`,
      {
        x: cx, y: barY + barH + 0.04, w: cw, h: 0.22,
        fontSize: 10, fontFace: "Calibri", italic: true, color: C.textMuted, align: "right", margin: 0,
      }
    );
  } else {
    // 100% case — fill the right-hand area with a green confirmation so the row isn't half-empty
    sExec.addText("All criteria above 3.0", {
      x: cx, y: barY + barH + 0.04, w: cw, h: 0.22,
      fontSize: 10, fontFace: "Calibri", italic: true, color: C.green, align: "right", margin: 0,
    });
  }
});

// Column 3 — Next tier (Next step)
drawHeroColumn(sExec, heroLeftX + 2 * (heroColW + heroGap), heroY, heroColW, heroH, C.cyan, "Next tier", (cx, cy, cw) => {
  const headline = exec.tierNum >= 0 && exec.tierNum < 4
    ? `Tier ${exec.tierNum + 1}: ${exec.nextTierName}`
    : exec.tierNum === 4 ? "All tiers achieved" : "Reach Foundation";
  // Headline: target tier name
  sExec.addText(headline, {
    x: cx, y: cy, w: cw, h: 0.42,
    fontSize: 16, fontFace: "Calibri", bold: true, color: C.cyan, margin: 0,
  });

  // Build the unlock summary sentence
  const blockerCt = exec.blockers.length;
  let unlockText;
  let badgeColor = C.cyan;
  let badgeNum = "";
  if (exec.tierNum === 4) {
    unlockText = "Maintain optimization across all criteria. Continue measuring against the rubric.";
    badgeNum = "";
  } else if (exec.tierNum >= 0) {
    if (blockerCt === 0) {
      unlockText = `All ${exec.nextTierName} criteria meet the threshold. Raise scores in higher-tier criteria to continue advancing.`;
      badgeNum = "";
    } else {
      const word = blockerCt === 1 ? "criterion" : "criteria";
      unlockText = `Unlocked by raising ${blockerCt} ${exec.nextTierName} ${word} above the Defined threshold (3.0).`;
      badgeNum = String(blockerCt);
    }
  } else {
    const word = blockerCt === 1 ? "criterion" : "criteria";
    unlockText = `Reach Foundation by raising ${blockerCt} ${word} above the Defined threshold (3.0).`;
    badgeNum = String(blockerCt);
    badgeColor = C.red;
  }

  // Visual: numeric badge + caption row (parallels the stat layout in the other cards)
  if (badgeNum) {
    sExec.addText(badgeNum, {
      x: cx, y: cy + 0.50, w: 0.7, h: 0.45,
      fontSize: 28, fontFace: "Calibri", bold: true, color: badgeColor,
      align: "left", valign: "middle", margin: 0,
    });
    sExec.addText(
      blockerCt === 1
        ? `${exec.nextTierName || "Foundation"} criterion below threshold`
        : `${exec.nextTierName || "Foundation"} criteria below threshold`,
      {
        x: cx + 0.7, y: cy + 0.50, w: cw - 0.7, h: 0.45,
        fontSize: 10, fontFace: "Calibri", italic: true, color: C.textSecondary,
        valign: "middle", margin: 0,
      }
    );
  }

  // Body explainer at the bottom
  sExec.addText(unlockText, {
    x: cx, y: cy + 0.98, w: cw, h: 0.28,
    fontSize: 10, fontFace: "Calibri", color: C.textPrimary, margin: 0,
  });
});

// ── Two-column lower section: Focus areas (left) | Current strengths (right) ──
// Sized to fit within the remaining slide height after the rich tier-narrative
// banner pushes the 3-card hero down. 5 items at 0.35 per row keeps the deck
// to a single slide footprint without truncating the bottom.
const focusY = 3.55;
const colItemH = 0.35;
const colMaxItems = 5;

function drawListItem(slide, item, iy, colX, colW, opts) {
  const pillW = 0.65;
  const pillH = 0.24;
  // Score pill (sized for visibility without crowding rows)
  slide.addShape(pres.shapes.RECTANGLE, {
    x: colX,
    y: iy + 0.05,
    w: pillW,
    h: pillH,
    fill: { color: getScoreColor(item.score) },
  });
  slide.addText(item.score.toFixed(2), {
    x: colX,
    y: iy + 0.05,
    w: pillW,
    h: pillH,
    fontSize: 11,
    fontFace: "Calibri",
    bold: true,
    color: C.bgDark,
    align: "center",
    valign: "middle",
    margin: 0,
  });
  // Criterion name
  slide.addText(item.criterion, {
    x: colX + pillW + 0.13,
    y: iy + 0.02,
    w: colW - pillW - 0.13,
    h: 0.2,
    fontSize: 11,
    fontFace: "Calibri",
    bold: true,
    color: C.textPrimary,
    margin: 0,
  });
  // Subline (target for blockers, category for strengths)
  if (opts.subline) {
    slide.addText(opts.subline, {
      x: colX + pillW + 0.13,
      y: iy + 0.21,
      w: colW - pillW - 0.13,
      h: 0.17,
      fontSize: 9,
      fontFace: "Calibri",
      color: C.textSecondary,
      italic: true,
      margin: 0,
    });
  }
}

// Left column — Focus Areas
const execLeftX = 0.6;
const execColW = 4.3;
const execRightX = execLeftX + execColW + 0.2;

if (exec.blockers.length > 0) {
  sExec.addText(
    `Focus areas — ${exec.nextTierName} criteria to address`,
    {
      x: execLeftX,
      y: focusY,
      w: execColW,
      h: 0.24,
      fontSize: 11,
      fontFace: "Calibri",
      bold: true,
      color: C.textSecondary,
      margin: 0,
    }
  );

  const focusItems = exec.blockers.slice(0, colMaxItems);
  focusItems.forEach((b, i) => {
    const iy = focusY + 0.32 + i * colItemH;
    // Take only the first measurable clause from the rubric's level-3 target so it
    // fits on a single line in the narrower two-column layout.
    const targetSummary = b.target ? b.target.split(";")[0].trim().replace(/\.$/, "") : "";
    drawListItem(sExec, b, iy, execLeftX, execColW, {
      subline: targetSummary ? `Target: ${targetSummary}` : "",
    });
  });
} else {
  sExec.addText(
    `All ${exec.nextTierName} criteria meet the Defined threshold.`,
    {
      x: execLeftX,
      y: focusY + 0.2,
      w: execColW,
      h: 0.6,
      fontSize: 11,
      fontFace: "Calibri",
      color: C.green,
      margin: 0,
    }
  );
}

// Right column — Current Strengths
if (exec.strengths.length > 0) {
  sExec.addText("Current strengths — top performers", {
    x: execRightX,
    y: focusY,
    w: execColW,
    h: 0.24,
    fontSize: 11,
    fontFace: "Calibri",
    bold: true,
    color: C.textSecondary,
    margin: 0,
  });

  const strengthItems = exec.strengths.slice(0, colMaxItems);
  strengthItems.forEach((s, i) => {
    const iy = focusY + 0.32 + i * colItemH;
    drawListItem(sExec, s, iy, execRightX, execColW, {
      subline: s.category,
    });
  });
}

// ================================================================
// SLIDE 3: Tier Progression + KPI Summary
// ================================================================
const s2 = pres.addSlide();
s2.background = { color: C.bgDark };

// Title (decorative section label and cyan top bar removed)
s2.addText("DEBMM Tier Overview", {
  x: 0.6,
  y: 0.25,
  w: 8,
  h: 0.5,
  fontSize: 24,
  fontFace: "Calibri",
  bold: true,
  color: C.white,
  margin: 0,
});

// Explanatory subtitle so the reader knows what they're looking at
s2.addText(
  "Five progressive tiers from Foundation to Expert. A tier is achieved only when every criterion in that tier and below scores at least 3.0 (Defined level).",
  {
    x: 0.6,
    y: 0.78,
    w: 9.2,
    h: 0.36,
    fontSize: 12,
    fontFace: "Calibri",
    italic: true,
    color: C.textSecondary,
    margin: 0,
  }
);

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
    fontSize: 10,
    fontFace: "Calibri",
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
s2.addText("Assessment summary", {
  x: 0.6,
  y: statY,
  w: 8,
  h: 0.25,
  fontSize: 11,
  fontFace: "Calibri",
  bold: true,
  color: C.textSecondary,
  charSpacing: 0,
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
    fontSize: 10,
    fontFace: "Calibri",
    italic: true,
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

// (Removed redundant bottom "TIER PROGRESSION" footer — the top tier cards
// already convey Complete / Current / In Progress per tier.)

// ================================================================
// SLIDE 3: DEBMM Core Criteria Detail
// ================================================================
const s3 = pres.addSlide();
s3.background = { color: C.bgDark };

// Title (decorative section label and cyan top bar removed)
s3.addText("Core Criteria Breakdown", {
  x: 0.6,
  y: 0.25,
  w: 8,
  h: 0.4,
  fontSize: 22,
  fontFace: "Calibri",
  bold: true,
  color: C.white,
  margin: 0,
});

// Explanatory subtitle
s3.addText(
  "All 18 DEBMM core criteria with score, maturity level, and pass/fail. Rows in red are below the 3.0 threshold and prevent tier advancement.",
  {
    x: 0.6,
    y: 0.65,
    w: 9.2,
    h: 0.28,
    fontSize: 11,
    fontFace: "Calibri",
    italic: true,
    color: C.textSecondary,
    margin: 0,
  }
);

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
  s3.addText(lbl, {
    x: colX[i],
    y: tblHeaderY + 0.02,
    w: colW[i],
    h: 0.24,
    fontSize: 10,
    fontFace: "Calibri",
    bold: true,
    color: C.textMuted,
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

// Title (decorative section label and cyan top bar removed)
s4.addText("People, Process & Governance", {
  x: 0.6,
  y: 0.25,
  w: 8,
  h: 0.4,
  fontSize: 22,
  fontFace: "Calibri",
  bold: true,
  color: C.white,
  margin: 0,
});

// Explanatory subtitle
s4.addText(
  "Six organizational dimensions enriching the DEBMM core. These shape what detection-engineering behaviors are possible but do not affect tier determination.",
  {
    x: 0.6,
    y: 0.65,
    w: 9.2,
    h: 0.3,
    fontSize: 11,
    fontFace: "Calibri",
    italic: true,
    color: C.textSecondary,
    margin: 0,
  }
);

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
  s4.addText(c.category, {
    x: cx + 0.2,
    y: cy + 0.1,
    w: enrCardW - 1.2,
    h: 0.18,
    fontSize: 10,
    fontFace: "Calibri",
    italic: true,
    color: C.textMuted,
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
  { label: "Enrichment avg", value: enrAvg.toFixed(2), color: C.cyan },
  { label: "People & Org", value: poAvg.toFixed(2), color: C.green },
  { label: "Process & Gov", value: pgAvg.toFixed(2), color: C.blue },
  {
    label: "All passing",
    value: enrichment.every((c) => c.status.includes("Pass")) ? "Yes" : "No",
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
    fontSize: 11,
    fontFace: "Calibri",
    italic: true,
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
