# DEBMM Self-Assessment Questionnaire

> **Instructions**: Complete this questionnaire to assess your detection engineering team's maturity. For checklist items, mark Yes or No. For scale items, circle the number that best describes your team. For text items, provide a written response.

**Organization**: ___________________________
**Assessor**: ___________________________
**Date**: ___________________________

---

## Tier 0: Foundation

### Structured Rule Development

**T0-Q1** Does your team follow a documented methodology for developing detection rules?
- [ ] Yes
- [ ] No

**T0-Q2** Do new detection rules go through peer review before deployment?
- [ ] Yes
- [ ] No

**T0-Q3** Rate the maturity of your rule development process.

| Score | Description |
|-------|-------------|
| [ ] 1 | No structured approach; rules created ad hoc |
| [ ] 2 | Some rules follow a loose process, inconsistently applied |
| [ ] 3 | Defined methodology documented and followed for most rules |
| [ ] 4 | Standardized across team with enforced workflows and quality gates |
| [ ] 5 | Continuous improvement with CI/CD integration and automated validation |

### Rule Creation and Maintenance

**T0-Q4** Do your detection rules have assigned owners responsible for their maintenance?
- [ ] Yes
- [ ] No

**T0-Q5** What percentage of your detection rules are reviewed on a regular schedule?

| Score | Description |
|-------|-------------|
| [ ] 1 | Less than 50% reviewed annually |
| [ ] 2 | 50-70% reviewed annually |
| [ ] 3 | 70-80% reviewed on schedule |
| [ ] 4 | 80-90% reviewed on schedule with peer review on all changes |
| [ ] 5 | 90-100% reviewed with automated health monitoring |

### Roadmap Documentation

**T0-Q6** Does your team maintain a documented detection engineering roadmap?
- [ ] Yes
- [ ] No

**T0-Q7** Rate the maturity of your detection engineering roadmap.

| Score | Description |
|-------|-------------|
| [ ] 1 | No roadmap exists; work is entirely reactive |
| [ ] 2 | Informal roadmap or backlog exists but not regularly maintained |
| [ ] 3 | Formal roadmap reviewed quarterly and shared with stakeholders |
| [ ] 4 | Integrated with security strategy; progress tracked with metrics |
| [ ] 5 | Dynamic, continuously updated based on intel, gaps, and risk |

### Threat Modeling

**T0-Q8** Does your team perform threat modeling exercises to inform detection priorities?
- [ ] Yes
- [ ] No

**T0-Q9** How frequently does your team perform threat modeling?

| Score | Description |
|-------|-------------|
| [ ] 1 | Never or not at all |
| [ ] 2 | Less than once per year |
| [ ] 3 | Quarterly with documented results |
| [ ] 4 | Monthly; outputs directly inform detection priorities |
| [ ] 5 | Continuous with real-time threat intelligence integration |

**T0-Q10** Describe your threat modeling process, including frameworks used, frequency, and how outputs inform detection development.

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

---

## Tier 1: Basic

### Baseline Rule Creation

**T1-Q1** How many custom baseline detection rules does your team maintain?

| Score | Description |
|-------|-------------|
| [ ] 1 | Fewer than 10 custom rules; mostly vendor defaults |
| [ ] 2 | 10-30 rules covering critical threats |
| [ ] 3 | 30-60 rules with a mix of signature and behavioral detections |
| [ ] 4 | 60-100 rules including behavioral and TTP-focused detections |
| [ ] 5 | 100+ rules with continuous refinement and environment-specific tuning |

**T1-Q2** Estimate your MITRE ATT&CK technique coverage for your priority threat areas.

| Score | Description |
|-------|-------------|
| [ ] 1 | Minimal or unknown coverage |
| [ ] 2 | Less than 30% of priority techniques covered |
| [ ] 3 | 40-60% of priority techniques covered |
| [ ] 4 | 60-80% coverage with behavioral detections |
| [ ] 5 | Over 80% coverage with continuous gap analysis |

### Ruleset Management and Maintenance

**T1-Q3** Are your detection rules stored in a version control system (e.g., Git)?
- [ ] Yes
- [ ] No

**T1-Q4** Does your team practice detection-as-code with CI/CD pipelines for rule deployment?
- [ ] Yes
- [ ] No

