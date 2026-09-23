# Allvue SOW/Scope Generator Skill

**Purpose**: Generate Statement of Work from client scope (estimate complexity, timelines, cost drivers)  
**Tier**: Integration (Tier 3)  
**Use**: Build SOWs with accurate object count estimates and resource planning

**Depends on**: Object Resolver, Reference Tracer, All domain skills

---

## Input Format

```
Client Name: [string]
Project Type: [Implementation | Enhancements | Migration | Integration]
Scope Inputs:
  - Portfolios: [N]
  - Asset Classes: [list: Bond, Equity, Loan, etc.]
  - Compliance Rules: [N]
  - Reports Needed: [N]
  - Integrations: [list: Geneva, Bloomberg, Custodians, etc.]
  - Users: [N]
  - Deployment: [On-prem | Cloud]
Timeline: [N months]
Module Focus: [IA | FA | FO | Nexius | Multi-module]
```

## Examples

```
Client: "New Alternative Fund Manager"
Type: Implementation
Portfolios: 3
Asset Classes: [Bond, Equity, Loan, Warrant]
Compliance: 8 portfolio constraints
Reports: 12 operational + 4 regulatory
Integrations: [Geneva, Custodian SFTP, Bloomberg]
Users: 25 (3 portfolio managers, 8 analysts, 14 operations)
Timeline: 6 months
Modules: IA + FO + Compliance

→ Generates: Full SOW with resource plan, timeline, cost estimate
```

---

## SOW Generation Process

### Step 1: Map Project Type to Deliverables

Classify engagement and standard deliverables:

```
Project Type Mapping:

IMPLEMENTATION (Greenfield)
├─ Scope: Full platform setup from scratch
├─ Phases: Discovery, Design, Build, Test, Deploy, Support
├─ Duration: 8-12 months typical
├─ Deliverables:
│  ├─ Requirements documents (BRD, TRD)
│  ├─ Design specifications
│  ├─ Configuration XML exports
│  ├─ Integration playbooks
│  ├─ UAT scripts and results
│  ├─ Training materials
│  ├─ Go-live support
│  └─ 90-day post-go-live monitoring
└─ Cost: $500K-$2M+ depending on scope

ENHANCEMENTS (Existing platform)
├─ Scope: Add features/modules to running system
├─ Phases: Design, Build, Test, Deploy
├─ Duration: 2-6 months
├─ Deliverables:
│  ├─ Change specification
│  ├─ Updated XML configurations
│  ├─ Test scripts
│  ├─ Training (delta only)
│  └─ Post-deployment support
└─ Cost: $100K-$500K

MIGRATION (Replace legacy system)
├─ Scope: Move from old system to Allvue
├─ Phases: Data analysis, Mapping, Build, Test, Deploy
├─ Duration: 6-12 months (data-heavy)
├─ Deliverables:
│  ├─ Data migration strategy
│  ├─ Mapping specifications
│  ├─ ETL scripts
│  ├─ Data validation scripts
│  ├─ Reconciliation procedures
│  └─ Legacy system decommission plan
└─ Cost: $400K-$1.5M+

INTEGRATION (Connect to ecosystem)
├─ Scope: Wire up external systems
├─ Phases: Design, Build, Test, Deploy
├─ Duration: 2-4 months per integration
├─ Deliverables:
│  ├─ Integration architecture
│  ├─ API specifications
│  ├─ Event subscription configs
│  ├─ Data mapping documentation
│  └─ Monitoring/alerting setup
└─ Cost: $50K-$200K per integration
```

### Step 2: Calculate Object Counts

Estimate Allvue objects needed based on scope:

