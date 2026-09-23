# Allvue Compliance Architect Skill

**Purpose**: Design compliance rule matrices, scenario tests, and rating methodologies  
**Tier**: Domain-Specific (Tier 2)  
**Use**: Build compliance frameworks for portfolio constraints and regulatory rules

**Depends on**: Object Resolver, Reference Tracer, DataSource Decoder

---

## Input Format

```
Compliance Framework: [string]
Guidelines: [list of investment guidelines/constraints]
Ratings: [optional: rating methodology]
Scenarios: [optional: what-if test cases]
Portfolios: [list of portfolio names to apply rules]
Severity: [Low | Medium | High | Critical]
```

## Examples

```
Framework: "Sector Concentration Limits"
Guidelines:
  - No sector > 25% of AUM
  - Technology sector cap: 20%
  - Finance sector cap: 15%
Scenarios: [market crash scenario, liquidity crisis]
Severity: Critical

Framework: "Credit Quality Requirements"
Ratings: "Moody's Ratings"
Guidelines:
  - Min 80% BBB or above
  - Max 5% Below BB
  - No holdings below B3
Portfolios: [All Conservative Funds]
```

---

## Compliance Framework Design Process

### Step 1: Define Compliance Objectives

Map business requirements to Allvue objects:

```
Objective → Allvue Object Type
├─ Sector limits → ComplianceScenario + RatingRule
├─ Credit quality → RatingMethodology + ComplianceScenario
├─ Counterparty exposure → CompliancePortfolioMatrix
├─ Liquidity requirements → ComplianceTest
├─ Leverage constraints → ComplianceScenarioExpression
└─ Concentration limits → ComplianceRank
```

For each guideline, determine:
- **Type**: Concentration, Credit Quality, Liquidity, Leverage, Other
- **Metric**: What you're measuring (% AUM, rating count, LDT, etc.)
- **Limit**: Upper/lower bound
- **Frequency**: Daily, weekly, monthly
- **Exception Process**: Who approves violations

### Step 2: Design Rating Methodology

Create RatingMethodology for credit assessment:

```
Mapping: Moody's Ratings → Internal Risk Tiers

RatingMethodology Object:
├─ CodeName: "Moodys_Internal_Mapping"
├─ Name: "Moody's to Internal Risk Tier"
├─ RatingRules (ordered by severity):
│  ├─ Aaa → Risk Tier 1 (Minimal risk)
│  ├─ Aa1 → Risk Tier 1
│  ├─ Aa2 → Risk Tier 1
│  ├─ Aa3 → Risk Tier 2 (Low risk)
│  ├─ A1 → Risk Tier 2
│  ├─ A2 → Risk Tier 2
│  ├─ A3 → Risk Tier 3 (Moderate risk)
│  ├─ Baa1 → Risk Tier 3
│  ├─ Baa2 → Risk Tier 3
│  ├─ Baa3 → Risk Tier 4 (Elevated risk)
│  ├─ Ba1 → Risk Tier 4
│  ├─ Ba2 → Risk Tier 4
│  ├─ Ba3 → Risk Tier 5 (High risk)
│  ├─ B1 → Risk Tier 5
│  ├─ B2 → Risk Tier 5
│  ├─ B3 → Risk Tier 5
│  ├─ Caa1 → Risk Tier 6 (Very high risk)
│  ├─ Caa2 → Risk Tier 6
│  ├─ Caa3 → Risk Tier 6
│  └─ Ca/C → Risk Tier 7 (Extreme risk)
└─ Recovery Assumptions: [by tier]
```

### Step 3: Create Compliance Tests

Define ComplianceTest for each guideline:

```
ComplianceTest: "Sector Concentration"
├─ CodeName: "SectorConcentration_Limit"
├─ TestType: Concentration
├─ Frequency: Daily
├─ Rule:
│  └─ For each sector:
│     └─ IF SectorWeight > 25% THEN VIOLATION
├─ Measurement:
│  └─ SectorWeight = SUM(Position.Value where Position.SectorID={SectorID}) / Portfolio.AUM
├─ Limit: 25%
├─ Severity: High
├─ Exception Process:
│  └─ Portfolio Manager approval required
└─ Reporting:
   └─ Daily exception report to Chief Investment Officer
```

For each test:
- Define the metric (SQL calculation)
- Set the threshold
- Define exceptions process
- Specify reporting cadence

### Step 4: Create Compliance Scenarios

Design ComplianceScenario for what-if analysis:

```
ComplianceScenario: "Market Stress Scenario"
├─ CodeName: "MarketStress_20pct_Drop"
├─ Description: "Portfolio stress test with 20% market decline"
├─ ScenarioType: Stress Testing
│
├─ ComplianceScenarioColumn (what we're measuring):
│  ├─ Column1: "Sector_Weight_Stressed"
│  ├─ Column2: "Credit_Quality_Post_Stress"
│  └─ Column3: "Leverage_Ratio_Stressed"
│
├─ ComplianceScenarioDataSource (data source):
│  └─ "PortfolioHoldingsWithStress"
│
├─ ComplianceScenarioDataObject (objects involved):
│  ├─ Portfolio
│  ├─ Position
│  └─ Asset
│
├─ ComplianceScenarioExpression (calculation logic):
│  └─ MarketValueStressed = CurrentMarketValue * 0.80
│
├─ ComplianceScenarioTable (output table):
│  └─ Results table with columns: [Portfolio, Sector, StressedWeight, Compliant]
│
└─ ComplianceScenarioResults:
   ├─ Stored in: [Compliance].[ComplianceScenarioTable]
   └─ Query: Refresh daily after market close
```

