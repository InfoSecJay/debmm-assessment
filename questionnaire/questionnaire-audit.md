# DEBMM Audit Assessment Questionnaire

> For external or third-party assessments. Includes evidence prompts.

**Organization Under Assessment**: ___________________________
**Auditor Name**: ___________________________
**Auditor Role**: ___________________________
**Date**: ___________________________
**Assessment Scope**: ___________________________

---

## Tier 0: Foundation

### Structured Rule Development

**T0-Q1** *(Structured Rule Development)* *(Scale 1-5)*
Rate the maturity of the assessed team's rule development process.

| Rating | Description |
|--------|-------------|
| 1 | No structured approach; rules created ad hoc or reactively (0% follow a formal process) |
| 2 | Some rules follow a loose process but it is inconsistently applied (<30% follow a documented process) |
| 3 | Defined methodology is documented and followed for most new rules (50-70% follow process; schema alignment >60%) |
| 4 | Standardized across team with enforced workflows, templates, and quality gates (80-90% schema alignment; all new rules go through formal review) |
| 5 | Continuous improvement via feedback loops; fully integrated with CI/CD and automated linting/validation (90-100% schema alignment) |

Evidence: ___________________________

**T0-Q2** *(Structured Rule Development)* *(Yes/No)*
Do all new detection rules go through peer review before production deployment?

[ ] Yes  [ ] No

Evidence: ___________________________

### Rule Creation and Maintenance

**T0-Q3** *(Rule Creation and Maintenance)* *(Scale 1-5)*
What percentage of the assessed team's rules are reviewed on a regular schedule?

| Rating | Description |
|--------|-------------|
| 1 | Less than 50% reviewed annually; no rule owners assigned |
| 2 | 50-70% reviewed annually; rules may have informal owners but no formal peer review process |
| 3 | 70-80% reviewed on schedule; rules have assigned owners and defined review cycles; peer review on most changes |
| 4 | 80-90% reviewed on schedule; comprehensive lifecycle management (create, test, deploy, monitor, retire); 100% peer review on changes |
| 5 | 90-100% reviewed on schedule; automated rule health monitoring flags stale or broken rules for review |

Evidence: ___________________________

### Roadmap Documentation

**T0-Q4** *(Roadmap Documentation)* *(Scale 1-5)*
Rate the maturity of the assessed team's detection engineering roadmap.

| Rating | Description |
|--------|-------------|
| 1 | No roadmap exists; work is entirely reactive or driven by individual initiative |
| 2 | Informal roadmap or backlog exists (e.g., a Jira board or wiki page) but is not regularly maintained or shared (<30% of work tied to a plan) |
| 3 | Formal roadmap documented, reviewed at least quarterly, shared with stakeholders; priorities are clear (50-70% of planned work tracked) |
| 4 | Integrated with organizational security strategy; progress tracked with metrics and reported to leadership (70-90% tracked; quarterly leadership reviews) |
| 5 | Dynamic, continuously updated roadmap driven by threat intel, gap analysis, and risk priorities (90-100% tracked; auto-updated from analysis feeds) |

Evidence: ___________________________

### Threat Modeling

**T0-Q5** *(Threat Modeling)* *(Scale 1-5)*
How frequently does the assessed team perform threat modeling?

| Rating | Description |
|--------|-------------|
| 1 | Never performed or not at all |
| 2 | Less than once per year; typically triggered by a major incident or audit finding |
| 3 | 1-2 times per year with documented results that inform the detection roadmap |
| 4 | Quarterly or more; outputs directly prioritize new detection development (>70% of new detections tied to threat model outputs) |
| 5 | Continuous proactive modeling incorporating real-time threat intel, attack surface changes, and emerging TTPs |

Evidence: ___________________________

**T0-Q6** *(Threat Modeling)* *(Yes/No)*
Does the assessed team's threat modeling use a recognized framework?

[ ] Yes  [ ] No

Evidence: ___________________________

**T0-Q7** *(Threat Modeling)* *(Yes/No)*
Do threat modeling outputs directly generate items on the assessed team's backlog?

[ ] Yes  [ ] No

Evidence: ___________________________

---

## Tier 1: Basic

### Baseline Rule Creation