```
Estimation Formulas:

PORTFOLIOS:
├─ Base: 1 Portfolio object per fund
├─ Sub-portfolios: Multiply by average share classes (typically 1.5x)
├─ Formula: N_SubPortfolios = N_Portfolios * 1.5
│  └─ Example: 5 portfolios → ~8 sub-portfolios
└─ Related: PortfolioCustom (1), ComplianceSetting (1 per compliance framework)

WORKFLOWS:
├─ Base: 1 workflow per asset class
├─ Variants: CVOS, VOS, AutoTransitions (typically +2 variants per workflow)
├─ Formula: N_WorkflowVariants = N_AssetClasses * 2.5
│  └─ Example: 4 asset classes → ~10 workflow variants
└─ Complexity: Bond > Equity > Loan > Warrant

COMPLIANCE RULES:
├─ ComplianceTest: 2-4 per compliance framework (typically 3)
├─ RatingRule: 1 per rating tier (typically 10-15 for institutional ratings)
├─ ComplianceScenario: 2-5 (stress tests)
├─ Formula: N_Compliance = N_Portfolios * 2 + N_RatingTiers + N_Scenarios
│  └─ Example: 5 portfolios, 12 rating tiers, 3 scenarios → 25 compliance objects

DATA PANELS:
├─ Portfolio Management: 8-10 panels
├─ OMS/Trading: 15-20 panels
├─ Compliance: 5-8 panels
├─ Reporting: 10-15 panels
├─ Admin: 5-8 panels
├─ Formula: N_DataPanels = (8 + 18 + 6 + 12 + 6) + N_CustomPanels
│  └─ Typical: 50-80 data panels

REPORTS:
├─ Operational: 5-8 (daily/ad-hoc)
├─ Compliance: 3-5 (daily/weekly)
├─ Regulatory: 2-4 (monthly/quarterly/annual)
├─ Executive: 2-3 (summary dashboards)
└─ Formula: N_Reports = 5 + 4 + 3 + 2 + N_CustomReports

DATA SOURCES:
├─ Typically 1.5-2x number of reports
├─ Include: Portfolio data, Trade data, Compliance results, Reference data
└─ Formula: N_DataSources = N_Reports * 1.5 + N_Integrations * 3

ROLES & USERS:
├─ Standard Roles: 5-7 (Admin, PM, Analyst, Trader, Operations, Compliance, API)
├─ Custom Roles: +1-3 per client specialization
├─ Users: Assume 60% portfolio managers, 40% operations/support
└─ RoleBasePanel assignments: Multiply by N_DataPanels * N_Roles * 0.3 (selective access)

INTEGRATIONS:
├─ Stock integrations: Geneva, Bloomberg, Custodians, Admin systems
├─ DataSource per integration: 2-4 (inbound, outbound, reference)
├─ EventSubscription per integration: 1-2
└─ Formula: N_IntegrationObjects = N_Integrations * 6
```

### Step 3: Estimate Configuration Effort

Map object counts to development hours:

```
Effort Estimation (hours per object type):

Portfolio Creation:
├─ Simple portfolio: 4-6 hours (just Portfolio object)
├─ Complex (with sub-portfolios, compliance): 8-12 hours per portfolio
└─ Subtotal: 5 portfolios * 10 hours = 50 hours

Workflow Design:
├─ Simple workflow (single asset, one path): 8-10 hours
├─ Complex workflow (multi-asset, branching, validation): 20-30 hours
├─ Each variant (CVOS, VOS): +4 hours
├─ 4 asset classes * 25 hours + 10 variants * 4 hours = 140 hours

Compliance:
├─ ComplianceTest (design, expression, testing): 12-16 hours each
├─ RatingMethodology (mapping, rules): 20-30 hours
├─ ComplianceScenario (complex scenario modeling): 16-24 hours each
├─ 3 tests * 14 + 1 methodology * 25 + 3 scenarios * 20 = 157 hours

Data Panels:
├─ Simple panel (single datasource, no parameters): 2-3 hours
├─ Complex panel (multiple joins, parameters, filters): 6-8 hours
├─ 70 panels avg 5 hours = 350 hours

Reports:
├─ Simple report (template-based): 3-4 hours
├─ Complex report (custom calculations, multi-format): 8-12 hours
├─ 12 reports avg 8 hours = 96 hours

Data Sources:
├─ Simple datasource (existing function): 1-2 hours
├─ Complex datasource (new SQL development): 8-16 hours
├─ 25 datasources avg 6 hours = 150 hours

Integrations (per integration):
├─ API connector: 40-60 hours
├─ File transfer (SFTP, etc.): 20-30 hours
├─ Real-time sync: 60-100 hours
├─ 3 integrations avg 40 hours = 120 hours

Testing & Validation:
├─ Unit testing (per workflow/panel): 2-4 hours
├─ Integration testing: 40-60 hours
├─ UAT preparation & execution: 60-100 hours
├─ Subtotal: 150 hours

TOTAL CONFIGURATION EFFORT: ~1,300 hours (50 + 140 + 157 + 350 + 96 + 150 + 120 + 150 + 137)
```

