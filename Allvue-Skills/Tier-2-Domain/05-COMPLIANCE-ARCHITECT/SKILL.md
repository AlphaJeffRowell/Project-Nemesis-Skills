# Compliance Architect Skill

**Trigger:** "design compliance", "compliance rules", "compliance framework"  
**Purpose:** Design compliance rule matrices, scenario tests, and ratings  
**Status:** Ready for deployment  
**Tier:** Domain-Specific (Building Layer)

---

## Quick Start

Ask the skill to build compliance rules:
- "Set up sector concentration limits"
- "Design credit quality compliance rules"
- "Create portfolio monitoring compliance"

The skill will:
1. Define compliance rules
2. Create scenario tests
3. Set rating methodologies
4. Design portfolio matrices
5. Generate compliance XML

---

## What It Does

Answers: "How do I set up compliance rules? What scenarios? What limits?"

**Inputs:**
- Rule type (concentration, rating, concentration, etc.)
- Thresholds and limits
- Applicable portfolios
- Test scenarios

**Outputs:**
- Compliance rule definitions
- Scenario test matrix
- Rating methodologies
- Portfolio-level compliance matrices
- XML configuration

---

## How It Works

1. **Define** — Create rule types and parameters
2. **Threshold** — Set limits and thresholds
3. **Scenarios** — Create test cases
4. **Matrix** — Build portfolio compliance matrix
5. **XML** — Generate configuration

---

## Real-World Examples

### Example 1: Sector Limits
```
User: "Set up sector concentration limits"
↓
Skill: Rules: Sector weight < 25%
       Methodology: Portfolio % by GICS
       Thresholds: Warning @ 22%, Breach @ 25%
       Scenarios: [Tech 30%, Finance 28%, Healthcare 15%]
       Output: compliance.xml with matrix and tests
```

### Example 2: Credit Quality
```
User: "Design credit quality compliance"
↓
Skill: Rules: Min average rating = BBB
       Methodology: Rating-weighted portfolio value
       Thresholds: Warning @ BBB-, Breach @ BB+
       Tests: [100% AAA, 50% BBB + 50% BB]
```

---

## Deployment

✅ **Ready for deployment** — Based on 4 client compliance frameworks

---

See IMPLEMENTATION.md for technical details.
