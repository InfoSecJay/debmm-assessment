# DEBMM Audit-Style Assessment Questionnaire

> **Instructions for Auditors**: Use this questionnaire to assess a detection engineering team's maturity. For each question, collect evidence to support the rating. Checklist items should be verified with documentation or demonstration. Scale items should be justified with specific examples. Text items should capture detailed responses for review.

**Organization Under Assessment**: ___________________________
**Auditor Name**: ___________________________
**Auditor Role**: ___________________________
**Date**: ___________________________
**Assessment Scope**: ___________________________

---

## Tier 0: Foundation

### Structured Rule Development

**T0-Q1** Does the assessed team follow a documented methodology for developing detection rules?
- [ ] Yes
- [ ] No

*Evidence required: Request documentation of the rule development process (wiki, runbook, SOP).*

**T0-Q2** Do new detection rules go through peer review before deployment?
- [ ] Yes
- [ ] No

*Evidence required: Show pull request history or review logs demonstrating peer review.*

**T0-Q3** Rate the maturity of the assessed team's rule development process.

| Score | Description |
|-------|-------------|
| [ ] 1 | No structured approach; rules created ad hoc |
| [ ] 2 | Some rules follow a loose process, inconsistently applied |
| [ ] 3 | Defined methodology documented and followed for most rules |
| [ ] 4 | Standardized across team with enforced workflows and quality gates |
| [ ] 5 | Continuous improvement with CI/CD integration and automated validation |

*Evidence required: Walk through a recent rule development from request to deployment.*

### Rule Creation and Maintenance

**T0-Q4** Do the assessed team's detection rules have assigned owners?
- [ ] Yes
- [ ] No

*Evidence required: Show rule metadata or ownership assignments.*

**T0-Q5** What percentage of the assessed team's rules are reviewed on a regular schedule?

| Score | Description |
|-------|-------------|
| [ ] 1 | Less than 50% reviewed annually |
| [ ] 2 | 50-70% reviewed annually |
| [ ] 3 | 70-80% reviewed on schedule |
| [ ] 4 | 80-90% reviewed on schedule with peer review on all changes |
| [ ] 5 | 90-100% reviewed with automated health monitoring |

*Evidence required: Show review logs, last-reviewed dates, or maintenance schedules.*

### Roadmap Documentation

**T0-Q6** Does the assessed team maintain a documented detection engineering roadmap?
- [ ] Yes
- [ ] No

*Evidence required: Request the current roadmap document or backlog.*

**T0-Q7** Rate the maturity of the assessed team's detection roadmap.

| Score | Description |
|-------|-------------|
| [ ] 1 | No roadmap exists; work is entirely reactive |
| [ ] 2 | Informal roadmap or backlog exists but not regularly maintained |
| [ ] 3 | Formal roadmap reviewed quarterly and shared with stakeholders |
| [ ] 4 | Integrated with security strategy; progress tracked with metrics |
| [ ] 5 | Dynamic, continuously updated based on intel, gaps, and risk |

*Evidence required: Show roadmap review cadence and stakeholder communication records.*

### Threat Modeling

**T0-Q8** Does the assessed team perform threat modeling exercises?
- [ ] Yes
- [ ] No

*Evidence required: Request threat modeling outputs or exercise documentation.*

**T0-Q9** How frequently does the assessed team perform threat modeling?

| Score | Description |
|-------|-------------|
| [ ] 1 | Never or not at all |
| [ ] 2 | Less than once per year |
| [ ] 3 | Quarterly with documented results |
| [ ] 4 | Monthly; outputs directly inform detection priorities |
| [ ] 5 | Continuous with real-time threat intelligence integration |

*Evidence required: Show dates and outputs of recent threat modeling exercises.*

**T0-Q10** Describe the assessed team's threat modeling process, including frameworks used, frequency, and how outputs inform detection development.

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

*Evidence required: Request sample threat model output and trace to detection backlog items.*

---

## Tier 1: Basic

### Baseline Rule Creation

**T1-Q1** How many custom baseline detection rules does the assessed team maintain?