**T1-Q1** *(Baseline Rule Creation)* *(Scale 1-5)*
How many custom detection rules does the assessed team maintain?

| Rating | Description |
|--------|-------------|
| 1 | Fewer than 10 custom rules; mostly relying on vendor/out-of-the-box rules |
| 2 | 10-30 rules covering the most critical threats (e.g., ransomware, credential theft, C2) |
| 3 | 30-60 rules with a mix of signature-based and behavioral detections across major categories |
| 4 | 60-100 rules including behavioral and TTP-focused detections tuned per environment |
| 5 | 100+ rules with continuous refinement, environment-specific tuning, and automated coverage analysis |

Evidence: ___________________________

**T1-Q2** *(Baseline Rule Creation)* *(Scale 1-5)*
Estimate the assessed team's MITRE ATT&CK technique coverage for priority areas.

| Rating | Description |
|--------|-------------|
| 1 | Unknown or not measured; no ATT&CK mapping performed |
| 2 | Less than 30% of priority techniques covered; coverage is ad hoc |
| 3 | 30-50% of priority techniques covered with documented gaps identified |
| 4 | 50-70% coverage including behavioral detections; gaps tracked against threat model |
| 5 | Over 70% coverage with continuous gap analysis and automated coverage tracking |

Evidence: ___________________________

### Ruleset Management

**T1-Q3** *(Ruleset Management)* *(Scale 1-5)*
Rate the maturity of the assessed team's ruleset management.

| Rating | Description |
|--------|-------------|
| 1 | No formal management; rules live only in the SIEM console with no version control or documentation (<20% in version control) |
| 2 | Some rules stored in version control (e.g., Git) with basic documentation (20-50% in VCS) |
| 3 | Most rules in version control with documentation standards; detection-as-code approach being adopted (50-80% in VCS with docs) |
| 4 | Detection-as-code is standard practice; CI/CD pipelines handle rule testing and deployment; all rules documented and versioned (80-90% in DaC pipeline) |
| 5 | Fully automated rule lifecycle: CI/CD, automated testing, continuous validation, and weekly maintenance cycles (100% DaC) |

Evidence: ___________________________

### Telemetry Quality

**T1-Q4** *(Telemetry Quality)* *(Scale 1-5)*
Rate the quality and coverage of the assessed team's telemetry.

| Rating | Description |
|--------|-------------|
| 1 | No active telemetry management; using whatever data sources happen to be available (<30% of rule types have adequate telemetry) |
| 2 | Some awareness of gaps; basic health checks on critical sources like EDR and firewall logs (30-50% adequate coverage) |
| 3 | Actively monitored; data source coverage mapped to detection needs; CTI enrichment beginning (50-70% coverage) |
| 4 | Comprehensive with automated health monitoring, CTI enrichment, and proactive gap identification (70-90% coverage) |
| 5 | Advanced workflows with real-time enrichment, automated remediation of telemetry gaps, full CTI integration (90-100% coverage) |

Evidence: ___________________________

**T1-Q5** *(Telemetry Quality)* *(Yes/No)*
Does the assessed team maintain a documented data source inventory mapped to use cases?

[ ] Yes  [ ] No

Evidence: ___________________________

**T1-Q6** *(Telemetry Quality)* *(Yes/No)*
Does the assessed team have automated alerting for data source degradation?

[ ] Yes  [ ] No

Evidence: ___________________________

### Threat Landscape Review

**T1-Q7** *(Threat Landscape Review)* *(Scale 1-5)*
How frequently does the assessed team review the threat landscape?

| Rating | Description |
|--------|-------------|
| 1 | No regular reviews; detection priorities are not informed by current threats |
| 2 | Annually or bi-annually; some rule updates after major threat advisories (1-2 reviews/year) |
| 3 | Quarterly with documented findings that update the detection roadmap (50-70% of rules reviewed against current threats) |
| 4 | Monthly reviews integrated with threat intelligence feeds; detection priorities continuously aligned (70-90% aligned) |
| 5 | Real-time threat landscape monitoring with automated intel feeds driving detection priority updates (90-100% aligned) |

Evidence: ___________________________

### Product Owner Engagement

**T1-Q8** *(Product Owner Engagement)* *(Scale 1-5)*
Rate the engagement between the assessed team and product/platform owners.

