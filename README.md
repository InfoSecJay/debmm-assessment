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

## Quick Start

### 1. Install Dependencies

```bash
pip install -r scorer/requirements.txt
npm install
```

### 2. Generate the Assessment Spreadsheet

```bash
# Self-assessment mode (default)
python scorer/generate_spreadsheet.py

# Audit mode (includes evidence prompts)
python scorer/generate_spreadsheet.py --mode audit -o templates/debmm-assessment-audit.xlsx
```

### 3. Fill Out the Assessment

Open the generated spreadsheet in Excel:

1. **Instructions** — Read the overview and maturity level definitions
2. **Assessment** — Fill in org details and answer all 41 questions using dropdowns
3. **Results Dashboard** — Scores calculate automatically with tier determination and color-coded heatmap
4. **Tier Scores Chart** — DEBMM core tier bar chart
5. **Readiness Chart** — Organizational readiness bar chart
6. **Rubric Reference** — Full rubric for reference while answering
7. **Report Data** — Flat data export for Power BI or report generation

**Save the file in Excel** after completing the assessment (this evaluates all formulas).

### 4. Generate a PowerPoint Report

Extract data from the completed spreadsheet, then generate the report:

```bash
# Extract assessment data to JSON
python scorer/extract_data.py my-assessment.xlsx -o data.json

# Generate 4-slide PowerPoint report
node scorer/generate_report.js data.json my-report.pptx
```

This produces a dark-themed, exec-ready 4-slide deck:
- **Slide 1**: Title slide with overall score, achieved tier, completion, pass/fail summary
- **Slide 2**: Tier progression overview with KPI cards and status indicators
- **Slide 3**: DEBMM core criteria breakdown with scores, levels, and score bars
- **Slide 4**: Enrichment criteria cards with category summaries

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
│   ├── generate_report.js                # Generates PowerPoint report from JSON
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