| Score | Description |
|-------|-------------|
| [ ] 1 | Fewer than 10 custom rules; mostly vendor defaults |
| [ ] 2 | 10-30 rules covering critical threats |
| [ ] 3 | 30-60 rules with a mix of signature and behavioral detections |
| [ ] 4 | 60-100 rules including behavioral and TTP-focused detections |
| [ ] 5 | 100+ rules with continuous refinement and environment-specific tuning |

*Evidence required: Request a rule inventory or repository listing.*

**T1-Q2** Estimate the assessed team's MITRE ATT&CK technique coverage for priority threat areas.

| Score | Description |
|-------|-------------|
| [ ] 1 | Minimal or unknown coverage |
| [ ] 2 | Less than 30% of priority techniques covered |
| [ ] 3 | 40-60% of priority techniques covered |
| [ ] 4 | 60-80% coverage with behavioral detections |
| [ ] 5 | Over 80% coverage with continuous gap analysis |

*Evidence required: Request ATT&CK coverage mapping or navigator layer export.*

### Ruleset Management and Maintenance

**T1-Q3** Are the assessed team's detection rules stored in version control?
- [ ] Yes
- [ ] No

*Evidence required: View the repository and recent commit history.*

**T1-Q4** Does the assessed team practice detection-as-code with CI/CD pipelines?
- [ ] Yes
- [ ] No

*Evidence required: Review CI/CD pipeline configuration and deployment logs.*

**T1-Q5** Rate the maturity of the assessed team's ruleset management.

| Score | Description |
|-------|-------------|
| [ ] 1 | No formal management; rules live in the SIEM without version control |
| [ ] 2 | Some rules in version control with basic documentation |
| [ ] 3 | Most rules versioned with documentation standards; DaC being adopted |
| [ ] 4 | DaC is standard; CI/CD handles deployment; all documented |
| [ ] 5 | Fully automated lifecycle with CI/CD, testing, and weekly validation |

*Evidence required: Walk through a rule change from commit to deployment.*

### Telemetry Quality

**T1-Q6** Rate the quality and coverage of the assessed team's telemetry.

| Score | Description |
|-------|-------------|
| [ ] 1 | No active management; data sources unassessed |
| [ ] 2 | Some awareness of gaps; basic health checks on critical sources |
| [ ] 3 | Actively monitored; coverage mapped to detection needs; CTI integration starting |
| [ ] 4 | Comprehensive with automated monitoring and CTI enrichment |
| [ ] 5 | Advanced workflows with real-time enrichment and automated gap remediation |

*Evidence required: Review data source inventory and health monitoring dashboards.*

**T1-Q7** Describe the assessed team's telemetry management. How is data quality ensured and coverage gaps identified?

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

*Evidence required: Request data source documentation and quality check procedures.*

### Threat Landscape Review

**T1-Q8** How frequently does the assessed team review the threat landscape?

| Score | Description |
|-------|-------------|
| [ ] 1 | No regular reviews |
| [ ] 2 | Annually or bi-annually |
| [ ] 3 | Quarterly with documented findings updating the roadmap |
| [ ] 4 | Monthly integrated with threat intelligence |
| [ ] 5 | Real-time monitoring with automated intel feeds |

*Evidence required: Show dates and outputs of recent threat landscape reviews.*

### Product Owner Engagement

**T1-Q9** Rate the engagement between the assessed team and product/platform owners.

| Score | Description |
|-------|-------------|
| [ ] 1 | No engagement with product owners |
| [ ] 2 | Occasional ad hoc engagement, reactive to issues |
| [ ] 3 | Regular engagement to communicate needs and provide feedback |
| [ ] 4 | Proactive partnership; detection needs on product roadmaps |
| [ ] 5 | Continuous engagement with joint planning and shared metrics |

*Evidence required: Show meeting notes, feature requests, or communication logs.*

### Release Testing and Validation

**T1-Q10** Does the assessed team test rules before production deployment?
- [ ] Yes
- [ ] No

*Evidence required: Show testing environment and sample test results.*

**T1-Q11** Rate the maturity of the assessed team's release testing.

| Score | Description |
|-------|-------------|
| [ ] 1 | No formal testing before deployment |
| [ ] 2 | Basic manual testing on some rules |
| [ ] 3 | Standardized testing with defined test cases and staging environment |
| [ ] 4 | Comprehensive testing with unit, integration, and emulation validation |
| [ ] 5 | Continuous automated testing in full CI/CD pipeline |

