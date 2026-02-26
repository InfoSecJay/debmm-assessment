# DEBMM Assessment Tool

A practical toolkit for SOC managers to assess their detection engineering team's maturity using [Elastic's Detection Engineering Behavior Maturity Model (DEBMM)](https://www.elastic.co/security-labs/elastic-releases-debmm), enriched with organizational dimensions from [detectionengineering.io](https://detectionengineering.io/).

## What This Is

A structured assessment covering **21 criteria** across **7 categories**:

- **Tier 0 - Foundation**: Rule development, maintenance, roadmaps, threat modeling
- **Tier 1 - Basic**: Baseline rules, ruleset management, telemetry, testing
- **Tier 2 - Intermediate**: False positive reduction, gap analysis, internal validation
- **Tier 3 - Advanced**: False negative triage, external validation, advanced TTP coverage
- **Tier 4 - Expert**: Threat hunting, automation, AI/LLM integration
- **People & Organization** (enrichment): Team structure, training, leadership
- **Process & Governance** (enrichment): Lifecycle, metrics, collaboration

Each criterion is scored on a 1-5 maturity scale (Initial → Optimized).

## Quick Start

### Option 1: Manual Assessment (No Tooling Required)

1. Print or open the questionnaire:
   - Self-assessment: [`questionnaire/questionnaire-self.md`](questionnaire/questionnaire-self.md)
   - Audit-style: [`questionnaire/questionnaire-audit.md`](questionnaire/questionnaire-audit.md)
2. Fill it out using the [`rubric/rubric.md`](rubric/rubric.md) as your scoring guide
3. Tally scores using the [methodology](docs/methodology.md)

### Option 2: Automated Scoring (Python)

```bash
# Install dependencies
pip install -r scorer/requirements.txt

# Copy and fill out the response template
cp templates/response-template.yaml my-assessment.yaml
# Edit my-assessment.yaml with your answers...

# Score it
python scorer/score.py my-assessment.yaml

# Generate a markdown report
python scorer/score.py my-assessment.yaml --report my-report.md

# Output raw JSON
python scorer/score.py my-assessment.yaml --json
```

### Option 3: LLM-Assisted Scoring

Scores text/written answers automatically, identifies inconsistencies, and generates improvement recommendations.

```bash
# Install LLM provider
pip install anthropic  # or: pip install openai

# Set API key
export ANTHROPIC_API_KEY=your-key-here
# or: export OPENAI_API_KEY=your-key-here

# Run with LLM analysis
python scorer/llm_scorer.py my-assessment.yaml --report my-report.md

# Use OpenAI instead
python scorer/llm_scorer.py my-assessment.yaml --provider openai --report my-report.md

# Preview the prompt without calling the API
python scorer/llm_scorer.py my-assessment.yaml --dry-run
```

## Try the Example

Run the scorer against the included example (a realistic mid-maturity org):

```bash
python scorer/score.py templates/example-response.yaml --report example-report.md
```

## Project Structure

```
debmm-assessment/
├── README.md                              # This file
├── LICENSE                                # MIT License
├── rubric/
│   ├── rubric.yaml                        # Machine-readable rubric (21 criteria, 5 levels each)
│   └── rubric.md                          # Human-readable rubric with scoring tables
├── questionnaire/
│   ├── questionnaire.yaml                 # Master questionnaire (55 questions, structured)
│   ├── questionnaire-self.md              # Printable self-assessment version
│   └── questionnaire-audit.md             # Printable audit version (with evidence prompts)
├── scorer/
│   ├── requirements.txt                   # Python dependencies
│   ├── score.py                           # Automated CLI scorer
│   ├── report.py                          # Markdown report generator
│   └── llm_scorer.py                      # LLM-assisted scorer (Anthropic/OpenAI)
├── templates/
│   ├── response-template.yaml             # Blank response template to fill out
│   └── example-response.yaml              # Example: mid-maturity organization
└── docs/
    └── methodology.md                     # Scoring methodology and interpretation guide
```

## How Scoring Works

- **Checklist questions** (yes/no): Yes maps to a maturity level (typically 3-4), No maps to 1
- **Scale questions** (1-5): Used directly as the maturity score
- **Text questions**: Flagged for manual review or scored by LLM

**Tier determination**: Your achieved tier is the highest tier where all criteria (in that tier and below) score >= 3.0 (Defined level). This enforces the progressive nature of the model - you need solid foundations before claiming advanced maturity.

See [docs/methodology.md](docs/methodology.md) for the full scoring methodology.

## Self-Assessment vs. Audit

| Mode | Use When | Questionnaire |
|------|----------|---------------|
| **Self-Assessment** | Manager evaluating their own team | `questionnaire-self.md` |
| **Audit** | Evaluating another team with evidence collection | `questionnaire-audit.md` |

The audit questionnaire includes evidence-request prompts for each question to support objective evaluation.

## Customization

- **Adjust weights**: Edit `weight` values in `rubric.yaml` to emphasize criteria important to your org
- **Add questions**: Add entries to `questionnaire.yaml` mapped to existing criteria
- **Modify rubric**: Edit maturity level descriptions in `rubric.yaml` to match your context

## References

- [Elastic DEBMM](https://www.elastic.co/security-labs/elastic-releases-debmm) - Primary framework
- [Detection Engineering Maturity Matrix](https://detectionengineering.io/) - Enrichment dimensions
- [MITRE ATT&CK](https://attack.mitre.org/) - Threat coverage framework referenced throughout

## License

MIT