### Step 5: Build Compliance Matrix

Create CompliancePortfolioMatrix:

```
CompliancePortfolioMatrix: "Global Fund Guideline Matrix"
├─ Row: Guideline/Test
├─ Column: Portfolio
├─ Value: Limit (or Status)

Example:

                    Fund1    Fund2    Conservative   Growth
                    -----    -----    -----------    ------
Sector Conc         25%      30%      20%            35%
Credit Quality      BBB-     BBB      BBB+           BB+
Max Single Issue    5%       10%      3%             8%
Leverage Ratio      2.0x     2.5x     1.5x           3.0x
Liquidity Req       95%      90%      98%            85%
```

Map each to CompliancePortfolioMatrixModifier:

```
Modifier: "Conservative Fund - Tighter Sector Limit"
├─ Portfolio: "Conservative Fund"
├─ ComplianceTest: "Sector Concentration"
├─ OriginalLimit: 25%
├─ ModifiedLimit: 20%
├─ Rationale: "Conservative mandate requires lower concentration"
├─ ApprovedBy: Chief Investment Officer
└─ EffectiveDate: 2026-01-01
```

### Step 6: Define Discount & Long-Dated Logic

Handle special securities:

```
DiscountLogic: "Collateral Haircut Rules"
├─ Security Type: Bond
├─ Credit Rating: BBB
├─ Haircut: 5%
│
└─ Applied in:
   ├─ Collateral calculations
   ├─ Compliance tests (adjusted for haircut)
   └─ Liquidity stress scenarios

LongDatedLogic: "Holdings > 5 Years"
├─ Definition: Maturity > 5 years from today
├─ Haircut: 10%
│
└─ Applied in:
   ├─ Interest rate risk calculations
   ├─ Liquidity assessments
   └─ Duration-constrained portfolios
```

### Step 7: Map to Ratings

Create RatingRule for specific constraints:

```
RatingRule: "Min Quality Requirement"
├─ CodeName: "MinQuality_BBB"
├─ RatingMethodology: "Moody's Internal Mapping"
├─ TargetRating: Baa2 (BBB equivalent)
├─ Rule: 
│  └─ IF Asset.Rating < Baa2 THEN CountAgainstLimit
├─ Limit: Max 5% of portfolio below BBB
└─ Action: Exception triggers if exceeded
```

### Step 8: Generate Compliance Events

Define ComplianceEventType for violations:

```
ComplianceEventType: "Guideline Violation"
├─ CodeName: "Violation_SectorConcentration"
├─ Name: "Sector Concentration Limit Exceeded"
├─ Severity: High
├─ Rules:
│  └─ IF SectorWeight > 25% THEN GenerateEvent
├─ Notification:
│  ├─ To: Portfolio Manager, Compliance Officer
│  ├─ Frequency: Daily (if violation persists)
│  └─ Escalation: If > 35% for > 5 days
└─ Resolution:
   ├─ Manual approval required
   ├─ Auto-resolve if brought under limit
   └─ Document exception reason
```

### Step 9: Set Portfolio Compliance Settings

Apply rules to specific portfolios:

```
PortfolioComplianceSetting: "Fund1 Compliance Rules"
├─ Portfolio: "AllVue ClearPar Fund 1"
├─ Active Compliance Tests:
│  ├─ Sector Concentration (25% limit)
│  ├─ Credit Quality (min BBB)
│  └─ Leverage (max 2.0x)
├─ Override Tests:
│  └─ [none]
├─ Rating Methodology: Moody's Internal
└─ Daily Compliance Check: Enabled
```

### Step 10: Generate Reporting

Create Report for compliance monitoring:

```
Report: "Daily Compliance Exception Report"
├─ DataSource: "ComplianceExceptionDataSource"
├─ Frequency: Daily, 8:00 AM
├─ Recipients: 
│  ├─ Chief Investment Officer
│  ├─ Compliance Officer
│  └─ Portfolio Managers
├─ Fields:
│  ├─ Portfolio
│  ├─ Guideline
│  ├─ CurrentValue
│  ├─ Limit
│  ├─ Status (Compliant/Exception)
│  ├─ DaysInException
│  └─ RequiredAction
└─ Export: Excel, PDF, email
```

---

## Output Format