| Rating | Description |
|--------|-------------|
| 1 | No engagement; detection needs are never communicated to product/platform teams |
| 2 | Occasional ad hoc engagement, typically reactive to issues or missing features (fewer than 4 interactions per year) |
| 3 | Quarterly structured engagements to communicate detection needs, request features, and provide feedback |
| 4 | Monthly proactive partnership; detection requirements tracked on product roadmaps (>50% of requests on roadmap) |
| 5 | Continuous engagement with joint planning, shared success metrics, and detection needs directly influencing product development |

Evidence: ___________________________

### Release Testing

**T1-Q9** *(Release Testing)* *(Scale 1-5)*
Rate the maturity of the assessed team's release testing.

| Rating | Description |
|--------|-------------|
| 1 | No testing; rules are deployed to production without validation (<20% tested) |
| 2 | Basic manual testing on some rules before deployment; no standardized process or test environment (20-40% tested) |
| 3 | Standardized testing with defined test cases and a staging/test environment; most rules validated before deploy (50-70% tested) |
| 4 | Comprehensive testing including unit tests, integration tests, and emulation-based validation; rapid deployment for emerging threats (70-90% automated; 24hr critical deployment capability) |
| 5 | Continuous automated testing in full CI/CD pipeline; every rule validated before every deployment (90-100% automated) |

Evidence: ___________________________

---

## Tier 2: Intermediate

### False Positive Reduction

**T2-Q1** *(False Positive Reduction)* *(Scale 1-5)*
Rate the maturity of the assessed team's FP reduction program.

| Rating | Description |
|--------|-------------|
| 1 | Minimal or no tuning; high false positive rates accepted as normal; no FP metrics tracked |
| 2 | Reactive tuning when analysts complain about noisy rules; no systematic tracking of FP rates (10-25% FP reduction from baseline) |
| 3 | Regular tuning cycles (at least quarterly); FP rates tracked per rule; tuning is documented (25-50% FP reduction) |
| 4 | Comprehensive FP management with automated tuning suggestions, risk-based alert scoring, and continuous monitoring (>50% FP reduction) |
| 5 | Automated dynamic tuning with ML; near-zero unnecessary alert noise; continuous optimization (>75% FP reduction from baseline) |

Evidence: ___________________________

**T2-Q2** *(False Positive Reduction)* *(Scale 1-5)*
What is the assessed team's estimated FP reduction from baseline?

| Rating | Description |
|--------|-------------|
| 1 | Unknown or not measured |
| 2 | Less than 25% reduction |
| 3 | 25-50% reduction with per-rule FP rate tracking |
| 4 | 50-75% reduction with automated tuning recommendations |
| 5 | Over 75% reduction with ML-assisted continuous tuning |

Evidence: ___________________________

### Gap Analysis

**T2-Q3** *(Gap Analysis)* *(Scale 1-5)*
Rate the maturity of the assessed team's gap analysis.

| Rating | Description |
|--------|-------------|
| 1 | No gap analysis performed; detection coverage gaps are unknown |
| 2 | Some gaps identified informally after incidents expose missing detections (1-3 gaps documented; reactive only) |
| 3 | Regular analysis against ATT&CK or similar frameworks at least quarterly; gaps documented, prioritized, and tracked (5+ gaps documented and prioritized) |
| 4 | Comprehensive analysis integrated with threat modeling and risk assessment; gaps drive the detection roadmap (continuous tracking; integrated into roadmap) |
| 5 | Automated gap analysis using coverage mapping tools; real-time dashboards showing detection coverage (automated continuous analysis) |

Evidence: ___________________________

**T2-Q4** *(Gap Analysis)* *(Yes/No)*
Does the assessed team maintain a documented, prioritized gap list updated quarterly?

[ ] Yes  [ ] No

Evidence: ___________________________

**T2-Q5** *(Gap Analysis)* *(Yes/No)*
Are the assessed team's gaps communicated to stakeholders at least quarterly?

[ ] Yes  [ ] No

Evidence: ___________________________

### Internal Testing

**T2-Q6** *(Internal Testing)* *(Scale 1-5)*
Rate the maturity of the assessed team's internal testing program.

