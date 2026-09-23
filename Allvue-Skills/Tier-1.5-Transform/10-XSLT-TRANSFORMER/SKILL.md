# XSLT Transformer Skill

**Trigger:** "transform data", "create xslt", "data mapping", "convert xml"  
**Purpose:** Create XSLT transformations to convert and map XML data  
**Status:** Ready for deployment  
**Tier:** Expressions & Transforms (Specialized Universal)

---

## Quick Start

Ask the skill to create transformations:
- "Create XSLT to map Geneva portfolios to Allvue"
- "Transform custodian feed to Allvue format"
- "Build import transformation for CSV"

The skill will:
1. Analyze source format
2. Map to target format
3. Create XSLT template
4. Add transformations
5. Generate test data

---

## What It Does

Answers: "How do I transform XML? How do I map data from one system to another?"

**Inputs:**
- Source format (XML, CSV, JSON structure)
- Target format (Allvue XML schema)
- Field mappings
- Transformation rules

**Outputs:**
- Complete XSLT stylesheet
- Field mapping matrix
- Test data samples
- Usage instructions
- Troubleshooting guide

---

## How It Works

1. **Analyze** — Parse source and target formats
2. **Map** — Create field mappings
3. **Build** — Write XSLT transformations
4. **Test** — Validate with sample data
5. **Deploy** — Ready for production use

---

## Real-World Examples

### Example 1: Geneva to Allvue
```
User: "Map Geneva portfolios to Allvue"
↓
Skill: Source: Geneva XML (PortID, PortName, Ticker)
       Target: Allvue Portfolio (PortfolioGUID, Name, Securities)
       Mappings: 12 (ID→GUID, Name→Name, Tickers→SecurityList)
       XSLT: <xsl:template match="Portfolio">
       Output: transform-geneva.xslt + test data
```

### Example 2: Custodian Feed Transform
```
User: "Transform custodian feed to Allvue"
↓
Skill: Source: Custodian CSV (ISIN, Qty, CostBasis)
       Target: Allvue Position XML
       XSLT: Rows→Elements, Qty formatting, CostBasis calc
       Mappings: 8 fields
```

### Example 3: CSV Import
```
User: "Build import transformation for CSV"
↓
Skill: Source: CSV headers + 1000 rows
       Target: Allvue bulk import format
       Transforms: CSV parse → XML structure
       Validation: ISIN format, Qty > 0
```

---

## Deployment

✅ **Ready for deployment** — 8+ production transformations documented

---

See IMPLEMENTATION.md for technical details.