```markdown
# Compliance Framework: {FrameworkName}

## Executive Summary
- **Name**: {FrameworkName}
- **Type**: {Type: Sector | Credit | Liquidity | Leverage | Combined}
- **Portfolios Affected**: {PortfolioList}
- **Severity**: {Severity}
- **Implementation**: {Draft | Ready for Approval | Approved}

## Compliance Objectives ({N} guidelines)

1. **Sector Concentration**
   - Guideline: No sector > 25% of AUM
   - Measurement: SectorWeight = SectorValue / PortfolioAUM
   - Exception: Portfolio Manager approval
   - Severity: High

2. **Credit Quality**
   - Guideline: Min 80% BBB or above
   - Measurement: RatingWeight = COUNT(Holdings where Rating >= BBB) / COUNT(All Holdings)
   - Exception: Chief Investment Officer approval
   - Severity: Critical

3. [Additional guidelines...]

## Rating Methodology: {MethodologyName}

| Moody's Rating | Internal Tier | Risk Level | Recovery Assumption |
|---|---|---|---|
| Aaa | 1 | Minimal | 100% |
| Aa1-Aa3 | 1 | Minimal | 100% |
| A1-A3 | 2 | Low | 95% |
| Baa1-Baa3 | 3 | Moderate | 85% |
| Ba1-Ba3 | 4 | Elevated | 70% |
| B1-B3 | 5 | High | 50% |
| Caa+ | 6 | Very High | 30% |
| Ca/C | 7 | Extreme | 10% |

## Compliance Tests ({N} tests)

### Test 1: Sector Concentration
- **Type**: ComplianceTest
- **CodeName**: SectorConcentration_Limit
- **Metric**: SectorWeight = SUM(Position.Value) / Portfolio.AUM
- **Limit**: 25% per sector
- **Frequency**: Daily
- **Reporting**: Daily exception report
- **Query**: 
\`\`\`sql
SELECT Portfolio, Sector, SectorWeight, 
  CASE WHEN SectorWeight > 0.25 THEN 'VIOLATION' ELSE 'OK' END as Status
FROM ComplianceResults
WHERE TestName = 'SectorConcentration'
\`\`\`

### Test 2: Credit Quality
- **Type**: ComplianceTest
- **Metric**: % Holdings >= BBB rating
- **Limit**: Min 80%
- **Frequency**: Daily

### Test 3: [Additional tests...]

## Compliance Scenarios ({N} scenarios)

### Scenario 1: Market Stress (20% Drop)
- **CodeName**: MarketStress_20pct_Drop
- **Description**: Portfolio response to 20% market decline
- **Data Sources**: PortfolioHoldingsWithStress
- **Measurements**:
  - New sector weights post-stress
  - Credit quality change
  - Leverage ratio increase
- **Expected Duration**: 1-5 days for market recovery
- **Action Triggers**:
  - If Leverage > 3.0x then trigger margin call protocol
  - If Credit Quality < 70% then reassess concentration

### Scenario 2: [Additional scenarios...]

## Portfolio Compliance Matrix

| Guideline | Fund1 | Fund2 | Conservative | Growth |
|-----------|-------|-------|-------------|--------|
| Sector Conc | 25% | 30% | 20% | 35% |
| Credit Quality | BBB- | BBB | BBB+ | BB+ |
| Max Single | 5% | 10% | 3% | 8% |
| Leverage | 2.0x | 2.5x | 1.5x | 3.0x |
| Liquidity | 95% | 90% | 98% | 85% |

## Special Security Rules

### Discount Logic
- **Bond Haircut (Credit Rating)**: 5% for BBB securities
- **Long-Dated Haircut**: 10% for maturities > 5 years
- **Collateral Haircut**: 15% for illiquid holdings

### Long-Dated Logic
- **Definition**: Holdings maturing > 5 years
- **Count**: {N} positions in portfolio
- **Impact**: Interest rate risk + 10% haircut in liquidity calculations

## Compliance Events

| Event | Trigger | Notification | Escalation |
|-------|---------|--------------|-----------|
| Sector Violation | Weight > 25% | PM, Compliance | If > 5 days |
| Credit Downgrade | Rating drops | PM, CIO | If < BBB |
| Leverage Breach | Ratio > 2.0x | Treasurer | Immediate |

## Implementation Roadmap

1. [ ] **Week 1**: Define all ComplianceTest objects
2. [ ] **Week 2**: Create ComplianceScenario simulations
3. [ ] **Week 3**: Build RatingMethodology mapping
4. [ ] **Week 4**: Configure PortfolioComplianceSetting per fund
5. [ ] **Week 5**: Generate Report templates
6. [ ] **Week 6**: UAT compliance monitoring
7. [ ] **Week 7**: User training and go-live

## Approval & Signoff

- [ ] Investment Committee Review
- [ ] Compliance Officer Approval
- [ ] Chief Investment Officer Sign-off
- [ ] Implementation Team Ready

## Related Objects

**Uses Allvue Components**:
- RatingMethodology: {Name}
- ComplianceScenario: {ScenarioList}
- ComplianceTest: {TestList}
- PortfolioComplianceSetting: {SettingList}

**Referenced By**:
- Report: Compliance Exception Report
- DataPanel: Compliance Dashboard
- Workflow: [Optional approval workflows]

---

This skill answers: **"How do I build a compliance framework?"**
