# Workflow Designer Skill

**Trigger:** "design workflow", "build trading workflow", "workflow builder"  
**Purpose:** Design trade/order workflows for any asset type  
**Status:** Ready for deployment  
**Tier:** Domain-Specific (Building Layer)

---

## Quick Start

Ask the skill to design a workflow for your asset type:
- "Build a Bond Trading workflow"
- "Design an Option Exercise workflow"
- "Create Equity Allocation workflow"

The skill will:
1. Create workflow steps
2. Define state transitions
3. Write validation rules (XPath)
4. Set role access controls
5. Generate XML configuration

---

## What It Does

Answers: "How do I build a trading workflow? What steps? What validations?"

**Inputs:**
- Asset type (Bond, Equity, Option, etc.)
- Required fields
- Workflow steps needed
- Validation rules

**Outputs:**
- Complete workflow XML
- State transition diagram
- Validation rule set (XPath expressions)
- Role-based access control
- Reference to required DataSources

---

## How It Works

1. **Design** — Create workflow states and transitions
2. **Validate** — Define XPath validation rules
3. **Access** — Set role-based permissions
4. **Reference** — Bind to required DataSources
5. **XML** — Generate Allvue configuration

---

## Real-World Examples

### Example 1: Bond Trading Workflow
```
User: "Build a Bond Trading workflow"
↓
Skill: States: New → Allocated → Settled → Confirmed → Archived
       Transitions: 5 (with validators)
       Validations: [SettleDate > TradeDate, Qty > 0, Rate >= 0]
       Roles: Trader (create), Allocator (allocate), Ops (settle)
       Output: workflow.xml with all steps and rules
```

### Example 2: Equity Order Workflow
```
User: "Design Equity Allocation workflow"
↓
Skill: Steps: Quote → Order → Allocate → Confirm
       Validations: [Price in range, Qty matches, Funds available]
       Access: Trader (all), PM (view only)
       DataSources: EquityPrices, PortfolioMatrix
```

---

## Deployment

✅ **Ready for deployment** — Covers all asset types and validated against 4 clients

---

See IMPLEMENTATION.md for technical details.
