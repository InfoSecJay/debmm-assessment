// Shared visual identity for the DEBMM PowerPoint generators.
// Both generate_report.js (point-in-time deck) and generate_trend.js
// (over-time deck) consume this module so colours, scoring bands, shadow
// treatment, and number formatting stay in lock-step across deliverables.

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

// Tier identity colour — used by tier KPI cards, the maturity stepper,
// and the verdict accent strip on the executive summary.
const tierColors = {
  T0: C.green,
  T1: C.blue,
  T2: C.yellow,
  T3: C.orange,
  T4: C.purple,
};

// Maturity-level identity colour — used for level badges and tier-name
// callouts that reference a specific level (Initial through Optimized).
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

// Score-band colour — semantic, anchored to the 3.0 Defined threshold
// so a reader can read pass/fail off the colour even without the level
// label. Above 3.0 trends green/cyan, below 3.0 trends orange/red.
function getScoreColor(score) {
  if (score >= 4.5) return C.green;
  if (score >= 3.5) return C.cyan;
  if (score >= 3.0) return C.yellow;
  if (score >= 2.0) return C.orange;
  return C.red;
}

// Period-over-period direction colour — used by the trend deck for
// delta indicators on each tier and criterion. Threshold 0.1 keeps
// rounding noise from showing as fake movement.
function getDeltaColor(delta) {
  if (delta > 0.1) return C.green;
  if (delta < -0.1) return C.red;
  return C.textMuted;
}

function getDeltaArrow(delta) {
  if (delta > 0.1) return "▲"; // ▲
  if (delta < -0.1) return "▼"; // ▼
  return "—"; // —
}

function fmtScore(s) {
  return s != null ? s.toFixed(2) : "N/A";
}

function fmtDelta(d) {
  if (d == null) return "N/A";
  const sign = d > 0 ? "+" : "";
  return sign + d.toFixed(2);
}

// pptxgenjs mutates the shadow object on each shape that uses it, so
// callers need a fresh instance every time rather than a shared constant.
const mkShadow = () => ({
  type: "outer",
  blur: 4,
  offset: 2,
  angle: 135,
  color: "000000",
  opacity: 0.3,
});

module.exports = {
  C,
  tierColors,
  levelColors,
  getLevelColor,
  getScoreColor,
  getDeltaColor,
  getDeltaArrow,
  fmtScore,
  fmtDelta,
  mkShadow,
};