*Evidence required: Walk through a recent rule test from plan to validation.*

---

## Tier 2: Intermediate

### False Positive Tuning and Reduction

**T2-Q1** Does the assessed team track false positive rates per rule?
- [ ] Yes
- [ ] No

*Evidence required: Show FP tracking mechanism or dashboard.*

**T2-Q2** Rate the maturity of the assessed team's FP reduction efforts.

| Score | Description |
|-------|-------------|
| [ ] 1 | Minimal or no tuning; high FP rates accepted |
| [ ] 2 | Some reactive tuning when analysts complain |
| [ ] 3 | Regular tuning cycles with tracked FP rates per rule |
| [ ] 4 | Comprehensive FP management with automated tuning and risk scoring |
| [ ] 5 | Automated dynamic tuning with ML; near-zero unnecessary noise |

*Evidence required: Show FP metrics, tuning logs, and reduction trends.*

**T2-Q3** Describe the assessed team's FP management process, metrics tracked, and reduction achieved.

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

*Evidence required: Request before/after FP metrics and tuning documentation.*

### Gap Analysis and Documentation

**T2-Q4** Does the assessed team perform regular gap analysis against ATT&CK or similar?
- [ ] Yes
- [ ] No

*Evidence required: Request most recent gap analysis output.*

**T2-Q5** Rate the maturity of the assessed team's gap analysis.

| Score | Description |
|-------|-------------|
| [ ] 1 | No gap analysis; coverage gaps unknown |
| [ ] 2 | Some gaps identified informally after incidents |
| [ ] 3 | Regular analysis against frameworks; gaps documented and prioritized |
| [ ] 4 | Comprehensive analysis integrated with threat modeling and risk |
| [ ] 5 | Automated analysis with real-time coverage dashboards |

*Evidence required: Show gap documentation, prioritization, and remediation tracking.*

**T2-Q6** Describe the assessed team's gap analysis process and how gaps are tracked and communicated.

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

*Evidence required: Trace a previously identified gap from discovery to resolution.*

### Internal Testing and Validation

**T2-Q7** Does the assessed team conduct attack emulation/simulation for validation?
- [ ] Yes
- [ ] No

*Evidence required: Show emulation tools, test plans, or exercise reports.*

**T2-Q8** Rate the maturity of the assessed team's internal testing program.

| Score | Description |
|-------|-------------|
| [ ] 1 | No internal testing of detection effectiveness |
| [ ] 2 | Occasional manual testing of high-priority rules |
| [ ] 3 | Regular testing with attack emulation; results documented |
| [ ] 4 | Comprehensive with automated emulation and purple team exercises |
| [ ] 5 | Continuous automated testing with full emulation and regression |

*Evidence required: Request test reports and coverage metrics.*

---

## Tier 3: Advanced

### False Negative Triage

**T3-Q1** Does the assessed team have a process for identifying and triaging false negatives?
- [ ] Yes
- [ ] No

*Evidence required: Show FN triage process documentation.*

**T3-Q2** Rate the assessed team's ability to detect and remediate false negatives.

| Score | Description |
|-------|-------------|
| [ ] 1 | No FN identification; missed detections only found during incidents |
| [ ] 2 | Some FNs identified through post-incident reviews |
| [ ] 3 | Systematic FN identification through regular testing; root causes analyzed |
| [ ] 4 | Comprehensive with automated validation and rapid remediation |
| [ ] 5 | Continuous automated FN detection with real-time validation |

*Evidence required: Show detection trigger rates from validation exercises.*

**T3-Q3** Describe the assessed team's FN identification and remediation process and detection trigger rates.

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

*Evidence required: Request validation test results showing trigger rates.*

### External Validation

**T3-Q4** Does the assessed organization conduct external validation of detections?
- [ ] Yes
- [ ] No

*Evidence required: Request external assessment reports or BAS results.*

**T3-Q5** Rate the maturity of the assessed team's external validation.

| Score | Description |
|-------|-------------|
| [ ] 1 | No external validation of detections |
| [ ] 2 | Annual pentest with some detection assessment |
| [ ] 3 | Regular red team or third-party assessments focused on detection |
| [ ] 4 | Multiple annual exercises (red/purple team, breach simulation) |
| [ ] 5 | Continuous BAS tools and regular adversary emulation |