| Rating | Description |
|--------|-------------|
| 1 | No internal testing; rules are assumed to work once deployed |
| 2 | Occasional manual testing of high-priority rules using basic atomic tests (<40% emulation coverage) |
| 3 | Regular testing program with attack emulation (e.g., Atomic Red Team, Caldera) covering major detection categories; results documented (40-70% emulation coverage; at least quarterly) |
| 4 | Comprehensive testing with automated attack emulation, purple team exercises, and continuous validation (70-90% automated emulation coverage) |
| 5 | Continuous automated testing with full emulation coverage and automated regression testing on every rule change (>90% automated coverage) |

Evidence: ___________________________

---

## Tier 3: Advanced

### False Negative Triage

**T3-Q1** *(False Negative Triage)* *(Scale 1-5)*
Rate the assessed team's ability to detect and remediate false negatives.

| Rating | Description |
|--------|-------------|
| 1 | No FN identification process; missed detections only discovered during incident response |
| 2 | Some FNs identified through post-incident reviews; basic tracking of missed detections (50% of tested samples trigger expected alerts) |
| 3 | Systematic FN identification through regular testing and validation; root causes analyzed and documented (70-90% trigger rate; 30-50% FN reduction) |
| 4 | Comprehensive FN management with automated detection validation, coverage testing, and rapid remediation (90-100% trigger rate; >50% FN reduction) |
| 5 | Continuous automated FN detection using real-time validation against live threat samples (near-zero FN rate; >75% FN reduction) |

Evidence: ___________________________

**T3-Q2** *(False Negative Triage)* *(Scale 1-5)*
What is the assessed team's detection trigger rate on tested samples?

| Rating | Description |
|--------|-------------|
| 1 | Unknown or not tested |
| 2 | Less than 50% of test samples trigger expected detections |
| 3 | 50-70% trigger rate with root cause analysis on misses |
| 4 | 70-90% trigger rate with automated validation and remediation |
| 5 | Over 90% trigger rate with continuous regression testing |

Evidence: ___________________________

### External Validation

**T3-Q3** *(External Validation)* *(Scale 1-5)*
Rate the maturity of the assessed team's external validation.

| Rating | Description |
|--------|-------------|
| 1 | No external validation; no red team, pentest, or third-party assessment of detection effectiveness |
| 2 | Annual penetration test that includes some detection assessment but is not detection-focused (1 exercise per year) |
| 3 | Regular external validation through red team engagements or third-party assessments specifically focused on detection effectiveness (>1 per year; findings drive improvements) |
| 4 | Multiple external validation exercises annually including red team, purple team, and breach simulation; systematic feedback integration (multiple per year; >70% of findings remediated within 30 days) |
| 5 | Continuous BAS (breach and attack simulation) tools and regular adversary emulation exercises with real-time feedback loops |

Evidence: ___________________________

### Advanced TTP Coverage

**T3-Q4** *(Advanced TTP Coverage)* *(Scale 1-5)*
Rate the assessed team's coverage of advanced TTPs.

| Rating | Description |
|--------|-------------|
| 1 | No advanced TTP coverage; detections are signature/IOC-based only |
| 2 | Limited coverage of 1-2 advanced technique categories (e.g., basic PowerShell abuse detection) |
| 3 | Growing coverage of 3-4 categories informed by threat intel; behavioral detections supplement signatures (e.g., LOLBin usage, fileless execution, credential access evasion) |
| 4 | Comprehensive coverage of 5+ categories including sophisticated evasion, novel attack chains, and emerging threats (e.g., defense evasion/log tampering, lateral movement via legitimate tools, supply chain vectors) |
| 5 | Continuous proactive coverage using AI/ML for anomaly detection and automated response to emerging TTPs; real-time advanced TTP detection |

Evidence: ___________________________

**T3-Q5** *(Advanced TTP Coverage)* *(Scale 1-5)*
How many of these categories does the assessed team have behavioral detections for: LOLBins, fileless malware, credential evasion, defense evasion, lateral movement?

| Rating | Description |
|--------|-------------|
| 1 | None of these |
| 2 | 1 of these categories |
| 3 | 2-3 of these categories |
| 4 | 4-5 of these categories |
| 5 | All 5 plus additional categories (e.g., supply chain attacks, AI-assisted threats) |

