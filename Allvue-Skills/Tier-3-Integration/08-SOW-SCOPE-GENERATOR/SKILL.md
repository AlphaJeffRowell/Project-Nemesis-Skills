# SOW Scope Generator Skill

**Trigger:** "generate sow", "estimate project", "scope project"  
**Purpose:** Generate Statement of Work from client scope  
**Status:** Ready for deployment  
**Tier:** Integration (Complex Multi-Step)

---

## Quick Start

Ask the skill to estimate a project:
- "Estimate project: 5 portfolios, 4 asset classes, 3 integrations"
- "Generate SOW for new fund setup"
- "Scope 10 portfolios with compliance"

The skill will:
1. Calculate object count
2. Estimate effort hours
3. Create timeline breakdown
4. Determine resource plan
5. Generate SOW document

---

## What It Does

Answers: "How much will this cost? How long will it take? What resources do I need?"

**Inputs:**
- Number of portfolios
- Asset classes
- Integrations needed
- Complexity level (Lite/Standard/Advanced)
- Special requirements

**Outputs:**
- Object count breakdown
- Effort estimation (hours)
- Cost estimate ($)
- Timeline (weeks)
- Resource plan (team size/skills)
- SOW document (ready to send)

---

## How It Works

1. **Analyze** — Count objects needed
2. **Estimate** — Calculate effort per object
3. **Schedule** — Build phase timeline
4. **Resource** — Determine team composition
5. **Document** — Generate SOW

---

## Real-World Examples

### Example 1: $1M Project Estimate
```
User: "Estimate: 10 portfolios, 5 asset classes, 4 integrations"
↓
Skill: Objects to Configure: 280
       Effort: 2,100 hours
       Duration: 16 weeks
       Cost: $350,000
       Team: 5 (1 PM, 1 Architect, 3 Dev)
       Output: Executive SOW + detailed breakdown
```

### Example 2: Simple Fund Setup
```
User: "Scope 2 portfolios with basic compliance"
↓
Skill: Objects: 40
       Effort: 200 hours
       Duration: 4 weeks
       Cost: $25,000
       Team: 2 (1 Dev, 1 QA)
```

---

## Deployment

✅ **Ready for deployment** — Validated against 4 real projects

---

See IMPLEMENTATION.md for technical details.