### Step 4: Calculate Resource Requirements

Map effort to resource needs:

```
Resource Planning:

Total Effort: 1,300 configuration hours + testing + support

Deployment Model:
├─ Waterfall (Traditional): 1 config lead + 2 devs + 1 QA
│  └─ Timeline: 1,300 hours ÷ (1 + 2 + 1) / 40 hrs/week = ~8 weeks
│
├─ Agile (Sprint-based): 1 config lead + 2 devs + 1 QA + 1 BA
│  └─ Timeline: 1,300 hours ÷ (1 + 2 + 1 + 1) / 40 hrs/week = ~6.5 weeks (compressed with parallel work)
│
└─ Blended (Recommended): 1 config lead + 1-2 devs + 1 QA + 0.5 BA (shared)
   └─ Timeline: 8-12 weeks depending on intensity

Team Composition:
├─ Configuration Lead (20% project time)
│  └─ Hours: 1,300 * 0.2 = 260 hours → 6.5 weeks FTE
│
├─ Developer 1 (workflow, compliance)
│  └─ Hours: 500 hours → 12.5 weeks FTE
│
├─ Developer 2 (UI, reporting)
│  └─ Hours: 400 hours → 10 weeks FTE
│
├─ QA/Tester
│  └─ Hours: 200 hours → 5 weeks FTE
│
└─ Business Analyst (shared)
   └─ Hours: 100 hours → 2.5 weeks FTE
```

### Step 5: Build Timeline

Create project phases with milestones:

```
PROJECT TIMELINE: 12 Weeks (3 months)

Phase 1: DISCOVERY & DESIGN (Weeks 1-3)
├─ Week 1: Requirements gathering, workshops
│  └─ Deliverables: Requirements doc, scope statement
├─ Week 2: Design sessions (workflows, compliance, integrations)
│  └─ Deliverables: Design specifications, data model
├─ Week 3: Finalize design, approve with client
│  └─ Deliverables: Approved design doc, resource allocation
└─ Effort: 240 hours (all team)

Phase 2: BUILD - CORE (Weeks 4-7)
├─ Week 4: Portfolio setup, initial workflows
│  └─ Deliverables: 5 portfolios created, 2 workflows drafted
├─ Week 5: Workflow completion, compliance framework
│  └─ Deliverables: All workflows complete, compliance rules defined
├─ Week 6: Data panels and reporting
│  └─ Deliverables: 40 data panels, 6 reports
├─ Week 7: Integrations, final panels
│  └─ Deliverables: Integration test data flowing, 30+ more panels
└─ Effort: 650 hours (developers)

Phase 3: TEST & VALIDATION (Weeks 8-10)
├─ Week 8: Unit testing, integration testing
│  └─ Deliverables: 80% test pass rate
├─ Week 9: UAT kickoff, issue remediation
│  └─ Deliverables: UAT scripts executed, issues logged
├─ Week 10: Issue resolution, final validation
│  └─ Deliverables: 100% test pass rate, UAT sign-off
└─ Effort: 200 hours (all team)

Phase 4: DEPLOY & SUPPORT (Weeks 11-12)
├─ Week 11: Production deployment, user training
│  └─ Deliverables: System in production, training complete
├─ Week 12: Go-live support, issue resolution
│  └─ Deliverables: 7-day support, transition to operations
└─ Effort: 100 hours (support team)

Milestones:
├─ Week 3: Design approved
├─ Week 7: Build phase complete
├─ Week 10: UAT sign-off
└─ Week 11: Go-live
```

### Step 6: Estimate Costs

Calculate resource costs:

```
Cost Estimation:

Labor Costs:
├─ Config Lead: 260 hours * $150/hr = $39,000
├─ Developer 1: 500 hours * $130/hr = $65,000
├─ Developer 2: 400 hours * $130/hr = $52,000
├─ QA/Tester: 200 hours * $100/hr = $20,000
├─ BA (shared): 100 hours * $120/hr = $12,000
└─ Subtotal Labor: $188,000

Infrastructure & Licensing:
├─ Allvue License (3-month trial): $30,000
├─ Development environment: $5,000
├─ UAT environment: $5,000
├─ Testing tools/data: $3,000
└─ Subtotal Infra: $43,000

Travel & Logistics:
├─ Onsite visits (2 weeks): $8,000
├─ Workshops & training materials: $5,000
└─ Subtotal Travel: $13,000

TOTAL PROJECT COST: $244,000

Contingency (20%): $48,800

TOTAL WITH CONTINGENCY: $292,800

Cost Drivers (high-impact factors):
├─ Complexity: Compliance rules increase cost by 40-60%
├─ Integrations: Each real-time integration adds $50-100K
├─ Custom development: Custom SQL/calculations add $20-50K
├─ Data migration: Large legacy migration adds $100-300K
└─ Multi-module: FA + Nexius adds 40% to IA baseline
```

### Step 7: Build SOW Document

Generate comprehensive SOW template:

```
SOW DOCUMENT STRUCTURE:

1. EXECUTIVE SUMMARY
   ├─ Client: {Name}
   ├─ Project: {Type}
   ├─ Duration: {Months}
   ├─ Cost: ${Amount}
   └─ Go-live date: {Date}

2. SCOPE OF WORK
   ├─ What's included:
   │  ├─ Portfolios: {N}
   │  ├─ Workflows: {N}
   │  ├─ Compliance rules: {N}
   │  ├─ Reports: {N}
   │  ├─ Integrations: {N}
   │  └─ Users: {N}
   │
   └─ What's NOT included:
      ├─ Custom code development
      ├─ Multi-year support contracts
      └─ Third-party system modifications

3. DELIVERABLES
   ├─ Phase 1: Requirements, design doc, approved scope
   ├─ Phase 2: Configured portfolios, workflows, compliance
   ├─ Phase 3: All reports, data panels, integrations
   ├─ Phase 4: Test scripts, UAT results, training materials
   └─ Phase 5: Go-live support (7 days)

4. TIMELINE & MILESTONES
   └─ [12-week timeline with dates]

5. RESOURCE PLAN
   ├─ Core Team (full-time): 4 people
   ├─ Client Participation: 10-15 hours/week
   └─ Key roles: Config Lead, 2 Devs, QA

6. COST & PAYMENT TERMS
   ├─ Total: ${Amount}
   ├─ Payment Schedule:
   │  ├─ 25% upon start
   │  ├─ 25% upon design approval
   │  ├─ 25% upon build completion
   │  └─ 25% upon go-live
   └─ Contingency: ${Amount} for scope changes

7. ASSUMPTIONS & DEPENDENCIES
   ├─ Data available by Week 2
   ├─ Client approvals within 3 days
   ├─ Legacy system decommission after 30 days
   └─ No major system changes during project

8. RISK & MITIGATION
   ├─ Risk: Poor data quality → Mitigation: Early data audit
   ├─ Risk: Scope creep → Mitigation: Change control process
   ├─ Risk: Staffing → Mitigation: Resource plan buffer
   └─ Risk: Integration delays → Mitigation: Parallel workstreams

9. SUPPORT & MAINTENANCE
   ├─ Go-live support (included): 7 days
   ├─ Transition support (optional): 30/60/90 day checkpoints
   └─ Post-go-live maintenance (optional): $X/month
```

---

## Output Format