**T1-Q5** Rate the maturity of your ruleset management and maintenance practices.

| Score | Description |
|-------|-------------|
| [ ] 1 | No formal management; rules live in the SIEM without version control |
| [ ] 2 | Some rules in version control with basic documentation |
| [ ] 3 | Most rules versioned with documentation standards; DaC being adopted |
| [ ] 4 | DaC is standard; CI/CD handles deployment; all documented |
| [ ] 5 | Fully automated lifecycle with CI/CD, testing, and weekly validation |

### Telemetry Quality

**T1-Q6** Rate the quality and coverage of your telemetry data sources.

| Score | Description |
|-------|-------------|
| [ ] 1 | No active management; data sources unassessed |
| [ ] 2 | Some awareness of gaps; basic health checks on critical sources |
| [ ] 3 | Actively monitored; coverage mapped to detection needs; CTI integration starting |
| [ ] 4 | Comprehensive with automated monitoring and CTI enrichment |
| [ ] 5 | Advanced workflows with real-time enrichment and automated gap remediation |

**T1-Q7** Describe your telemetry management practices. How do you ensure data quality and identify coverage gaps?

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

### Threat Landscape Review

**T1-Q8** How frequently does your team review the threat landscape to update detection priorities?

| Score | Description |
|-------|-------------|
| [ ] 1 | No regular reviews |
| [ ] 2 | Annually or bi-annually |
| [ ] 3 | Quarterly with documented findings updating the roadmap |
| [ ] 4 | Monthly integrated with threat intelligence |
| [ ] 5 | Real-time monitoring with automated intel feeds |

### Product Owner Engagement

**T1-Q9** Rate the level of engagement between your detection engineering team and security product/platform owners.

| Score | Description |
|-------|-------------|
| [ ] 1 | No engagement with product owners |
| [ ] 2 | Occasional ad hoc engagement, reactive to issues |
| [ ] 3 | Regular engagement to communicate needs and provide feedback |
| [ ] 4 | Proactive partnership; detection needs on product roadmaps |
| [ ] 5 | Continuous engagement with joint planning and shared metrics |

### Release Testing and Validation

**T1-Q10** Does your team test detection rules before deploying them to production?
- [ ] Yes
- [ ] No

**T1-Q11** Rate the maturity of your release testing and validation process.

| Score | Description |
|-------|-------------|
| [ ] 1 | No formal testing before deployment |
| [ ] 2 | Basic manual testing on some rules |
| [ ] 3 | Standardized testing with defined test cases and staging environment |
| [ ] 4 | Comprehensive testing with unit, integration, and emulation validation |
| [ ] 5 | Continuous automated testing in full CI/CD pipeline |

---

## Tier 2: Intermediate

### False Positive Tuning and Reduction

**T2-Q1** Does your team track false positive rates per detection rule?
- [ ] Yes
- [ ] No

**T2-Q2** Rate the maturity of your false positive tuning and reduction efforts.

| Score | Description |
|-------|-------------|
| [ ] 1 | Minimal or no tuning; high FP rates accepted |
| [ ] 2 | Some reactive tuning when analysts complain |
| [ ] 3 | Regular tuning cycles with tracked FP rates per rule |
| [ ] 4 | Comprehensive FP management with automated tuning and risk scoring |
| [ ] 5 | Automated dynamic tuning with ML; near-zero unnecessary noise |

**T2-Q3** Describe your false positive management process. What metrics do you track and what reduction have you achieved?

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

### Gap Analysis and Documentation

**T2-Q4** Does your team perform regular gap analysis against frameworks like MITRE ATT&CK?
- [ ] Yes
- [ ] No

**T2-Q5** Rate the maturity of your detection coverage gap analysis.

| Score | Description |
|-------|-------------|
| [ ] 1 | No gap analysis; coverage gaps unknown |
| [ ] 2 | Some gaps identified informally after incidents |
| [ ] 3 | Regular analysis against frameworks; gaps documented and prioritized |
| [ ] 4 | Comprehensive analysis integrated with threat modeling and risk |
| [ ] 5 | Automated analysis with real-time coverage dashboards |

**T2-Q6** Describe your gap analysis process. How are gaps identified, documented, prioritized, and communicated?

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

### Internal Testing and Validation

