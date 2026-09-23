# Configuration Cloner Skill

**Trigger:** "clone config", "duplicate configuration", "copy portfolio setup"  
**Purpose:** Clone object configurations with reference adjustments  
**Status:** Ready for deployment  
**Tier:** Integration (Complex Multi-Step)

---

## Quick Start

Ask the skill to clone a configuration:
- "Clone Fund 1 to Fund 2"
- "Duplicate Bond workflow for Equity"
- "Copy compliance rules to new portfolio"

The skill will:
1. Identify all references
2. Clone the configuration
3. Adjust references to new object
4. Generate import package
5. Create validation scripts

---

## What It Does

Answers: "How do I duplicate a configuration? How do I adjust references?"

**Inputs:**
- Source object name
- Target name
- Object type
- Reference adjustments needed

**Outputs:**
- Cloned XML configuration
- Import package (ready to load)
- Validation scripts
- Broken reference report
- Step-by-step instructions

---

## How It Works

1. **Export** — Extract source object XML
2. **Clone** — Create copy with new ID/name
3. **Adjust** — Update all internal references
4. **Validate** — Check for broken refs
5. **Package** — Create import-ready output

---

## Real-World Examples

### Example 1: Clone Portfolio
```
User: "Clone Fund 1 to Fund 2"
↓
Skill: Source: Fund 1 portfolio (47 objects)
       Clone: All workflows, compliance, reports
       Refs Updated: 89 internal references
       New Objects: 47 (all renamed)
       Output: import_fund2.xml + validation script
```

### Example 2: Duplicate Workflow
```
User: "Duplicate Bond workflow for Equity"
↓
Skill: Source: BondTradingWorkflow
       New: EquityTradingWorkflow
       Refs Updated: 12 (validation rules, roles)
       Data: [New DataSources, New field mappings]
       Output: workflow_equity.xml
```

---

## Deployment

✅ **Ready for deployment** — Tested on 4 production clients

---

See IMPLEMENTATION.md for technical details.
