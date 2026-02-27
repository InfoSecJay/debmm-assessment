# DEBMM Self-Assessment Questionnaire

> 41 questions across 7 categories. All answers are dropdown selections.

**Organization**: ___________________________
**Assessor**: ___________________________
**Date**: ___________________________

---

## Tier 0: Foundation

### Structured Rule Development

**T0-Q1** *(Structured Rule Development)* *(Scale 1-5)*
Rate the maturity of your team's rule development process.

| Rating | Description |
|--------|-------------|
| 1 | No structured approach; rules created ad hoc or reactively (0% follow a formal process) |
| 2 | Some rules follow a loose process but it is inconsistently applied (<30% follow a documented process) |
| 3 | Defined methodology is documented and followed for most new rules (50-70% follow process; schema alignment >60%) |
| 4 | Standardized across team with enforced workflows, templates, and quality gates (80-90% schema alignment; all new rules go through formal review) |
| 5 | Continuous improvement via feedback loops; fully integrated with CI/CD and automated linting/validation (90-100% schema alignment) |

**T0-Q2** *(Structured Rule Development)* *(Yes/No)*
Do all new detection rules go through peer review before deployment to production?

[ ] Yes  [ ] No

### Rule Creation and Maintenance

**T0-Q3** *(Rule Creation and Maintenance)* *(Scale 1-5)*
What percentage of your detection rules are reviewed on a regular schedule?

| Rating | Description |
|--------|-------------|
| 1 | Less than 50% reviewed annually; no rule owners assigned |
| 2 | 50-70% reviewed annually; rules may have informal owners but no formal peer review process |
| 3 | 70-80% reviewed on schedule; rules have assigned owners and defined review cycles; peer review on most changes |
| 4 | 80-90% reviewed on schedule; comprehensive lifecycle management (create, test, deploy, monitor, retire); 100% peer review on changes |
| 5 | 90-100% reviewed on schedule; automated rule health monitoring flags stale or broken rules for review |

### Roadmap Documentation

**T0-Q4** *(Roadmap Documentation)* *(Scale 1-5)*
Rate the maturity of your detection engineering roadmap.

| Rating | Description |
|--------|-------------|
| 1 | No roadmap exists; work is entirely reactive or driven by individual initiative |
| 2 | Informal roadmap or backlog exists (e.g., a Jira board or wiki page) but is not regularly maintained or shared (<30% of work tied to a plan) |
| 3 | Formal roadmap documented, reviewed at least quarterly, shared with stakeholders; priorities are clear (50-70% of planned work tracked) |
| 4 | Integrated with organizational security strategy; progress tracked with metrics and reported to leadership (70-90% tracked; quarterly leadership reviews) |
| 5 | Dynamic, continuously updated roadmap driven by threat intel, gap analysis, and risk priorities (90-100% tracked; auto-updated from analysis feeds) |

### Threat Modeling

**T0-Q5** *(Threat Modeling)* *(Scale 1-5)*
How frequently does your team perform threat modeling to inform detection priorities?

| Rating | Description |
|--------|-------------|
| 1 | Never performed or not at all |
| 2 | Less than once per year; typically triggered by a major incident or audit finding |
| 3 | 1-2 times per year with documented results that inform the detection roadmap |
| 4 | Quarterly or more; outputs directly prioritize new detection development (>70% of new detections tied to threat model outputs) |
| 5 | Continuous proactive modeling incorporating real-time threat intel, attack surface changes, and emerging TTPs |

**T0-Q6** *(Threat Modeling)* *(Yes/No)*
Does your threat modeling use a recognized framework (e.g., STRIDE, MITRE ATT&CK, PASTA, attack trees)?

[ ] Yes  [ ] No

**T0-Q7** *(Threat Modeling)* *(Yes/No)*
Do threat modeling outputs directly generate items on your detection engineering backlog or roadmap?

[ ] Yes  [ ] No

---

## Tier 1: Basic

### Baseline Rule Creation

**T1-Q1** *(Baseline Rule Creation)* *(Scale 1-5)*
How many custom detection rules does your team maintain (excluding vendor defaults)?