**T2-Q7** Does your team conduct attack emulation or simulation to validate detection rules?
- [ ] Yes
- [ ] No

**T2-Q8** Rate the maturity of your internal detection testing and validation program.

| Score | Description |
|-------|-------------|
| [ ] 1 | No internal testing of detection effectiveness |
| [ ] 2 | Occasional manual testing of high-priority rules |
| [ ] 3 | Regular testing with attack emulation; results documented |
| [ ] 4 | Comprehensive with automated emulation and purple team exercises |
| [ ] 5 | Continuous automated testing with full emulation and regression |

---

## Tier 3: Advanced

### False Negative Triage

**T3-Q1** Does your team have a process for identifying and triaging false negatives (missed detections)?
- [ ] Yes
- [ ] No

**T3-Q2** Rate your team's ability to detect and remediate false negatives.

| Score | Description |
|-------|-------------|
| [ ] 1 | No FN identification; missed detections only found during incidents |
| [ ] 2 | Some FNs identified through post-incident reviews |
| [ ] 3 | Systematic FN identification through regular testing; root causes analyzed |
| [ ] 4 | Comprehensive with automated validation and rapid remediation |
| [ ] 5 | Continuous automated FN detection with real-time validation |

**T3-Q3** Describe how your team identifies, tracks, and remediates false negatives. What is your detection trigger rate on tested samples?

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

### External Validation

**T3-Q4** Does your organization conduct external validation of detection capabilities (red team, pentest, BAS)?
- [ ] Yes
- [ ] No

**T3-Q5** Rate the maturity of your external validation program.

| Score | Description |
|-------|-------------|
| [ ] 1 | No external validation of detections |
| [ ] 2 | Annual pentest with some detection assessment |
| [ ] 3 | Regular red team or third-party assessments focused on detection |
| [ ] 4 | Multiple annual exercises (red/purple team, breach simulation) |
| [ ] 5 | Continuous BAS tools and regular adversary emulation |

### Advanced TTP Coverage

**T3-Q6** Rate your detection coverage of advanced TTPs (living-off-the-land, fileless, evasion techniques).

| Score | Description |
|-------|-------------|
| [ ] 1 | No advanced TTP coverage; signatures and IOCs only |
| [ ] 2 | Limited coverage of 1-3 advanced techniques |
| [ ] 3 | Growing coverage informed by intel; behavioral detections in place |
| [ ] 4 | Comprehensive coverage of evasion, novel attack chains, emerging threats |
| [ ] 5 | Continuous proactive coverage using AI/ML for anomaly detection |

**T3-Q7** Describe your advanced TTP detection capabilities. What specific advanced techniques do you detect and how?

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

---

## Tier 4: Expert

### Threat Hunting

**T4-Q1** Does your team conduct proactive threat hunting activities?
- [ ] Yes
- [ ] No

**T4-Q2** Rate the maturity of your threat hunting program.

| Score | Description |
|-------|-------------|
| [ ] 1 | No proactive hunting; all detection is passive |
| [ ] 2 | Occasional ad hoc hunting; findings not systematically converted |
| [ ] 3 | Regular structured hunting driven by intelligence; findings feed detections |
| [ ] 4 | Comprehensive daily program with advanced analytics and integration |
| [ ] 5 | Automated real-time hunting augmented by AI/ML |

**T4-Q3** Describe your threat hunting program. How often do you hunt, what drives your hypotheses, and how are findings integrated into detections?

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

### Automation and Continuous Improvement

**T4-Q4** What percentage of your detection engineering tasks are automated?

| Score | Description |
|-------|-------------|
| [ ] 1 | None; all processes are manual |
| [ ] 2 | Less than 30% (basic deployment scripts) |
| [ ] 3 | 40-60% (lifecycle automation; improvement metrics tracked) |
| [ ] 4 | 70-80% (advanced automation; AI/LLM tools in use) |
| [ ] 5 | Over 90% (full AI/LLM lifecycle integration) |

**T4-Q5** Does your team use AI or LLM tools to assist with detection rule development, tuning, or analysis?
- [ ] Yes
- [ ] No

**T4-Q6** Describe your automation and AI/LLM integration in the detection engineering lifecycle. What tools do you use and what results have you achieved?

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

---

## Enrichment: People & Organization

### Team Structure

**EP-Q1** Rate the maturity of your detection engineering team structure.

