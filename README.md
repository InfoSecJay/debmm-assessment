# DEBMM Assessment Tool

A practical toolkit for SOC managers to assess their detection engineering team's maturity using [Elastic's Detection Engineering Behavior Maturity Model (DEBMM)](https://www.elastic.co/security-labs/elastic-releases-debmm), enriched with organizational dimensions from [detectionengineering.io](https://detectionengineering.io/).

## What This Is

A structured assessment covering **24 criteria** across **7 categories** with **41 dropdown questions** (no free-text required):

- **Tier 0 - Foundation**: Rule development, maintenance, roadmaps, threat modeling
- **Tier 1 - Basic**: Baseline rules, ruleset management, telemetry, testing
- **Tier 2 - Intermediate**: False positive reduction, gap analysis, internal validation
- **Tier 3 - Advanced**: False negative triage, external validation, advanced TTP coverage
- **Tier 4 - Expert**: Threat hunting, automation, AI/LLM integration
- **People & Organization** (enrichment): Team structure, training, leadership
- **Process & Governance** (enrichment): Lifecycle, metrics, collaboration

Each criterion is scored on a 1-5 maturity scale (Initial → Optimized). Your **achieved tier** is the highest tier where all criteria (in that tier and all below) score >= 3.0 — enforcing the progressive nature of the model.

## Prerequisites

- **Python 3.10+** with pip
- **Node.js 18+** with npm (for PowerPoint report generation)
- **Microsoft Excel** or compatible spreadsheet app (for filling out assessments)

## Quick Start — One-Time Setup

### 1. Fork and Clone

Fork this repo for your organization, then clone it:

```bash
git clone https://github.com/<your-org>/debmm-assessment.git
cd debmm-assessment
```

### 2. Install Dependencies

```bash
pip install -r scorer/requirements.txt
npm install
```

### 3. Generate the Assessment Spreadsheet

```bash
# Self-assessment mode (default)
python scorer/generate_spreadsheet.py

# Audit mode (includes evidence prompts)
python scorer/generate_spreadsheet.py --mode audit -o templates/debmm-assessment-audit.xlsx
```

This creates the spreadsheet in `templates/`. You only need to regenerate it if you modify the rubric or questionnaire YAML files.

## Monthly Workflow

### First Assessment

#### 1. Fill Out the Assessment

Open `templates/debmm-assessment.xlsx` in Excel. The spreadsheet has 7 tabs:

1. **Instructions** — Overview and maturity level definitions
2. **Assessment** — Fill in org details and answer all 41 questions using dropdowns
3. **Results Dashboard** — Scores calculate automatically with tier determination and color-coded heatmap
4. **Tier Scores Chart** — DEBMM core tier bar chart
5. **Readiness Chart** — Organizational readiness bar chart
6. **Rubric Reference** — Full rubric for reference while answering
7. **Report Data** — Flat data export for Power BI or report generation

**Save the file in Excel** after completing the assessment (this evaluates all formulas).

#### 2. Extract Data and Build History

```bash
python scorer/extract_data.py templates/debmm-assessment.xlsx -o data.json --history history.json
```

This does two things:
- Writes `data.json` — the current assessment snapshot (for the point-in-time report)
- Creates/updates `history.json` — appends this assessment to the history file (for trend reporting)

The date period is automatically derived from the spreadsheet's Date field. To override:

```bash
python scorer/extract_data.py templates/debmm-assessment.xlsx -o data.json --history history.json --date 2026-01
```

#### 3. Generate Reports

**Point-in-time report** (4-slide exec deck):

```bash
node scorer/generate_report.js data.json reports/2026-01-report.pptx
```

Produces a dark-themed, exec-ready 4-slide deck:
- **Slide 1**: Title slide with overall score, achieved tier, completion, pass/fail summary
- **Slide 2**: Tier progression overview with KPI cards and status indicators
- **Slide 3**: DEBMM core criteria breakdown with scores, levels, and score bars
- **Slide 4**: Enrichment criteria cards with category summaries

**Trend report** (3-slide trend deck — available with 1+ assessments):

```bash
node scorer/generate_trend.js history.json reports/2026-01-trend.pptx
```

With a single assessment, this shows a "Baseline Established" card with current state. After 2+ assessments, it generates full trend analysis:
- **Slide 1**: Score trajectory line chart with 3.0 threshold and tier achievement badges
- **Slide 2**: Per-tier score trends with delta indicators and sparkline history
- **Slide 3**: Biggest improvements and areas needing attention

### Recurring Monthly Updates

Each month, repeat the process:

```bash
# 1. Open the spreadsheet, update answers, save in Excel

# 2. Extract and append to history
python scorer/extract_data.py templates/debmm-assessment.xlsx -o data.json --history history.json

# 3. Generate both reports
node scorer/generate_report.js data.json reports/2026-02-report.pptx
node scorer/generate_trend.js history.json reports/2026-02-trend.pptx
```

The extract step automatically detects the date from the spreadsheet and upserts the entry in `history.json` — if the same month already exists, it replaces it.

## Handling Common Scenarios

| Scenario | What to Do |
|----------|------------|
| **Missed a month** | No action needed. The trend chart shows actual assessment dates with gaps — no interpolation. |
| **Re-run mid-month** | Just re-extract. The `--history` flag upserts by date, so the existing entry for that month is replaced. |
| **Retroactive entry** | Use `--date YYYY-MM` to override the period: `python scorer/extract_data.py ... --history history.json --date 2025-12` |
| **Assessor changes** | The trend report automatically detects assessor changes and flags them with a warning on Slide 2. |
| **Changed criteria/rubric** | Only criteria present in both the latest and previous period are compared. New or removed criteria are handled gracefully. |

## Alternative Scoring Methods

### YAML + Python CLI

For technical users or CI/CD integration:

```bash
# Copy and fill out the response template
cp templates/response-template.yaml my-assessment.yaml
# Edit my-assessment.yaml with your answers...

# Score it (rich terminal output)
python scorer/score.py my-assessment.yaml

# Generate a markdown report
python scorer/score.py my-assessment.yaml --report my-report.md

# Output raw JSON
python scorer/score.py my-assessment.yaml --json
```

### Score from a Filled-Out Spreadsheet

```bash
python scorer/score.py --from-xlsx my-filled-assessment.xlsx --report my-report.md
```

### LLM-Assisted Scoring

Scores text answers automatically, identifies inconsistencies, and generates improvement recommendations:

```bash
pip install anthropic  # or: pip install openai
export ANTHROPIC_API_KEY=your-key-here

python scorer/llm_scorer.py my-assessment.yaml --report my-report.md
```

### Printable Markdown (No Tooling)

For pen-and-paper or workshop-style assessments:

1. Open [`questionnaire/questionnaire-self.md`](questionnaire/questionnaire-self.md) or [`questionnaire/questionnaire-audit.md`](questionnaire/questionnaire-audit.md)
2. Score using [`rubric/rubric.md`](rubric/rubric.md)
3. Tally scores using the [methodology](docs/methodology.md)

## CLI Reference

### `scorer/generate_spreadsheet.py`

```
python scorer/generate_spreadsheet.py [--mode {self,audit}] [-o OUTPUT]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--mode` | `self` | Assessment mode: `self` or `audit` (adds evidence prompts) |
| `-o` | `templates/debmm-assessment.xlsx` | Output path for generated spreadsheet |

### `scorer/extract_data.py`

```
python scorer/extract_data.py <xlsx> [-o OUTPUT] [--history HISTORY] [--date YYYY-MM]
```

| Flag | Default | Description |
|------|---------|-------------|
| `<xlsx>` | *(required)* | Path to completed assessment spreadsheet |
| `-o` | `<input>_data.json` | Output path for extracted JSON |
| `--history` | *(none)* | Path to history file — appends/upserts this assessment |
| `--date` | *(auto)* | Override period (YYYY-MM). Default: from spreadsheet date or current month |

### `scorer/generate_report.js`

```
node scorer/generate_report.js <data.json> [output.pptx]
```

Generates a 4-slide point-in-time assessment report from a single extract.

### `scorer/generate_trend.js`

```
node scorer/generate_trend.js <history.json> [output.pptx]
```

Generates a 3-slide trend report from the history file. Works with 1+ entries (baseline mode with 1, full trends with 2+).

### `scorer/score.py`

```
python scorer/score.py <assessment.yaml> [--report OUTPUT.md] [--json] [--from-xlsx FILE]
```

CLI scorer with rich terminal output, markdown reports, or raw JSON.

## Project Structure

```
debmm-assessment/
├── README.md
├── LICENSE
├── package.json                          # Node.js dependencies (pptxgenjs)
├── rubric/
│   ├── rubric.yaml                       # Machine-readable rubric (24 criteria, 5 levels each)
│   └── rubric.md                         # Human-readable rubric with scoring tables
├── questionnaire/
│   ├── questionnaire.yaml                # Master questionnaire (41 questions, structured)
│   ├── questionnaire-self.md             # Printable self-assessment version
│   └── questionnaire-audit.md            # Printable audit version (with evidence prompts)
├── scorer/
│   ├── requirements.txt                  # Python dependencies
│   ├── generate_spreadsheet.py           # Generates the all-in-one Excel assessment
│   ├── extract_data.py                   # Extracts assessment data from xlsx to JSON
│   ├── generate_report.js                # Generates 4-slide PowerPoint report from JSON
│   ├── generate_trend.js                 # Generates 3-slide trend report from history
│   ├── score.py                          # Automated CLI scorer (YAML or Excel input)
│   ├── report.py                         # Markdown report generator
│   └── llm_scorer.py                     # LLM-assisted scorer (Anthropic/OpenAI)
├── templates/
│   ├── debmm-assessment.xlsx             # Generated self-assessment spreadsheet
│   ├── debmm-assessment-audit.xlsx       # Generated audit spreadsheet
│   ├── response-template.yaml            # Blank YAML response template
│   └── example-response.yaml             # Example: mid-maturity organization
└── docs/
    └── methodology.md                    # Scoring methodology and interpretation guide
```

## How Scoring Works

- **Scale questions** (1-5): Each dropdown option maps directly to a maturity score with quantitative thresholds from the rubric
- **Checklist questions** (yes/no): Yes maps to a maturity level (typically 3-4), No maps to 1

**Tier determination**: Your achieved tier is the highest tier where **all** criteria (in that tier and all below) score >= 3.0 (Defined level). A single criterion below 3.0 anywhere in the chain caps your tier — this enforces the progressive nature of the model.

See [docs/methodology.md](docs/methodology.md) for the full scoring methodology.

## Self-Assessment vs. Audit

| Mode | Use When | Command |
|------|----------|---------|
| **Self-Assessment** | Manager evaluating their own team | `python scorer/generate_spreadsheet.py` |
| **Audit** | Evaluating another team with evidence collection | `python scorer/generate_spreadsheet.py --mode audit -o templates/debmm-assessment-audit.xlsx` |

The audit version includes evidence-request prompts for each question to support objective evaluation.

## Customization

- **Adjust weights**: Edit `weight` values in `rubric.yaml` to emphasize criteria important to your org
- **Add questions**: Add entries to `questionnaire.yaml` mapped to existing criteria
- **Modify rubric**: Edit maturity level descriptions in `rubric.yaml` to match your context
- **Regenerate spreadsheet**: After editing YAML sources, re-run `generate_spreadsheet.py`

## References

- [Elastic DEBMM](https://www.elastic.co/security-labs/elastic-releases-debmm) - Primary framework
- [Detection Engineering Maturity Matrix](https://detectionengineering.io/) - Enrichment dimensions
- [MITRE ATT&CK](https://attack.mitre.org/) - Threat coverage framework referenced throughout

## License

MIT
