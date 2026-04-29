# Scoring Methodology

This document explains how the DEBMM Assessment Tool scores organizations and determines maturity tiers.

## Source Frameworks

### Primary: Elastic's DEBMM

The [Detection Engineering Behavior Maturity Model (DEBMM)](https://www.elastic.co/security-labs/elastic-releases-debmm) by Elastic Security Labs provides the core structure:

- **5 Maturity Tiers** (0: Foundation through 4: Expert) representing progressive levels of detection engineering capability
- **18 Core Criteria** across those tiers, each with qualitative behaviors and quantitative thresholds
- **5 Behavior Levels** per criterion (Initial, Repeatable, Defined, Managed, Optimized) loosely aligned with the NIST CSF maturity model

### Enrichment: Detection Engineering Maturity Matrix

[Kyle Bailey's Detection Engineering Maturity Matrix](https://detectionengineering.io/) enriches the DEBMM with dimensions it doesn't deeply cover:

- **People & Organization** (3 criteria): Team structure, skills development, leadership commitment
- **Process & Governance** (3 criteria): Detection lifecycle, metrics/KPIs, cross-team collaboration

These enrichment categories ensure SOC managers get a complete picture beyond just detection content quality.

## Scoring Model

### Question Types and Scoring

All 46 questions are dropdowns — there are no free-text questions:

| Type | Input | Scoring Method |
|------|-------|----------------|
| **Checklist** | Yes/No | Yes maps to a predefined maturity value (typically 3 or 4); No maps to 1 |
| **Scale** | 1–5 integer | Used directly as the maturity score |

### Criterion Score

Each criterion has 1–4 questions. The criterion score is the **arithmetic mean** of all scored questions for that criterion:

```
criterion_score = sum(question_scores) / count(scored_questions)
```

### Tier Score

Each tier score is the **weighted average** of its criteria scores:

```
tier_score = sum(criterion_score * criterion_weight) / sum(criterion_weights)
```

Default weight for all criteria is 1.0. Weights can be adjusted in `rubric.yaml` to reflect organizational priorities (e.g., weighting threat modeling higher for threat-intel-driven teams).

### Overall Score

The overall score is the weighted average across **all** criteria (core + enrichment):

```
overall_score = sum(all_criterion_scores * weights) / sum(all_weights)
```

### Tier Determination

The **achieved tier** is the highest tier where **all** criteria within that tier and all lower tiers score >= 3.0 (Defined level). This enforces the DEBMM's progressive philosophy - you must have solid foundations before claiming higher-tier maturity.

```
Achieved Tier = highest N where:
  for all tiers 0..N:
    for all criteria in tier:
      criterion_score >= 3.0
```

Example:
- If all Tier 0 and Tier 1 criteria are >= 3.0, but one Tier 2 criterion is 2.5 → **Achieved: Tier 1 (Basic)**
- If one Tier 0 criterion is 2.0 → **Achieved: Below Foundation**

Note: Enrichment categories (People & Organization, Process & Governance) contribute to the overall score but do **not** affect tier determination, as they extend beyond the core DEBMM model.

## Scoring Paths

The repo supports four equivalent ways to capture and score answers — see the [README](../README.md) for full command reference. All paths produce the same scoring output:

| Path | Input | When to use |
|------|-------|-------------|
| **Spreadsheet** (default) | `templates/debmm-assessment.xlsx` | Most users — formulas calculate scores live as you fill in answers |
| **YAML CLI** | `templates/response-template.yaml` | CI/CD or version-controlled assessments |
| **From spreadsheet** | filled `.xlsx` → `score.py --from-xlsx` | Score a completed spreadsheet without first extracting data |
| **Printable markdown** | `questionnaire/questionnaire.md` | Pen-and-paper or workshop-style assessments |

## Interpreting Results

### Score Ranges

| Score | Level | Interpretation |
|-------|-------|----------------|
| 1.0-1.4 | Initial | No meaningful capability; needs immediate attention |
| 1.5-2.4 | Repeatable | Ad hoc efforts exist but are inconsistent |
| 2.5-3.4 | Defined | Documented processes exist and are generally followed |
| 3.5-4.4 | Managed | Well-integrated practices with measurable outcomes |
| 4.5-5.0 | Optimized | Continuously improving with automation and advanced capabilities |

### Reading the Report

1. **Start with the achieved tier** — this tells you where the organization solidly stands
2. **Check the overall score** — the weighted average shows general maturity across all dimensions
3. **Review tier scores** — identify which tiers are strong versus weak
4. **Look at enrichment scores** — people and process gaps often block technical progress
5. **Follow the recommendations** — prioritize high-priority items in foundational tiers
6. **Read the Evidence column** — supporting notes provide the qualitative context behind the numbers

### Common Patterns

- **Strong Tier 0, weak Tier 1-2**: Good foundations but struggling with systematic quality improvement
- **Strong technical, weak enrichment**: Technical skills exist but organizational support (people, process) is lacking
- **High scale scores, low checklist scores**: Aspirational self-rating that doesn't match concrete behaviors
- **Uneven within tiers**: Some criteria dramatically higher/lower than peers, suggesting focused investment in specific areas

## Limitations

- Self-reported scores may reflect aspiration rather than reality. Filling out the Evidence column for each answer (required for audits, optional for self-assessments) is the best mitigation
- Checklist Yes/No scoring is coarse; a "Yes" for peer review might mean "sometimes" rather than "always"
- LLM-generated recommendations are non-deterministic and should be validated by a human
- Weights are equal by default and should be tuned to the organization's context
- The enrichment categories are a simplified adaptation of detectionengineering.io's framework

## References

- [Elastic DEBMM Blog Post](https://www.elastic.co/security-labs/elastic-releases-debmm)
- [Detection Engineering Maturity Matrix](https://detectionengineering.io/)
- [Kyle Bailey's GitHub Repository](https://github.com/k-bailey/detection-engineering-maturity-matrix)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