| Rating | Description |
|--------|-------------|
| 1 | Fewer than 10 custom rules; mostly relying on vendor/out-of-the-box rules |
| 2 | 10-30 rules covering the most critical threats (e.g., ransomware, credential theft, C2) |
| 3 | 30-60 rules with a mix of signature-based and behavioral detections across major categories |
| 4 | 60-100 rules including behavioral and TTP-focused detections tuned per environment |
| 5 | 100+ rules with continuous refinement, environment-specific tuning, and automated coverage analysis |

**T1-Q2** *(Baseline Rule Creation)* *(Scale 1-5)*
Estimate your MITRE ATT&CK technique coverage for your organization's priority threat areas.

| Rating | Description |
|--------|-------------|
| 1 | Unknown or not measured; no ATT&CK mapping performed |
| 2 | Less than 30% of priority techniques covered; coverage is ad hoc |
| 3 | 30-50% of priority techniques covered with documented gaps identified |
| 4 | 50-70% coverage including behavioral detections; gaps tracked against threat model |
| 5 | Over 70% coverage with continuous gap analysis and automated coverage tracking |

### Ruleset Management

**T1-Q3** *(Ruleset Management)* *(Scale 1-5)*
Rate the maturity of your ruleset management practices.

| Rating | Description |
|--------|-------------|
| 1 | No formal management; rules live only in the SIEM console with no version control or documentation (<20% in version control) |
| 2 | Some rules stored in version control (e.g., Git) with basic documentation (20-50% in VCS) |
| 3 | Most rules in version control with documentation standards; detection-as-code approach being adopted (50-80% in VCS with docs) |
| 4 | Detection-as-code is standard practice; CI/CD pipelines handle rule testing and deployment; all rules documented and versioned (80-90% in DaC pipeline) |
| 5 | Fully automated rule lifecycle: CI/CD, automated testing, continuous validation, and weekly maintenance cycles (100% DaC) |

### Telemetry Quality

**T1-Q4** *(Telemetry Quality)* *(Scale 1-5)*
Rate the quality and coverage of your telemetry data sources for detection.

| Rating | Description |
|--------|-------------|
| 1 | No active telemetry management; using whatever data sources happen to be available (<30% of rule types have adequate telemetry) |
| 2 | Some awareness of gaps; basic health checks on critical sources like EDR and firewall logs (30-50% adequate coverage) |
| 3 | Actively monitored; data source coverage mapped to detection needs; CTI enrichment beginning (50-70% coverage) |
| 4 | Comprehensive with automated health monitoring, CTI enrichment, and proactive gap identification (70-90% coverage) |
| 5 | Advanced workflows with real-time enrichment, automated remediation of telemetry gaps, full CTI integration (90-100% coverage) |

**T1-Q5** *(Telemetry Quality)* *(Yes/No)*
Do you maintain a documented inventory of telemetry data sources mapped to detection use cases?

[ ] Yes  [ ] No

**T1-Q6** *(Telemetry Quality)* *(Yes/No)*
Do you have automated alerting for when critical data sources stop ingesting or degrade in quality?

[ ] Yes  [ ] No

### Threat Landscape Review

**T1-Q7** *(Threat Landscape Review)* *(Scale 1-5)*
How frequently does your team review the threat landscape to update detection priorities?

| Rating | Description |
|--------|-------------|
| 1 | No regular reviews; detection priorities are not informed by current threats |
| 2 | Annually or bi-annually; some rule updates after major threat advisories (1-2 reviews/year) |
| 3 | Quarterly with documented findings that update the detection roadmap (50-70% of rules reviewed against current threats) |
| 4 | Monthly reviews integrated with threat intelligence feeds; detection priorities continuously aligned (70-90% aligned) |
| 5 | Real-time threat landscape monitoring with automated intel feeds driving detection priority updates (90-100% aligned) |

### Product Owner Engagement

**T1-Q8** *(Product Owner Engagement)* *(Scale 1-5)*
Rate the engagement between your detection engineering team and security product/platform owners (e.g., SIEM vendor, EDR team).