Evidence: ___________________________

---

## Tier 4: Expert

### Threat Hunting

**T4-Q1** *(Threat Hunting)* *(Scale 1-5)*
Rate the maturity of the assessed team's threat hunting.

| Rating | Description |
|--------|-------------|
| 1 | No proactive hunting; all detection is passive through deployed rules |
| 2 | Occasional ad hoc hunting triggered by intel or incidents; findings not systematically converted to detections (fewer than 2 hunts/month; <30% findings converted to rules) |
| 3 | Regular structured hunting at least weekly, driven by documented hypotheses from intel or gap analysis; findings feed detection development (weekly hunts; 50-70% of findings integrated into rules) |
| 4 | Comprehensive daily hunting program with advanced analytics (e.g., statistical baselining, graph analysis); systematic integration of all findings (daily hunts; >90% findings integrated) |
| 5 | Automated real-time hunting augmented by AI/ML; hunting outputs automatically generate detection rule candidates |

Evidence: ___________________________

**T4-Q2** *(Threat Hunting)* *(Yes/No)*
Are the assessed team's hunts driven by documented hypotheses?

[ ] Yes  [ ] No

Evidence: ___________________________

**T4-Q3** *(Threat Hunting)* *(Yes/No)*
Is there a defined process to convert hunting findings into production rules?

[ ] Yes  [ ] No

Evidence: ___________________________

### Automation and Continuous Improvement

**T4-Q4** *(Automation and Continuous Improvement)* *(Scale 1-5)*
What percentage of the assessed team's DE tasks are automated?

| Rating | Description |
|--------|-------------|
| 1 | None; all processes are manual (0% automated) |
| 2 | Basic automation of some repetitive tasks like deployment scripts (<30% automated) |
| 3 | Significant lifecycle automation including AI-based quality checks on new rules; improvement metrics tracked (40-60% automated) |
| 4 | Advanced automation covering most of the lifecycle; AI/LLM tools used for rule optimization, duplication detection, and analysis (70-80% automated) |
| 5 | Full AI/LLM integration throughout the detection lifecycle; automated rule generation, tuning, and retirement (>90% automated; 40%+ FP reduction via AI) |

Evidence: ___________________________

**T4-Q5** *(Automation and Continuous Improvement)* *(Scale 1-5)*
How many detection lifecycle stages have automation or AI integration?

| Rating | Description |
|--------|-------------|
| 1 | None; all stages are manual |
| 2 | 1 stage (e.g., deployment scripts only) |
| 3 | 2-3 stages automated or AI-assisted |
| 4 | 4-5 stages automated or AI-assisted |
| 5 | All 6 stages with AI/LLM integration throughout |

Evidence: ___________________________

---

## Enrichment: People & Organization

### Team Structure

**EP-Q1** *(Team Structure)* *(Scale 1-5)*
Rate the maturity of the assessed detection engineering team structure.

| Rating | Description |
|--------|-------------|
| 1 | No dedicated roles; detection work is a side task for SOC analysts or other staff (0 dedicated FTEs) |
| 2 | One or more staff have detection engineering as a partial responsibility; no formal team or career path |
| 3 | At least one dedicated detection engineering role or team established with clear responsibilities and defined career progression |
| 4 | Established multi-person team with subject matter experts across key domains (host, network, cloud, application); defined career ladder |
| 5 | Mature team with deep specialization, mentorship programs, and influence on organizational security strategy |

Evidence: ___________________________

### Skills Development

**EP-Q2** *(Skills Development)* *(Scale 1-5)*
Rate the maturity of the assessed team's skills development.

| Rating | Description |
|--------|-------------|
| 1 | No formal training; learning is entirely self-directed with no organizational support or budget |
| 2 | Ad hoc training; individuals may attend a conference or take a course occasionally but there is no structured program |
| 3 | Written training plan with scheduled activities; regular knowledge sharing sessions (e.g., weekly/biweekly); defined skill requirements for roles |
| 4 | Comprehensive program covering advanced topics; cross-training with IR, threat intel, and engineering teams; certifications supported and funded |
| 5 | Continuous learning culture with community contribution (blog posts, conference talks), internal research programs, and mentorship |