*Evidence required: Show exercise schedule, findings, and remediation tracking.*

### Advanced TTP Coverage

**T3-Q6** Rate the assessed team's coverage of advanced TTPs.

| Score | Description |
|-------|-------------|
| [ ] 1 | No advanced TTP coverage; signatures and IOCs only |
| [ ] 2 | Limited coverage of 1-3 advanced techniques |
| [ ] 3 | Growing coverage informed by intel; behavioral detections in place |
| [ ] 4 | Comprehensive coverage of evasion, novel attack chains, emerging threats |
| [ ] 5 | Continuous proactive coverage using AI/ML for anomaly detection |

*Evidence required: Request advanced TTP detection inventory with technique mappings.*

**T3-Q7** Describe the assessed team's advanced TTP detection capabilities and specific techniques covered.

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

*Evidence required: Review specific detection rules targeting advanced TTPs.*

---

## Tier 4: Expert

### Threat Hunting

**T4-Q1** Does the assessed team conduct proactive threat hunting?
- [ ] Yes
- [ ] No

*Evidence required: Show hunting program documentation or hypothesis log.*

**T4-Q2** Rate the maturity of the assessed team's threat hunting.

| Score | Description |
|-------|-------------|
| [ ] 1 | No proactive hunting; all detection is passive |
| [ ] 2 | Occasional ad hoc hunting; findings not systematically converted |
| [ ] 3 | Regular structured hunting driven by intelligence; findings feed detections |
| [ ] 4 | Comprehensive daily program with advanced analytics and integration |
| [ ] 5 | Automated real-time hunting augmented by AI/ML |

*Evidence required: Show hunting cadence, hypothesis log, and finding integration.*

**T4-Q3** Describe the assessed team's hunting program, hypothesis process, and finding integration.

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

*Evidence required: Trace a hunting finding from hypothesis to detection rule.*

### Automation and Continuous Improvement

**T4-Q4** What percentage of the assessed team's DE tasks are automated?

| Score | Description |
|-------|-------------|
| [ ] 1 | None; all processes are manual |
| [ ] 2 | Less than 30% (basic deployment scripts) |
| [ ] 3 | 40-60% (lifecycle automation; improvement metrics tracked) |
| [ ] 4 | 70-80% (advanced automation; AI/LLM tools in use) |
| [ ] 5 | Over 90% (full AI/LLM lifecycle integration) |

*Evidence required: Inventory automated vs. manual processes.*

**T4-Q5** Does the assessed team use AI/LLM tools for detection work?
- [ ] Yes
- [ ] No

*Evidence required: Show AI/LLM tools in use and their output.*

**T4-Q6** Describe the assessed team's automation and AI/LLM integration, tools used, and results.

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

*Evidence required: Demonstrate automation in action and show measurable results.*

---

## Enrichment: People & Organization

### Team Structure

**EP-Q1** Rate the maturity of the assessed detection engineering team structure.

| Score | Description |
|-------|-------------|
| [ ] 1 | No dedicated roles; detection is a side task for other staff |
| [ ] 2 | Part-time detection responsibilities; no formal team |
| [ ] 3 | Dedicated role(s) or team with clear responsibilities |
| [ ] 4 | Established team with domain experts (host, network, cloud, app) |
| [ ] 5 | Mature team with specialization, mentorship, and strategic influence |

*Evidence required: Review org chart, job descriptions, and team composition.*

**EP-Q2** Does the assessed organization have at least one dedicated detection engineer?
- [ ] Yes
- [ ] No

*Evidence required: Verify role title and job description.*

### Skills Development

**EP-Q3** Rate the maturity of the assessed team's skills development.

| Score | Description |
|-------|-------------|
| [ ] 1 | No formal training; self-directed learning only |
| [ ] 2 | Ad hoc training; no structured program |
| [ ] 3 | Defined training program with regular knowledge sharing |
| [ ] 4 | Comprehensive training with cross-training and certifications |
| [ ] 5 | Continuous learning culture with community contribution and research |

*Evidence required: Show training records, programs, or development plans.*

