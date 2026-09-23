# Object Resolver Skill

**Trigger:** "resolve object", "what is", "object lookup"  
**Purpose:** Resolve ANY Allvue object to complete dependency chain  
**Status:** Ready for deployment  
**Tier:** Foundation (Understanding Layer)

---

## Quick Start

Ask the skill to identify an object and understand its relationships:
- "What is the Daily Allocation Report?"
- "Resolve AllocationMethodology"
- "Object lookup for TradeWorkflow"

The skill will:
1. Identify object type
2. Find all object references
3. Show SQL relationships
4. Display usage context
5. List downstream dependents

---

## What It Does

Answers: "What is X? What does it reference? Who uses it?"

**Inputs:**
- Object name (exact or partial)
- Object type (optional)

**Outputs:**
- Object type classification
- 300+ SQL foreign key relationships
- Complete dependency chain
- Usage context (reports, workflows, compliance)
- Client examples from live deployments

---

## How It Works

1. **Identify** — Find object in 170 Allvue types
2. **Reference** — Trace ALL incoming/outgoing references
3. **SQL Map** — Show database table + relationships
4. **Context** — Explain usage in workflows/reports/compliance
5. **Examples** — Show real usage from 4 client deployments

---

## Real-World Examples

### Example 1: Resolve a Report
```
User: "What is Daily Compliance Summary?"
↓
Skill: Type=Report
       DataSources: ComplianceRules, PortfolioMatrix
       References: 5 workflows, 8 compliance rules, 2 roles
       SQL: Views sa_ComplianceSummary, sa_PortfolioMatrix
       Used By: Compliance Manager, Risk Officer
```

### Example 2: Resolve a DataSource
```
User: "Resolve AllocationDataSource"
↓
Skill: Type=DataSource
       SQL Function: fnAllocationReport
       Parameters: [PortfolioID, AsOfDate, AllocationMethod]
       Joins: 4 tables (Allocations, AllocationMethods, Positions, Securities)
       Usage: 12 reports, 3 workflows
```

### Example 3: Resolve a Workflow
```
User: "What is Bond Trading Workflow?"
↓
Skill: Type=Workflow
       Steps: 5 (New Trade, Allocate, Settle, Confirm, Archive)
       Validation Rules: 15 XPath expressions
       References: 2 compliance rules, 3 role assignments
       Used in: Bond portfolio, Fixed Income team
```

---

## Deployment

✅ **Ready for deployment** — Fully documented, tested across 4 client implementations

---

See IMPLEMENTATION.md for technical details.