| Score | Description |
|-------|-------------|
| [ ] 1 | No dedicated roles; detection is a side task for other staff |
| [ ] 2 | Part-time detection responsibilities; no formal team |
| [ ] 3 | Dedicated role(s) or team with clear responsibilities |
| [ ] 4 | Established team with domain experts (host, network, cloud, app) |
| [ ] 5 | Mature team with specialization, mentorship, and strategic influence |

**EP-Q2** Does your organization have at least one full-time dedicated detection engineer?
- [ ] Yes
- [ ] No

### Skills Development

**EP-Q3** Rate the maturity of your detection engineering skills development program.

| Score | Description |
|-------|-------------|
| [ ] 1 | No formal training; self-directed learning only |
| [ ] 2 | Ad hoc training; no structured program |
| [ ] 3 | Defined training program with regular knowledge sharing |
| [ ] 4 | Comprehensive training with cross-training and certifications |
| [ ] 5 | Continuous learning culture with community contribution and research |

**EP-Q4** Does your team have a defined training plan or skills development roadmap?
- [ ] Yes
- [ ] No

### Leadership Commitment

**EP-Q5** Rate the level of executive sponsorship and leadership commitment to detection engineering.

| Score | Description |
|-------|-------------|
| [ ] 1 | No executive awareness or sponsorship |
| [ ] 2 | Some awareness but no formal sponsorship or budget |
| [ ] 3 | Executive sponsor; dedicated budget; function formally recognized |
| [ ] 4 | Strong support; metrics reported to leadership; influences investments |
| [ ] 5 | Strategic priority; board-level visibility; cross-org influence |

**EP-Q6** Does your detection engineering function have a dedicated budget?
- [ ] Yes
- [ ] No

**EP-Q7** Describe executive engagement with detection engineering. How is the function's value communicated to and supported by leadership?

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

---

## Enrichment: Process & Governance

### Detection Lifecycle

**EG-Q1** Rate the maturity of your detection lifecycle workflow (from request through retirement).

| Score | Description |
|-------|-------------|
| [ ] 1 | No defined lifecycle; no structured workflow |
| [ ] 2 | Basic lifecycle covering creation and deployment only |
| [ ] 3 | Full lifecycle: request, development, review, testing, deploy, monitor, retire |
| [ ] 4 | Enforced through tooling; SLAs defined; cycle time tracked |
| [ ] 5 | Optimized with automated transitions and predictive analytics |

**EG-Q2** Does your team have a defined process for retiring or deprecating outdated detection rules?
- [ ] Yes
- [ ] No

### Metrics and KPI Tracking

**EG-Q3** Does your team track detection engineering KPIs (e.g., coverage, quality, velocity)?
- [ ] Yes
- [ ] No

**EG-Q4** Rate the maturity of your detection engineering metrics program.

| Score | Description |
|-------|-------------|
| [ ] 1 | No metrics tracked; success is anecdotal |
| [ ] 2 | Basic metrics tracked informally (rule count, alert volume) |
| [ ] 3 | Defined KPIs for coverage, quality, velocity; quarterly reporting |
| [ ] 4 | Comprehensive program with automated collection; metrics drive decisions |
| [ ] 5 | Advanced analytics with predictive metrics and benchmarking |

**EG-Q5** List the key metrics and KPIs your team tracks for detection engineering. How are they collected, reported, and used?

> _________________________________________________________________________
> _________________________________________________________________________
> _________________________________________________________________________

### Cross-Team Collaboration

**EG-Q6** Rate the maturity of collaboration between detection engineering and other teams (IR, threat intel, engineering).

| Score | Description |
|-------|-------------|
| [ ] 1 | Operates in isolation; no structured collaboration |
| [ ] 2 | Ad hoc collaboration, reactive to incidents |
| [ ] 3 | Regular collaboration via defined channels and scheduled touchpoints |
| [ ] 4 | Deep integration with joint planning and shared objectives |
| [ ] 5 | Seamless cross-functional collaboration with automated information sharing |

**EG-Q7** Does your detection engineering team have regularly scheduled touchpoints with incident response and threat intelligence teams?
- [ ] Yes
- [ ] No

---

*Assessment complete. See [scoring methodology](../docs/methodology.md) for how to interpret results.*