| Rating | Description |
|--------|-------------|
| 1 | No engagement; detection needs are never communicated to product/platform teams |
| 2 | Occasional ad hoc engagement, typically reactive to issues or missing features (fewer than 4 interactions per year) |
| 3 | Quarterly structured engagements to communicate detection needs, request features, and provide feedback |
| 4 | Monthly proactive partnership; detection requirements tracked on product roadmaps (>50% of requests on roadmap) |
| 5 | Continuous engagement with joint planning, shared success metrics, and detection needs directly influencing product development |

### Release Testing

**T1-Q9** *(Release Testing)* *(Scale 1-5)*
Rate the maturity of your detection rule testing before production deployment.

| Rating | Description |
|--------|-------------|
| 1 | No testing; rules are deployed to production without validation (<20% tested) |
| 2 | Basic manual testing on some rules before deployment; no standardized process or test environment (20-40% tested) |
| 3 | Standardized testing with defined test cases and a staging/test environment; most rules validated before deploy (50-70% tested) |
| 4 | Comprehensive testing including unit tests, integration tests, and emulation-based validation; rapid deployment for emerging threats (70-90% automated; 24hr critical deployment capability) |
| 5 | Continuous automated testing in full CI/CD pipeline; every rule validated before every deployment (90-100% automated) |

---

## Tier 2: Intermediate

### False Positive Reduction

**T2-Q1** *(False Positive Reduction)* *(Scale 1-5)*
Rate the maturity of your false positive tuning and reduction program.

| Rating | Description |
|--------|-------------|
| 1 | Minimal or no tuning; high false positive rates accepted as normal; no FP metrics tracked |
| 2 | Reactive tuning when analysts complain about noisy rules; no systematic tracking of FP rates (10-25% FP reduction from baseline) |
| 3 | Regular tuning cycles (at least quarterly); FP rates tracked per rule; tuning is documented (25-50% FP reduction) |
| 4 | Comprehensive FP management with automated tuning suggestions, risk-based alert scoring, and continuous monitoring (>50% FP reduction) |
| 5 | Automated dynamic tuning with ML; near-zero unnecessary alert noise; continuous optimization (>75% FP reduction from baseline) |

**T2-Q2** *(False Positive Reduction)* *(Scale 1-5)*
What is your estimated false positive reduction from initial baseline across your tuned rules?

| Rating | Description |
|--------|-------------|
| 1 | Unknown or not measured |
| 2 | Less than 25% reduction |
| 3 | 25-50% reduction with per-rule FP rate tracking |
| 4 | 50-75% reduction with automated tuning recommendations |
| 5 | Over 75% reduction with ML-assisted continuous tuning |

### Gap Analysis

**T2-Q3** *(Gap Analysis)* *(Scale 1-5)*
Rate the maturity of your detection coverage gap analysis.

| Rating | Description |
|--------|-------------|
| 1 | No gap analysis performed; detection coverage gaps are unknown |
| 2 | Some gaps identified informally after incidents expose missing detections (1-3 gaps documented; reactive only) |
| 3 | Regular analysis against ATT&CK or similar frameworks at least quarterly; gaps documented, prioritized, and tracked (5+ gaps documented and prioritized) |
| 4 | Comprehensive analysis integrated with threat modeling and risk assessment; gaps drive the detection roadmap (continuous tracking; integrated into roadmap) |
| 5 | Automated gap analysis using coverage mapping tools; real-time dashboards showing detection coverage (automated continuous analysis) |

**T2-Q4** *(Gap Analysis)* *(Yes/No)*
Do you maintain a documented, prioritized list of detection coverage gaps that is updated at least quarterly?

[ ] Yes  [ ] No

**T2-Q5** *(Gap Analysis)* *(Yes/No)*
Are detection coverage gaps formally communicated to stakeholders (leadership, IR, threat intel) at least quarterly?

[ ] Yes  [ ] No

### Internal Testing

**T2-Q6** *(Internal Testing)* *(Scale 1-5)*
Rate the maturity of your internal detection testing and validation program.