Evidence: ___________________________

### Leadership Commitment

**EP-Q3** *(Leadership Commitment)* *(Scale 1-5)*
Rate the executive sponsorship of the assessed detection engineering function.

| Rating | Description |
|--------|-------------|
| 1 | No executive awareness; detection engineering is not recognized as a distinct capability |
| 2 | Some leadership awareness but no formal executive sponsor, no dedicated budget allocation |
| 3 | Executive sponsor identified; dedicated budget for tooling and headcount; detection engineering formally recognized as a function |
| 4 | Strong executive support; detection engineering metrics included in regular executive reporting; function influences security investment decisions |
| 5 | Detection engineering is a strategic priority; board-level visibility; leadership actively champions the function across the organization |

Evidence: ___________________________

**EP-Q4** *(Leadership Commitment)* *(Yes/No)*
Does the assessed team present metrics to executive leadership at least quarterly?

[ ] Yes  [ ] No

Evidence: ___________________________

**EP-Q5** *(Leadership Commitment)* *(Yes/No)*
Has leadership made investment/staffing decisions based on the assessed team's metrics in the past year?

[ ] Yes  [ ] No

Evidence: ___________________________

---

## Enrichment: Process & Governance

### Detection Lifecycle

**EG-Q1** *(Detection Lifecycle)* *(Scale 1-5)*
Rate the maturity of the assessed team's detection lifecycle workflow.

| Rating | Description |
|--------|-------------|
| 1 | No defined lifecycle; detections created and deployed without structured workflow |
| 2 | Basic lifecycle covering creation and deployment only; no formal stages for review, testing, or retirement (2-3 stages defined) |
| 3 | Full lifecycle defined and followed: request, development, review, testing, deployment, monitoring, and retirement (all 7 stages documented) |
| 4 | Lifecycle enforced through tooling and automation; SLAs defined for each stage; cycle time and throughput metrics tracked |
| 5 | Optimized lifecycle with automated stage transitions, predictive analytics for rule retirement, and continuous process improvement |

Evidence: ___________________________

### Metrics and KPIs

**EG-Q2** *(Metrics Tracking)* *(Scale 1-5)*
Rate the maturity of the assessed team's metrics program.

| Rating | Description |
|--------|-------------|
| 1 | No metrics tracked; success is anecdotal or unmeasured |
| 2 | 1-2 basic metrics tracked informally (e.g., rule count, alert volume); no formal KPI program or dashboards |
| 3 | 3-5 defined KPIs covering key areas with quarterly reporting and dashboards (e.g., coverage %, FP rate, deployment velocity) |
| 4 | 5+ KPIs with automated collection, trending, and correlation; metrics actively drive decision-making and resource allocation |
| 5 | Advanced analytics with predictive metrics, industry benchmarking, and data-driven continuous optimization |

Evidence: ___________________________

**EG-Q3** *(Metrics Tracking)* *(Scale 1-5)*
How many of these KPI categories does the assessed team track: coverage, quality, velocity, rule health, analyst impact?

| Rating | Description |
|--------|-------------|
| 1 | None of these are tracked |
| 2 | 1 category tracked |
| 3 | 2-3 categories tracked with regular reporting |
| 4 | 4-5 categories tracked with automated collection and dashboards |
| 5 | All 5 categories plus additional metrics with trend analysis and benchmarking |

Evidence: ___________________________

### Cross-Team Collaboration

**EG-Q4** *(Cross-Team Collaboration)* *(Scale 1-5)*
Rate cross-team collaboration involving the assessed detection engineering function.

| Rating | Description |
|--------|-------------|
| 1 | Operates in isolation; no structured collaboration with other teams |
| 2 | Ad hoc collaboration, typically reactive to incidents or specific requests (no scheduled touchpoints) |
| 3 | Regular collaboration through defined channels; scheduled touchpoints at least monthly with IR and threat intel teams |
| 4 | Deep integration with joint planning sessions at least quarterly, shared OKRs/objectives, and integrated workflows (e.g., threat intel feeds directly inform detection priorities) |
| 5 | Seamless cross-functional collaboration with automated information sharing, shared metrics dashboards, and embedded team members |

Evidence: ___________________________

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
