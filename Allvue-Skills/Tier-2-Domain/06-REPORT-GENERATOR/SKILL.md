# Report Generator Skill

**Trigger:** "create report", "generate report", "build dashboard"  
**Purpose:** Generate reports with proper DataSource binding and access control  
**Status:** Ready for deployment  
**Tier:** Domain-Specific (Building Layer)

---

## Quick Start

Ask the skill to create a report:
- "Create a Daily Allocations report"
- "Build an Executive Dashboard"
- "Generate Compliance Summary report"

The skill will:
1. Design report structure
2. Bind to DataSources
3. Set role-based access
4. Configure export formats
5. Schedule delivery

---

## What It Does

Answers: "How do I create a report? What DataSources? What access control?"

**Inputs:**
- Report purpose
- Data sources needed
- Export formats (Excel, PDF, HTML)
- Access roles
- Refresh frequency

**Outputs:**
- Report XML configuration
- DataSource bindings
- Role-based access matrix
- Export templates
- Scheduling configuration

---

## How It Works

1. **Design** — Structure report sections and panels
2. **Data** — Bind to required DataSources
3. **Access** — Set role-based permissions
4. **Format** — Configure export options
5. **XML** — Generate configuration

---

## Real-World Examples

### Example 1: Daily Operations Report
```
User: "Create a Daily Allocations report"
↓
Skill: Sections: Portfolio Summary, Trade Details, Allocation Status
       DataSources: [tfnAllocationReport, tfnTradeDetails]
       Roles: Ops Manager (full), Trader (view only)
       Export: Excel, PDF daily @ 6am
       Output: report.xml ready to import
```

### Example 2: Executive Dashboard
```
User: "Build Executive Dashboard"
↓
Skill: Panels: 4 (NAV, Allocation %, Performance, Risk)
       DataSources: [ComplianceMatrix, PerformanceCalc, RiskMetrics]
       Roles: CIO (all), CFO (financials)
       Refresh: Real-time
```

---

## Deployment

✅ **Ready for deployment** — 25+ report templates from 4 clients

---

See IMPLEMENTATION.md for technical details.
