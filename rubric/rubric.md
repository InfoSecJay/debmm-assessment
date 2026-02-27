# DEBMM Assessment Rubric

> Based on [Elastic's Detection Engineering Behavior Maturity Model](https://www.elastic.co/security-labs/elastic-releases-debmm) with enrichment from [detectionengineering.io](https://detectionengineering.io/).

## Maturity Levels

| Level | Name | Description |
|-------|------|-------------|
| 1 | **Initial** | Minimal or no structured activity in this area |
| 2 | **Repeatable** | Sporadic and inconsistent efforts; some awareness but no formal process |
| 3 | **Defined** | Regular, documented processes are in place and followed consistently |
| 4 | **Managed** | Comprehensive, well-integrated activities with measurable outcomes |
| 5 | **Optimized** | Fully automated, continuously improving, and deeply embedded in operations |

---

## Tier 0: Foundation

Establishes the basic groundwork for detection engineering. Without these foundational practices, higher-tier activities lack structure and consistency.

### Structured Rule Development Approach

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No structured approach; rules created randomly or reactively | 0% of rules follow a formal process |
| 2 - Repeatable | Some rules follow a loose process, inconsistently applied | <30% follow a documented process |
| 3 - Defined | Defined methodology exists, documented; most new rules follow it with peer review | 50-70% follow process; >60% schema alignment |
| 4 - Managed | Standardized across team with enforced workflows, templates, and quality gates | 80-90% schema alignment; formal review on all new rules |
| 5 - Optimized | Continuous improvement via feedback loops; integrated with CI/CD and automated checks | 90-100% schema alignment; automated linting/validation |

### Rule Creation and Maintenance

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | Rules created ad hoc with no maintenance schedule; stale rules accumulate | <50% of rules reviewed annually |
| 2 - Repeatable | Some rules periodically reviewed; updates happen reactively | 50-70% reviewed annually; no formal peer review |
| 3 - Defined | Regular review cycles established; rules have owners and schedules | 70-80% reviewed on schedule; peer review on most changes |
| 4 - Managed | Comprehensive lifecycle management with creation, testing, deployment, monitoring, retirement | 80-90% reviewed on schedule; 100% peer review |
| 5 - Optimized | Continuous improvement with automated health monitoring and triggered updates | 90-100% reviewed; automated health monitoring |

### Roadmap Documentation

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No detection roadmap exists; work is entirely reactive | 0% of work tied to a documented plan |
| 2 - Repeatable | Informal roadmap or backlog exists but not regularly maintained | <30% of rules have scheduled timelines |
| 3 - Defined | Formal roadmap documented, reviewed quarterly, shared with stakeholders | 50-70% of planned work tracked against roadmap |
| 4 - Managed | Integrated with organizational security strategy; progress tracked with metrics | 70-90% tracked; quarterly reviews with leadership |
| 5 - Optimized | Dynamic, continuously updated roadmap driven by intel, gap analysis, and risk | 90-100% tracked; auto-updated from analysis feeds |

### Threat Modeling

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No threat modeling performed | Zero exercises performed |
| 2 - Repeatable | Occasional exercises triggered by incidents or major changes | <1 formal exercise per year |
| 3 - Defined | Quarterly exercises inform detection priorities; results documented | Quarterly exercises; results documented |
| 4 - Managed | Integrated into detection development lifecycle; new detections prioritized by outputs | Monthly exercises; >70% new detections tied to threat models |
| 5 - Optimized | Continuous proactive modeling with real-time intelligence and emerging TTPs | Continuous; real-time integration with intel feeds |

---

## Tier 1: Basic

Establishes baseline detection capabilities with systematic management, version control, and initial alignment with the threat landscape.

### Baseline Rule Creation

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | Few or no baseline rules; limited to out-of-the-box vendor rules | <10 custom rules; minimal ATT&CK coverage |
| 2 - Repeatable | Small set covers most critical threats; basic signature/IOC detections | 10-30 rules; <30% ATT&CK coverage for priority areas |
| 3 - Defined | Key threat categories covered with mix of signature and behavioral | 30-60 rules; 30-50% ATT&CK coverage with documented gaps |
| 4 - Managed | Comprehensive baseline with behavioral and TTP-focused detections | 60-100 rules; 50-70% ATT&CK coverage including behavioral detections; gaps tracked against threat model |
| 5 - Optimized | Continuously refined with full environment-specific tuning | 100+ rules; >70% ATT&CK coverage; continuous gap analysis and automated coverage tracking |

### Ruleset Management and Maintenance

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No formal management; rules live in SIEM without version control | <20% under version control |
| 2 - Repeatable | Some rules in version control; basic but incomplete documentation | 20-50% in version control |
| 3 - Defined | Most rules in version control with documentation standards; DaC being adopted | 50-80% in version control with documentation |
| 4 - Managed | Detection-as-code standard; CI/CD for deployment; all documented and versioned | 80-90% in DaC pipeline; automated deployment |
| 5 - Optimized | Fully automated lifecycle with CI/CD, automated testing, continuous validation | 100% DaC; automated testing/deployment; weekly validation |

### Telemetry Quality

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No active telemetry management; data sources unassessed | <30% of rule types have adequate telemetry |
| 2 - Repeatable | Some awareness of gaps; basic health checks on critical sources | 30-50% adequate telemetry; basic health checks |
| 3 - Defined | Actively monitored; data source coverage mapped to detection needs | 50-70% coverage; CTI integration beginning |
| 4 - Managed | Comprehensive with automated monitoring, CTI enrichment, proactive gap ID | 70-90% coverage; automated monitoring; CTI integrated |
| 5 - Optimized | Advanced workflows with real-time enrichment and automated remediation | 90-100% coverage; real-time enrichment; automated gap remediation |

### Threat Landscape Review

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No regular reviews; priorities not informed by current threats | No scheduled reviews; <30% rules aligned |
| 2 - Repeatable | Bi-annual or annual reviews; some updates based on major changes | 1-2 reviews/year; some rule updates |
| 3 - Defined | Quarterly reviews with documented findings; roadmap updated accordingly | Quarterly; 50-70% rules reviewed against current threats |
| 4 - Managed | Monthly reviews integrated with threat intelligence; continuous alignment | Monthly; 70-90% aligned; automated intel integration |
| 5 - Optimized | Real-time monitoring with automated intel feeds driving priority updates | Continuous; 90-100% alignment; automated updates |

### Product Owner Engagement

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No engagement with product/platform owners | Zero structured engagements |
| 2 - Repeatable | Occasional ad hoc engagement, reactive to issues | 1-2 per quarter; reactive only |
| 3 - Defined | Regular engagement to communicate needs and provide feedback | Quarterly structured engagements; feature requests tracked |
| 4 - Managed | Proactive partnership; detection requirements on product roadmaps | Monthly; >50% requests on product roadmap |
| 5 - Optimized | Continuous proactive engagement; joint planning and shared metrics | >90% requirements reflected in roadmap changes |

### Release Testing and Validation

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No formal testing before deployment | <20% of rules tested |
| 2 - Repeatable | Basic manual testing on some rules; no standardized process | 20-40% tested; manual only |
| 3 - Defined | Standardized testing with defined test cases; staging environment | 50-70% tested; staging environment |
| 4 - Managed | Comprehensive testing with unit, integration, and emulation-based validation | 70-90% automated; 24-hour critical deployment capability |
| 5 - Optimized | Continuous automated testing; full CI/CD with pre-deployment validation | 90-100% automated; continuous CI/CD validation |

---

## Tier 2: Intermediate

Focuses on improving detection quality through tuning, gap analysis, and systematic internal validation.

### False Positive Tuning and Reduction

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | Minimal or no tuning; high FP rates accepted as normal | No measurable FP reduction |
| 2 - Repeatable | Some reactive tuning when analysts complain; no systematic tracking | 10-25% FP reduction; sporadic tuning |
| 3 - Defined | Regular tuning cycles with tracked FP rates per rule | 25-50% FP reduction; quarterly cycles; per-rule tracking |
| 4 - Managed | Comprehensive FP management with automated tuning suggestions and risk scoring | >50% FP reduction; automated recommendations; risk scoring |
| 5 - Optimized | Automated dynamic tuning with ML; near-zero unnecessary noise | >75% FP reduction; ML-assisted; continuous optimization |

### Gap Analysis and Documentation

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No gap analysis; coverage gaps unknown and undocumented | Zero gaps formally documented |
| 2 - Repeatable | Some gaps identified informally after incidents | 1-3 gaps documented; reactive only |
| 3 - Defined | Regular analysis against ATT&CK; gaps documented, prioritized, communicated | 5+ gaps documented quarterly; prioritized |
| 4 - Managed | Comprehensive analysis integrated with threat modeling and risk assessment | Continuous tracking; integrated into roadmap |
| 5 - Optimized | Automated analysis using advanced analytics; real-time coverage mapping | Automated continuous analysis; real-time dashboards |

### Internal Testing and Validation

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No internal testing of detection effectiveness | Zero testing activities |
| 2 - Repeatable | Occasional manual testing of high-priority rules | <40% emulation coverage; sporadic |
| 3 - Defined | Regular testing with attack emulation; results documented | 40-70% emulation coverage; quarterly cycles |
| 4 - Managed | Comprehensive with automated emulation and purple team exercises | 70-90% automated coverage; regular purple team |
| 5 - Optimized | Continuous automated testing with full emulation and regression | >90% automated; continuous validation; regression testing |

---

## Tier 3: Advanced

Addresses false negatives, external validation, and advanced threat coverage to ensure detections catch real attacks.

### False Negative Triage

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No process for identifying FNs; missed detections only found during IR | Zero FN reduction activities |
| 2 - Repeatable | Some FNs identified through post-incident reviews; basic tracking | 50% of tested samples trigger expected alerts |
| 3 - Defined | Systematic FN identification through regular testing; root causes analyzed | 70-90% trigger rate; root cause analysis documented; 30-50% FN reduction from baseline |
| 4 - Managed | Comprehensive with automated validation, coverage testing, rapid remediation | 90-100% trigger rate; automated validation; >50% FN reduction |
| 5 - Optimized | Continuous automated FN detection with real-time validation | Continuous validation; near-zero FN on tested scenarios; >75% FN reduction |

### External Validation

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No external validation of detection capabilities | Zero external exercises |
| 2 - Repeatable | Occasional external validation; typically annual pentest | 1 exercise per year |
| 3 - Defined | Regular external validation through red team or third-party assessments | >1 per year; findings drive improvements |
| 4 - Managed | Multiple exercises annually (red/purple team, breach simulation) | Multiple per year; >70% findings remediated in 30 days |
| 5 - Optimized | Continuous BAS tools and regular adversary emulation | Continuous BAS; regular emulation; real-time feedback |

### Advanced TTP Coverage

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No advanced TTP coverage; signatures and basic indicators only | Zero advanced TTP detections |
| 2 - Repeatable | Limited coverage of 1-3 advanced techniques | 1-3 advanced TTP detections |
| 3 - Defined | Growing coverage informed by intel; behavioral detections supplement signatures | 3-5 advanced TTP detections; behavioral capabilities |
| 4 - Managed | Comprehensive coverage of evasion techniques, novel chains, emerging threats | 5+ advanced TTP detections; evasion/novel coverage |
| 5 - Optimized | Continuous proactive coverage using AI/ML for anomaly detection | Real-time; AI/ML-assisted; automated emerging threat coverage |

---

## Tier 4: Expert

Features proactive threat hunting, advanced automation, AI/LLM integration, and continuous improvement across the detection lifecycle.

### Threat Hunting in Telemetry

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No proactive hunting; all detection is passive through deployed rules | Zero hunting activities |
| 2 - Repeatable | Occasional ad hoc hunting; findings not systematically converted | Bi-weekly; <30% findings converted to rules |
| 3 - Defined | Regular structured hunting driven by intelligence; findings feed detections | Weekly; 50-70% findings integrated into rules |
| 4 - Managed | Comprehensive daily program with advanced analytics and systematic integration | Daily; >90% findings integrated; advanced analytics |
| 5 - Optimized | Automated real-time hunting augmented by AI/ML | Real-time; AI-assisted hypothesis generation |

### Automation and Continuous Improvement

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No automation; all processes manual | Zero automation |
| 2 - Repeatable | Basic automation of some repetitive tasks (e.g., deployment scripts) | <30% of routine tasks automated |
| 3 - Defined | Significant lifecycle automation including AI-based quality checks on new rules; continuous improvement defined | 40-60% automated; AI quality checks on new rules; improvement metrics tracked |
| 4 - Managed | Advanced automation covering most of lifecycle; AI/LLM tools in use | 70-80% automated; AI/LLM for optimization |
| 5 - Optimized | Full AI/LLM integration throughout lifecycle | >90% automated; 40%+ FP reduction via AI; full AI lifecycle |

---

## Enrichment: People & Organization

Assesses the human and organizational factors enabling effective detection engineering.

### Team Structure and Dedicated Roles

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No dedicated roles; detection work is a side task | Zero dedicated FTEs |
| 2 - Repeatable | Partial responsibility assigned; no formal team structure | Part-time; no dedicated team |
| 3 - Defined | Dedicated role(s) or team established with clear responsibilities | At least 1 dedicated FTE; defined role |
| 4 - Managed | Established team with domain experts (host, network, cloud, app) | Multi-person team; domain specialization; career ladder |
| 5 - Optimized | Mature team with deep specialization, mentorship, and strategic influence | Full team; mentorship program; strategic influence |

### Skills Development and Training

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No formal training; learning is self-directed without support | Zero training budget or programs |
| 2 - Repeatable | Some ad hoc training; no structured program | Occasional training; no structured program |
| 3 - Defined | Defined training program covering core skills; regular knowledge sharing | Annual plan; regular sharing; defined skill requirements |
| 4 - Managed | Comprehensive training with cross-training and certification support | Advanced program; cross-training; certification support |
| 5 - Optimized | Continuous learning culture with community contribution and research | Continuous development; community contribution; research |

### Leadership Commitment and Executive Sponsorship

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No executive awareness or sponsorship | Zero executive engagement |
| 2 - Repeatable | Some leadership awareness but no formal sponsorship or budget | Informal awareness; no dedicated budget |
| 3 - Defined | Executive sponsor identified; dedicated budget; function recognized | Dedicated budget; sponsor; formally recognized |
| 4 - Managed | Strong support with metrics reported to leadership; influences investments | Regular executive reporting; metrics-driven investments |
| 5 - Optimized | Strategic priority championed by leadership across the organization | Board-level visibility; cross-org influence |

---

## Enrichment: Process & Governance

Assesses process maturity and governance supporting detection engineering.

### Detection Lifecycle Workflow

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No defined lifecycle; no structured workflow | No documented process |
| 2 - Repeatable | Basic lifecycle covering creation and deployment only | Partial lifecycle; 2-3 stages |
| 3 - Defined | Full lifecycle: request, development, review, testing, deployment, monitoring, retirement | Full lifecycle documented; all stages followed |
| 4 - Managed | Enforced through tooling/automation; SLAs defined; metrics tracked | Automated enforcement; SLAs; cycle time tracked |
| 5 - Optimized | Optimized with automated transitions and predictive analytics | Fully automated; predictive analytics; continuous optimization |

### Metrics and KPI Tracking

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | No metrics tracked; success is anecdotal | Zero KPIs defined or tracked |
| 2 - Repeatable | Basic metrics tracked informally (rule count, alert volume) | 1-2 basic metrics; informal tracking |
| 3 - Defined | Defined KPIs for coverage, quality, velocity; regular reporting | 3-5 KPIs; quarterly reporting; dashboards |
| 4 - Managed | Comprehensive program with automated collection and trending | 5+ KPIs; automated collection; metrics-driven decisions |
| 5 - Optimized | Advanced analytics with predictive metrics and benchmarking | Predictive analytics; benchmarking; data-driven optimization |

### Cross-Team Collaboration

| Level | Qualitative | Quantitative |
|-------|-------------|--------------|
| 1 - Initial | Operates in isolation; no structured collaboration | Zero structured cross-team interactions |
| 2 - Repeatable | Ad hoc collaboration, reactive to incidents or requests | Occasional reactive collaboration |
| 3 - Defined | Regular collaboration with IR, threat intel, engineering via defined channels | Regular scheduled touchpoints; defined channels |
| 4 - Managed | Deep integration with joint planning, shared objectives, integrated workflows | Joint planning; shared objectives; integrated workflows |
| 5 - Optimized | Seamless cross-functional collaboration with automated information sharing | Fully integrated; automated sharing; shared metrics |

---

## Scoring

- Each criterion is scored 1-5 based on the maturity level descriptions above
- **Per-tier score**: Average of all criteria scores within that tier
- **Overall score**: Weighted average across all tiers and enrichment categories
- **Current tier**: Highest tier where all criteria score >= 3 (Defined)
- See [methodology.md](../docs/methodology.md) for detailed scoring formulas