```markdown
# SOW/Scope Generator: {ClientName}

## Project Overview
- **Client**: {ClientName}
- **Project Type**: {Implementation | Enhancement | Migration}
- **Duration**: {N} months
- **Total Cost**: ${Amount}
- **Go-Live Date**: {Date}

## Scope Summary

**What's Included**:
- Portfolios: {N} (with {N} sub-portfolios)
- Workflows: {N} (across {N} asset classes)
- Compliance Rules: {N} tests, {N} scenarios
- Reports: {N} operational, {N} compliance, {N} regulatory
- Data Panels: {N} configured
- Integrations: {N} systems connected
- Users: {N} trained

**What's NOT Included**:
- Custom development beyond scope
- Multi-year support contracts
- Third-party system modifications
- Legacy system decommissioning (scope edge)

## Object Count Estimate

| Object Type | Count | Effort (hrs) | Notes |
|---|---|---|---|
| Portfolio | 5 | 50 | Includes sub-portfolios |
| Workflow | 10 | 140 | 4 asset classes + variants |
| Compliance | 25 | 157 | Tests, scenarios, rules |
| DataPanel | 70 | 350 | UI configuration |
| Report | 12 | 96 | Operational + regulatory |
| DataSource | 25 | 150 | SQL functions/procedures |
| Integration | 3 | 120 | API, file transfer, etc |
| Testing/QA | - | 150 | Validation & UAT |
| **TOTAL** | | **1,300** | |

## Resource Plan

**Core Team**:
- Config Lead (20% project allocation)
- Developer 1 (Workflows, Compliance) - FTE
- Developer 2 (UI, Reporting) - FTE
- QA/Tester - 50% FTE
- Business Analyst (shared) - 20% FTE

**Client Participation Required**: 10-15 hours/week
- Business stakeholder sign-offs
- UAT team (5-8 people)
- Training participants (25 total users)

**Client Responsibility**:
- Data provision (portfolio, holdings, compliance rules)
- System access & credentials
- Approvals & decisions (3-day SLA)
- UAT execution

## Timeline

**Phase 1: Discovery & Design** (Weeks 1-3)
- Requirements gathering
- Design workshops
- Approved design document

**Phase 2: Build** (Weeks 4-7)
- Portfolio & workflow setup
- Compliance framework
- Data panels & reports
- Integration implementation

**Phase 3: Test & Validation** (Weeks 8-10)
- Unit & integration testing
- UAT execution
- Issue remediation

**Phase 4: Deploy & Support** (Weeks 11-12)
- Production deployment
- User training
- 7-day go-live support

**Key Milestones**:
- Week 3: Design approved
- Week 7: Build complete
- Week 10: UAT sign-off
- Week 11: Go-live

## Cost Breakdown

| Category | Cost |
|----------|------|
| Labor (1,300 hrs @ avg $125/hr) | $188,000 |
| Infrastructure & Licensing | $43,000 |
| Travel & Materials | $13,000 |
| **Subtotal** | **$244,000** |
| Contingency (20%) | $48,800 |
| **TOTAL** | **$292,800** |

**Payment Terms**:
- 25% upon contract signature
- 25% upon design approval
- 25% upon build completion
- 25% upon go-live

## Assumptions

- [ ] Data available by Week 2
- [ ] Client provides 2 business stakeholders for weekly meetings
- [ ] System access provisioned by Week 1
- [ ] No major changes to Allvue during project
- [ ] Legacy system operational until 30 days post-go-live

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Data quality issues | High | Early data audit (Week 1) |
| Scope creep | Medium | Change control process, weekly scope review |
| Staffing turnover | Medium | Resource buffer, cross-training |
| Integration delays | Medium | Parallel workstreams, contingency time |
| Compliance complexity | High | Early complexity assessment, design review |

## Cost Drivers

**Increases cost by 40-60%**:
- Extensive compliance rules (20+ tests/scenarios)
- Multi-module implementation (FA, Nexius added to IA)
- Multiple asset classes (5+)

**Increases cost by $50-100K each**:
- Real-time integrations (vs. batch)
- Custom SQL development
- Data migration complexity

## Implementation Sequence

1. Portfolio & Sub-Portfolio creation
2. Workflow design & testing
3. Compliance rule setup
4. Data source development
5. UI panel configuration
6. Report generation
7. Integration implementation
8. Testing & QA
9. User training & go-live

## Support & Maintenance

**Included**:
- 7-day go-live support
- Production issue triage
- Post-launch stabilization

**Optional (Additional Cost)**:
- 30/60/90-day checkpoints: $10K/month
- Ongoing maintenance & enhancements: $15-25K/month
- Managed services (24/7 support): $50K+/month

---

This skill answers: **"How do I estimate scope, cost, and timeline for a project?"**