| Rating | Description |
|--------|-------------|
| 1 | No internal testing; rules are assumed to work once deployed |
| 2 | Occasional manual testing of high-priority rules using basic atomic tests (<40% emulation coverage) |
| 3 | Regular testing program with attack emulation (e.g., Atomic Red Team, Caldera) covering major detection categories; results documented (40-70% emulation coverage; at least quarterly) |
| 4 | Comprehensive testing with automated attack emulation, purple team exercises, and continuous validation (70-90% automated emulation coverage) |
| 5 | Continuous automated testing with full emulation coverage and automated regression testing on every rule change (>90% automated coverage) |

---

## Tier 3: Advanced

### False Negative Triage

**T3-Q1** *(False Negative Triage)* *(Scale 1-5)*
Rate your team's ability to identify and remediate false negatives (missed detections).

| Rating | Description |
|--------|-------------|
| 1 | No FN identification process; missed detections only discovered during incident response |
| 2 | Some FNs identified through post-incident reviews; basic tracking of missed detections (50% of tested samples trigger expected alerts) |
| 3 | Systematic FN identification through regular testing and validation; root causes analyzed and documented (70-90% trigger rate; 30-50% FN reduction) |
| 4 | Comprehensive FN management with automated detection validation, coverage testing, and rapid remediation (90-100% trigger rate; >50% FN reduction) |
| 5 | Continuous automated FN detection using real-time validation against live threat samples (near-zero FN rate; >75% FN reduction) |

**T3-Q2** *(False Negative Triage)* *(Scale 1-5)*
What is your detection trigger rate when tested samples or emulations are run against your rules?

| Rating | Description |
|--------|-------------|
| 1 | Unknown or not tested |
| 2 | Less than 50% of test samples trigger expected detections |
| 3 | 50-70% trigger rate with root cause analysis on misses |
| 4 | 70-90% trigger rate with automated validation and remediation |
| 5 | Over 90% trigger rate with continuous regression testing |

### External Validation

**T3-Q3** *(External Validation)* *(Scale 1-5)*
Rate the maturity of your external validation program for detection capabilities.

| Rating | Description |
|--------|-------------|
| 1 | No external validation; no red team, pentest, or third-party assessment of detection effectiveness |
| 2 | Annual penetration test that includes some detection assessment but is not detection-focused (1 exercise per year) |
| 3 | Regular external validation through red team engagements or third-party assessments specifically focused on detection effectiveness (>1 per year; findings drive improvements) |
| 4 | Multiple external validation exercises annually including red team, purple team, and breach simulation; systematic feedback integration (multiple per year; >70% of findings remediated within 30 days) |
| 5 | Continuous BAS (breach and attack simulation) tools and regular adversary emulation exercises with real-time feedback loops |

### Advanced TTP Coverage

**T3-Q4** *(Advanced TTP Coverage)* *(Scale 1-5)*
Rate your detection coverage of advanced TTPs beyond basic signatures and IOCs.

| Rating | Description |
|--------|-------------|
| 1 | No advanced TTP coverage; detections are signature/IOC-based only |
| 2 | Limited coverage of 1-2 advanced technique categories (e.g., basic PowerShell abuse detection) |
| 3 | Growing coverage of 3-4 categories informed by threat intel; behavioral detections supplement signatures (e.g., LOLBin usage, fileless execution, credential access evasion) |
| 4 | Comprehensive coverage of 5+ categories including sophisticated evasion, novel attack chains, and emerging threats (e.g., defense evasion/log tampering, lateral movement via legitimate tools, supply chain vectors) |
| 5 | Continuous proactive coverage using AI/ML for anomaly detection and automated response to emerging TTPs; real-time advanced TTP detection |

**T3-Q5** *(Advanced TTP Coverage)* *(Scale 1-5)*
How many of these advanced TTP categories does your team have behavioral detections for: (1) LOLBins/living-off-the-land, (2) fileless malware, (3) credential dumping evasion, (4) defense evasion/log tampering, (5) lateral movement via legitimate tools?

| Rating | Description |
|--------|-------------|
| 1 | None of these |
| 2 | 1 of these categories |
| 3 | 2-3 of these categories |
| 4 | 4-5 of these categories |
| 5 | All 5 plus additional categories (e.g., supply chain attacks, AI-assisted threats) |

---

## Tier 4: Expert

### Threat Hunting

**T4-Q1** *(Threat Hunting)* *(Scale 1-5)*
Rate the maturity of your threat hunting program.

