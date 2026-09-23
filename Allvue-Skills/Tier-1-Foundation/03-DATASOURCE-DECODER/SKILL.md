# DataSource Decoder Skill

**Trigger:** "decode datasource", "what sql", "datasource lookup"  
**Purpose:** Decode DataSource definitions to SQL signature  
**Status:** Ready for deployment  
**Tier:** Foundation (Understanding Layer)

---

## Quick Start

Ask the skill to understand what data a DataSource queries:
- "What SQL does AA_tfnAllocationReport execute?"
- "Decode AllocationDataSource"
- "What fields come from AllocationWorkflow?"

The skill will:
1. Show the SQL function definition
2. List all parameters required
3. Display returned fields
4. Map SQL joins
5. Show usage across reports/workflows

---

## What It Does

Answers: "What does this DataSource query? What SQL joins occur? What fields does it return?"

**Inputs:**
- DataSource name
- Panel or report using it (optional)

**Outputs:**
- SQL function signature
- Parameter names and types
- JOIN statements with tables
- Field list with data types
- Usage context (reports, workflows, filters)

---

## How It Works

1. **Locate** — Find DataSource definition
2. **Extract** — Parse SQL function
3. **Map** — Identify all joins and tables
4. **Field** — List returned columns
5. **Context** — Show which objects use it

---

## Real-World Examples

### Example 1: Decode a Report DataSource
```
User: "What SQL does AA_tfnAllocationReport execute?"
↓
Skill: Function: [dbo].[fnAllocationReport]
       Parameters: @PortfolioID INT, @AsOfDate DATE, @MethodID INT
       Tables: Allocations, AllocationMethods, Positions, Securities
       Joins: 4 INNER JOINs on ID fields
       Returns: [AllocID, AllocPercent, MethodName, SecurityID, ...]
       Used By: 12 reports, 3 compliance workflows
```

### Example 2: Find Fields Available
```
User: "What fields come from ComplianceDataSource?"
↓
Skill: SQL: fnComplianceMatrix
       Tables: ComplianceRules, PortfolioMatrix, Scenarios
       Returns: [RuleID, RuleName, LimitValue, Threshold, TestResult]
       Filters: Optional Date range, Portfolio filter
       Used in: Compliance Dashboard, Risk Reports
```

---

## Deployment

✅ **Ready for deployment** — Analyzes 1,710+ SQL definitions

---

See IMPLEMENTATION.md for technical details.