**EP-Q4** Does the assessed team have a defined training plan or skills roadmap?
- [ ] Yes
- [ ] No

*Evidence required: Request the training plan or skills matrix.*

### Leadership Commitment

**EP-Q5** Rate the executive sponsorship of the assessed detection engineering function.

| Score | Description |
|-------|-------------|
| [ ] 1 | No executive awareness or sponsorship |
| [ ] 2 | Some awareness but no formal sponsorship or budget |
| [ ] 3 | Executive sponsor; dedicated budget; function formally recognized |
| [ ] 4 | Strong support; metrics reported to leadership; influences investments |
| [ ] 5 | Strategic priority; board-level visibility; cross-org influence |

*Evidence required: Show budget allocation, executive communications, or strategy docs.*

**EP-Q6** Does the assessed detection engineering function have a dedicated budget?
- [ ] Yes
- [ ] No

*Evidence required: Verify budget line item.*

**EP-Q7** Describe executive engagement with the assessed detection engineering function.

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

*Evidence required: Show executive-facing reports and communication records.*

---

## Enrichment: Process & Governance

### Detection Lifecycle

**EG-Q1** Rate the maturity of the assessed team's detection lifecycle workflow.

| Score | Description |
|-------|-------------|
| [ ] 1 | No defined lifecycle; no structured workflow |
| [ ] 2 | Basic lifecycle covering creation and deployment only |
| [ ] 3 | Full lifecycle: request, development, review, testing, deploy, monitor, retire |
| [ ] 4 | Enforced through tooling; SLAs defined; cycle time tracked |
| [ ] 5 | Optimized with automated transitions and predictive analytics |

*Evidence required: Walk through the lifecycle stages with examples.*

**EG-Q2** Does the assessed team have a rule retirement/deprecation process?
- [ ] Yes
- [ ] No

*Evidence required: Show retired rule examples and process documentation.*

### Metrics and KPI Tracking

**EG-Q3** Does the assessed team track detection engineering KPIs?
- [ ] Yes
- [ ] No

*Evidence required: Show KPI definitions and reporting cadence.*

**EG-Q4** Rate the maturity of the assessed team's metrics program.

| Score | Description |
|-------|-------------|
| [ ] 1 | No metrics tracked; success is anecdotal |
| [ ] 2 | Basic metrics tracked informally (rule count, alert volume) |
| [ ] 3 | Defined KPIs for coverage, quality, velocity; quarterly reporting |
| [ ] 4 | Comprehensive program with automated collection; metrics drive decisions |
| [ ] 5 | Advanced analytics with predictive metrics and benchmarking |

*Evidence required: Show dashboards, reports, or metrics presentations.*

**EG-Q5** List the KPIs tracked by the assessed team and describe collection and reporting.

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

*Evidence required: Request recent metrics reports with historical trending.*

### Cross-Team Collaboration

**EG-Q6** Rate cross-team collaboration involving the assessed detection engineering function.

| Score | Description |
|-------|-------------|
| [ ] 1 | Operates in isolation; no structured collaboration |
| [ ] 2 | Ad hoc collaboration, reactive to incidents |
| [ ] 3 | Regular collaboration via defined channels and scheduled touchpoints |
| [ ] 4 | Deep integration with joint planning and shared objectives |
| [ ] 5 | Seamless cross-functional collaboration with automated information sharing |

*Evidence required: Show meeting schedules, shared channels, or joint planning docs.*

**EG-Q7** Does the assessed team have regular touchpoints with IR and threat intel?
- [ ] Yes
- [ ] No

*Evidence required: Show meeting invites, notes, or collaboration channel activity.*

---

## Auditor Notes

### Overall Observations
> _________________________________________________________________________
> _________________________________________________________________________

### Key Strengths Identified
> _________________________________________________________________________
> _________________________________________________________________________

### Primary Gaps and Recommendations
> _________________________________________________________________________
> _________________________________________________________________________

### Evidence Quality Assessment
- [ ] Strong evidence provided across most areas
- [ ] Moderate evidence; some areas rely on verbal claims
- [ ] Limited evidence; many ratings based on self-reporting without verification

---

*Assessment complete. See [scoring methodology](../docs/methodology.md) for how to interpret results.*