| Rating | Description |
|--------|-------------|
| 1 | No proactive hunting; all detection is passive through deployed rules |
| 2 | Occasional ad hoc hunting triggered by intel or incidents; findings not systematically converted to detections (fewer than 2 hunts/month; <30% findings converted to rules) |
| 3 | Regular structured hunting at least weekly, driven by documented hypotheses from intel or gap analysis; findings feed detection development (weekly hunts; 50-70% of findings integrated into rules) |
| 4 | Comprehensive daily hunting program with advanced analytics (e.g., statistical baselining, graph analysis); systematic integration of all findings (daily hunts; >90% findings integrated) |
| 5 | Automated real-time hunting augmented by AI/ML; hunting outputs automatically generate detection rule candidates |

**T4-Q2** *(Threat Hunting)* *(Yes/No)*
Are your threat hunts driven by documented hypotheses (from intel, incidents, or gap analysis) rather than ad hoc exploration?

[ ] Yes  [ ] No

**T4-Q3** *(Threat Hunting)* *(Yes/No)*
Is there a defined process to convert threat hunting findings into production detection rules?

[ ] Yes  [ ] No

### Automation and Continuous Improvement

**T4-Q4** *(Automation and Continuous Improvement)* *(Scale 1-5)*
What percentage of your detection engineering tasks are automated?

| Rating | Description |
|--------|-------------|
| 1 | None; all processes are manual (0% automated) |
| 2 | Basic automation of some repetitive tasks like deployment scripts (<30% automated) |
| 3 | Significant lifecycle automation including AI-based quality checks on new rules; improvement metrics tracked (40-60% automated) |
| 4 | Advanced automation covering most of the lifecycle; AI/LLM tools used for rule optimization, duplication detection, and analysis (70-80% automated) |
| 5 | Full AI/LLM integration throughout the detection lifecycle; automated rule generation, tuning, and retirement (>90% automated; 40%+ FP reduction via AI) |

**T4-Q5** *(Automation and Continuous Improvement)* *(Scale 1-5)*
How many detection lifecycle stages have AI/LLM or automation integration? Stages: (1) rule authoring, (2) testing, (3) tuning, (4) deployment, (5) monitoring, (6) retirement.

| Rating | Description |
|--------|-------------|
| 1 | None; all stages are manual |
| 2 | 1 stage (e.g., deployment scripts only) |
| 3 | 2-3 stages automated or AI-assisted |
| 4 | 4-5 stages automated or AI-assisted |
| 5 | All 6 stages with AI/LLM integration throughout |

---

## Enrichment: People & Organization

### Team Structure

**EP-Q1** *(Team Structure)* *(Scale 1-5)*
Rate the maturity of your detection engineering team structure.

| Rating | Description |
|--------|-------------|
| 1 | No dedicated roles; detection work is a side task for SOC analysts or other staff (0 dedicated FTEs) |
| 2 | One or more staff have detection engineering as a partial responsibility; no formal team or career path |
| 3 | At least one dedicated detection engineering role or team established with clear responsibilities and defined career progression |
| 4 | Established multi-person team with subject matter experts across key domains (host, network, cloud, application); defined career ladder |
| 5 | Mature team with deep specialization, mentorship programs, and influence on organizational security strategy |

### Skills Development

**EP-Q2** *(Skills Development)* *(Scale 1-5)*
Rate the maturity of your detection engineering skills development program.

| Rating | Description |
|--------|-------------|
| 1 | No formal training; learning is entirely self-directed with no organizational support or budget |
| 2 | Ad hoc training; individuals may attend a conference or take a course occasionally but there is no structured program |
| 3 | Written training plan with scheduled activities; regular knowledge sharing sessions (e.g., weekly/biweekly); defined skill requirements for roles |
| 4 | Comprehensive program covering advanced topics; cross-training with IR, threat intel, and engineering teams; certifications supported and funded |
| 5 | Continuous learning culture with community contribution (blog posts, conference talks), internal research programs, and mentorship |

### Leadership Commitment

**EP-Q3** *(Leadership Commitment)* *(Scale 1-5)*
Rate the level of executive sponsorship and leadership commitment to detection engineering.

| Rating | Description |
|--------|-------------|
| 1 | No executive awareness; detection engineering is not recognized as a distinct capability |
| 2 | Some leadership awareness but no formal executive sponsor, no dedicated budget allocation |
| 3 | Executive sponsor identified; dedicated budget for tooling and headcount; detection engineering formally recognized as a function |
| 4 | Strong executive support; detection engineering metrics included in regular executive reporting; function influences security investment decisions |
| 5 | Detection engineering is a strategic priority; board-level visibility; leadership actively champions the function across the organization |

**EP-Q4** *(Leadership Commitment)* *(Yes/No)*
Does your detection engineering team present metrics or results to executive leadership at least quarterly?

[ ] Yes  [ ] No

**EP-Q5** *(Leadership Commitment)* *(Yes/No)*
Has executive leadership made investment or staffing decisions based on detection engineering metrics or recommendations in the past year?

[ ] Yes  [ ] No

---

## Enrichment: Process & Governance

### Detection Lifecycle

**EG-Q1** *(Detection Lifecycle)* *(Scale 1-5)*
Rate the maturity of your detection lifecycle workflow (from request through retirement).

| Rating | Description |
|--------|-------------|
| 1 | No defined lifecycle; detections created and deployed without structured workflow |
| 2 | Basic lifecycle covering creation and deployment only; no formal stages for review, testing, or retirement (2-3 stages defined) |
| 3 | Full lifecycle defined and followed: request, development, review, testing, deployment, monitoring, and retirement (all 7 stages documented) |
| 4 | Lifecycle enforced through tooling and automation; SLAs defined for each stage; cycle time and throughput metrics tracked |
| 5 | Optimized lifecycle with automated stage transitions, predictive analytics for rule retirement, and continuous process improvement |

### Metrics and KPIs

**EG-Q2** *(Metrics Tracking)* *(Scale 1-5)*
Rate the maturity of your detection engineering metrics program.

| Rating | Description |
|--------|-------------|
| 1 | No metrics tracked; success is anecdotal or unmeasured |
| 2 | 1-2 basic metrics tracked informally (e.g., rule count, alert volume); no formal KPI program or dashboards |
| 3 | 3-5 defined KPIs covering key areas with quarterly reporting and dashboards (e.g., coverage %, FP rate, deployment velocity) |
| 4 | 5+ KPIs with automated collection, trending, and correlation; metrics actively drive decision-making and resource allocation |
| 5 | Advanced analytics with predictive metrics, industry benchmarking, and data-driven continuous optimization |

**EG-Q3** *(Metrics Tracking)* *(Scale 1-5)*
How many of these KPI categories does your team actively track: (1) detection coverage (ATT&CK %), (2) detection quality (FP/FN rates), (3) detection velocity (time to deploy new rules), (4) rule health (stale/broken rules), (5) analyst impact (alert-to-incident ratio)?

| Rating | Description |
|--------|-------------|
| 1 | None of these are tracked |
| 2 | 1 category tracked |
| 3 | 2-3 categories tracked with regular reporting |
| 4 | 4-5 categories tracked with automated collection and dashboards |
| 5 | All 5 categories plus additional metrics with trend analysis and benchmarking |

### Cross-Team Collaboration

**EG-Q4** *(Cross-Team Collaboration)* *(Scale 1-5)*
Rate the maturity of collaboration between detection engineering and other security teams (IR, threat intel, security engineering).

| Rating | Description |
|--------|-------------|
| 1 | Operates in isolation; no structured collaboration with other teams |
| 2 | Ad hoc collaboration, typically reactive to incidents or specific requests (no scheduled touchpoints) |
| 3 | Regular collaboration through defined channels; scheduled touchpoints at least monthly with IR and threat intel teams |
| 4 | Deep integration with joint planning sessions at least quarterly, shared OKRs/objectives, and integrated workflows (e.g., threat intel feeds directly inform detection priorities) |
| 5 | Seamless cross-functional collaboration with automated information sharing, shared metrics dashboards, and embedded team members |

---

*Assessment complete. See [scoring methodology](../docs/methodology.md) for how to interpret results.*
