# Allvue XSLT Transformer Skill

**Purpose**: Create XSLT transformations to convert and map Allvue XML configurations  
**Tier**: Foundation+ (Tier 1.5 - specialized but universal)  
**Use**: Data import/export, XML mapping, configuration transformations, integration workflows

---

## What is XSLT in Allvue?

XSLT (eXtensible Stylesheet Language Transformations) is used to:
1. **Transform XML** from one format to another
2. **Map data** between systems (Allvue ↔ Legacy, API, Custodian)
3. **Export configurations** in different formats
4. **Import configurations** with format conversion
5. **Batch migrate** data across clients or versions

**Real Allvue use cases:**
```
C:\repo\Clients\BDT-MSD\App Exports\*
├─ Allocation Methodology.xml (Allvue format)
├─ Trade Import.xml (Legacy format)
└─ XSLT would convert: Trade Import.xml → Allocation Methodology.xml

Integration workflows:
├─ Geneva data → XSLT → Allvue Portfolio XML
├─ Custodian XML → XSLT → Allvue SubPortfolio XML
└─ Bloomberg JSON → XSLT → Allvue AssetType XML
```

---

## Input Format

```
Transform Type: [Import | Export | Mapping | Migration | Integration]
Source Format: [Allvue XML | Legacy XML | JSON | CSV | Custom]
Target Format: [Allvue XML | Report XML | API JSON | Database]
Scope: [Single object | Batch | Full config | Subset]
Special Rules: [optional: field mappings, calculations, filtering]
```

## Examples

```
Transform Type: Import
Source: Geneva portfolio export (Excel-based XML)
Target: Allvue Portfolio.xml + SubPortfolio.xml
Rules: 
  - Map Geneva FundID → Allvue PortfolioCodeName
  - Map Geneva ShareClass → Allvue SubPortfolio
  - Convert dates: DD/MM/YYYY → YYYY-MM-DD
  - Aggregate: Multiple Geneva records → Single Allvue Portfolio

Transform Type: Export
Source: Allvue Allocation.xml
Target: Legacy OMS import format
Rules:
  - Extract only executed trades (Status='Executed')
  - Map Allvue PortfolioID → Legacy PortNum
  - Convert Quantity to lots (Qty / LotSize)
  - Calculate NetPrice including accrual

Transform Type: Mapping
Source: Custodian SFTP feed (CSV-to-XML)
Target: Allvue Cash Account XML
Rules:
  - Parse CSV to temporary XML
  - Map custodian account # → Allvue CashAccountID
  - Convert currency codes
  - Calculate balances: Available + Pending
```

---

## XSLT Fundamentals

### Basic Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:bms="http://blackmountainsystems.com/ltd/b2b">
  
  <!-- Root template -->
  <xsl:template match="/">
    <!-- Transformation logic here -->
  </xsl:template>
  
  <!-- Named templates -->
  <xsl:template name="TemplateName">
    <!-- Reusable transformation -->
  </xsl:template>
  
</xsl:stylesheet>
```

### Key XSLT Constructs

**1. Copy Elements**
```xml
<!-- Copy all attributes and text -->
<xsl:copy-of select="@*|node()"/>

<!-- Copy specific element -->
<xsl:copy>
  <xsl:apply-templates select="@*|node()"/>
</xsl:copy>
```

**2. Transform Elements**
```xml
<!-- Select element and transform -->
<xsl:value-of select="/Root/Element"/>

<!-- Select with condition -->
<xsl:value-of select="/Root/Element[Status='Active']"/>

<!-- Apply template to matched elements -->
<xsl:apply-templates select="//Trade"/>
```

**3. Loop Through Data**
```xml
<!-- For each element -->
<xsl:for-each select="//Trade">
  <!-- Process each trade -->
  <xsl:value-of select="./Quantity"/>
</xsl:for-each>

<!-- Apply template for each matched element -->
<xsl:apply-templates select="//Holdings" mode="processHolding"/>
```

**4. Conditionals**
```xml
<!-- If condition -->
<xsl:if test="/Trade/Status='Executed'">
  <!-- This trade is executed -->
</xsl:if>

<!-- If-else condition -->
<xsl:choose>
  <xsl:when test="/Trade/AssetType='Bond'">
    <!-- Bond processing -->
  </xsl:when>
  <xsl:when test="/Trade/AssetType='Equity'">
    <!-- Equity processing -->
  </xsl:when>
  <xsl:otherwise>
    <!-- Other assets -->
  </xsl:otherwise>
</xsl:choose>
```

**5. Variables & Parameters**
```xml
<!-- Define variable -->
<xsl:variable name="totalQty" select="sum(//Trade/Quantity)"/>

<!-- Use variable -->
<xsl:value-of select="$totalQty"/>

<!-- Parameter (passed in) -->
<xsl:param name="exchangeRate" select="1.0"/>
<xsl:value-of select="/Trade/Amount * $exchangeRate"/>
```

**6. String Functions**
```xml
<!-- Substring -->
<xsl:value-of select="substring(/Trade/CodeName, 1, 5)"/>

<!-- Concatenate -->
<xsl:value-of select="concat(/Trade/Fund, '-', /Trade/TradeID)"/>

<!-- Replace -->
<xsl:value-of select="translate(/Trade/Name, ' ', '_')"/>

<!-- Uppercase/Lowercase (XSLT 1.0) -->
<xsl:value-of select="translate(/Trade/Status, 'executed', 'EXECUTED')"/>
```

**7. Number Functions**
```xml
<!-- Sum -->
<xsl:value-of select="sum(//Trade/Quantity)"/>

<!-- Count -->
<xsl:value-of select="count(//Trade[Status='Executed'])"/>

<!-- Rounding (in calculation) -->
<xsl:value-of select="round(/Trade/Price * 100) div 100"/>
```

---

## Common Transformation Patterns

### Pattern 1: Simple Field Mapping

```xml
<!-- Source: Legacy format -->
<!-- 
<LegacyTrade>
  <FundID>ABC123</FundID>
  <TradeQty>1000</TradeQty>
  <Price>98.50</Price>
  <TradeType>BUY</TradeType>
</LegacyTrade>
-->

<!-- XSLT Transform -->
<xsl:template match="LegacyTrade">
  <Trade>
    <PortfolioCodeName>
      <xsl:value-of select="FundID"/>
    </PortfolioCodeName>
    <TradeQuantity>
      <xsl:value-of select="TradeQty"/>
    </TradeQuantity>
    <Price>
      <xsl:value-of select="Price"/>
    </Price>
    <TradeTransactionType>
      <!-- Map BUY → Purchase -->
      <xsl:choose>
        <xsl:when test="TradeType='BUY'">Purchase</xsl:when>
        <xsl:when test="TradeType='SELL'">Sale</xsl:when>
        <xsl:otherwise>Other</xsl:otherwise>
      </xsl:choose>
    </TradeTransactionType>
  </Trade>
</xsl:template>

<!-- Result: Allvue Trade format -->
<!--
<Trade>
  <PortfolioCodeName>ABC123</PortfolioCodeName>
  <TradeQuantity>1000</TradeQuantity>
  <Price>98.50</Price>
  <TradeTransactionType>Purchase</TradeTransactionType>
</Trade>
-->
```

### Pattern 2: Hierarchical Transformation (Flattening)

```xml
<!-- Source: Nested structure -->
<!--
<Portfolio>
  <PortfolioID>Fund1</PortfolioID>
  <SubPortfolios>
    <SubPortfolio>
      <ClassID>ClassA</ClassID>
      <AUM>1000000</AUM>
    </SubPortfolio>
    <SubPortfolio>
      <ClassID>ClassB</ClassID>
      <AUM>500000</AUM>
    </SubPortfolio>
  </SubPortfolios>
</Portfolio>
-->

<!-- XSLT: Flatten to multiple root records -->
<xsl:template match="Portfolio">
  <xsl:for-each select="SubPortfolios/SubPortfolio">
    <FlatRecord>
      <PortfolioID>
        <xsl:value-of select="../../PortfolioID"/>
      </PortfolioID>
      <ClassID>
        <xsl:value-of select="ClassID"/>
      </ClassID>
      <AUM>
        <xsl:value-of select="AUM"/>
      </AUM>
    </FlatRecord>
  </xsl:for-each>
</xsl:template>

<!-- Result: Multiple records -->
<!--
<FlatRecord>
  <PortfolioID>Fund1</PortfolioID>
  <ClassID>ClassA</ClassID>
  <AUM>1000000</AUM>
</FlatRecord>
<FlatRecord>
  <PortfolioID>Fund1</PortfolioID>
  <ClassID>ClassB</ClassID>
  <AUM>500000</AUM>
</FlatRecord>
-->
```

### Pattern 3: Filtering & Conditional Transformation

```xml
<!-- Source: All trades -->
<!--
<Trades>
  <Trade Status="Executed" Qty="100" Price="98.50"/>
  <Trade Status="Pending" Qty="50" Price="98.25"/>
  <Trade Status="Cancelled" Qty="25" Price="0"/>
  <Trade Status="Executed" Qty="200" Price="99.00"/>
</Trades>
-->

<!-- XSLT: Filter to only executed trades, calculate extended price -->
<xsl:template match="Trades">
  <Trades>
    <xsl:for-each select="Trade[Status='Executed']">
      <ExecutedTrade>
        <Quantity>
          <xsl:value-of select="@Qty"/>
        </Quantity>
        <Price>
          <xsl:value-of select="@Price"/>
        </Price>
        <ExtendedPrice>
          <!-- Calculate: Qty * Price -->
          <xsl:value-of select="@Qty * @Price"/>
        </ExtendedPrice>
      </ExecutedTrade>
    </xsl:for-each>
  </Trades>
</xsl:template>

<!-- Result: Only executed trades with calculations -->
<!--
<Trades>
  <ExecutedTrade>
    <Quantity>100</Quantity>
    <Price>98.50</Price>
    <ExtendedPrice>9850</ExtendedPrice>
  </ExecutedTrade>
  <ExecutedTrade>
    <Quantity>200</Quantity>
    <Price>99.00</Price>
    <ExtendedPrice>19800</ExtendedPrice>
  </ExecutedTrade>
</Trades>
-->
```

### Pattern 4: Data Enrichment (Lookup)

```xml
<!-- Source 1: Trades (limited info) -->
<!--
<Trades>
  <Trade TradeID="1" AssetID="100" Qty="1000"/>
  <Trade TradeID="2" AssetID="101" Qty="500"/>
</Trades>
-->

<!-- Source 2: Asset reference data (passed as parameter) -->
<!--
<AssetRef>
  <Asset ID="100" Name="Apple Bond" Type="Bond"/>
  <Asset ID="101" Name="Tech Fund" Type="Equity"/>
</AssetRef>
-->

<!-- XSLT: Enrich trades with asset name -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:param name="assetData"/>
  
  <xsl:template match="Trade">
    <EnrichedTrade>
      <TradeID>
        <xsl:value-of select="@TradeID"/>
      </TradeID>
      <AssetName>
        <!-- Look up asset name by ID -->
        <xsl:value-of select="$assetData//Asset[@ID=current()/@AssetID]/@Name"/>
      </AssetName>
      <Quantity>
        <xsl:value-of select="@Qty"/>
      </Quantity>
    </EnrichedTrade>
  </xsl:template>
</xsl:stylesheet>

<!-- Result: Trades enriched with asset info -->
<!--
<EnrichedTrade>
  <TradeID>1</TradeID>
  <AssetName>Apple Bond</AssetName>
  <Quantity>1000</Quantity>
</EnrichedTrade>
<EnrichedTrade>
  <TradeID>2</TradeID>
  <AssetName>Tech Fund</AssetName>
  <Quantity>500</Quantity>
</EnrichedTrade>
-->
```

### Pattern 5: Date/Time Transformation

```xml
<!-- Source: US date format (MM/DD/YYYY) -->
<!-- <Trade TradeDate="01/15/2026" SettleDate="01/20/2026"/> -->

<!-- XSLT: Convert to ISO format (YYYY-MM-DD) -->
<xsl:template name="convertDate">
  <xsl:param name="inputDate"/>
  <!-- Extract parts: MM/DD/YYYY → YYYY-MM-DD -->
  <xsl:variable name="month" select="substring-before($inputDate, '/')"/>
  <xsl:variable name="day" select="substring-before(substring-after($inputDate, '/'), '/')"/>
  <xsl:variable name="year" select="substring-after(substring-after($inputDate, '/'), '/')"/>
  <xsl:value-of select="concat($year, '-', $month, '-', $day)"/>
</xsl:template>

<xsl:template match="Trade">
  <Trade>
    <TradeDate>
      <xsl:call-template name="convertDate">
        <xsl:with-param name="inputDate" select="@TradeDate"/>
      </xsl:call-template>
    </TradeDate>
  </Trade>
</xsl:template>

<!-- Result: ISO date format -->
<!-- <Trade><TradeDate>2026-01-15</TradeDate></Trade> -->
```

### Pattern 6: Currency Conversion

```xml
<!-- Source: Amounts in USD -->
<!-- <Trade Amount="1000" Currency="USD"/> -->

<!-- XSLT: Convert currencies -->
<xsl:template match="Trade">
  <xsl:variable name="rate">
    <xsl:choose>
      <xsl:when test="@Currency='USD'">1.00</xsl:when>
      <xsl:when test="@Currency='EUR'">1.10</xsl:when>
      <xsl:when test="@Currency='GBP'">1.27</xsl:when>
      <xsl:otherwise>1.00</xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
  
  <ConvertedTrade>
    <OriginalAmount>
      <xsl:value-of select="@Amount"/>
    </OriginalAmount>
    <USDEquivalent>
      <xsl:value-of select="@Amount * $rate"/>
    </USDEquivalent>
  </ConvertedTrade>
</xsl:template>

<!-- Result: Amounts converted to USD -->
```

---

## Real Allvue XSLT Examples

### Example 1: Geneva Portfolio Import

```xml
<!-- Source: Geneva export -->
<!--
<GenevaPortfolios>
  <Fund FundCode="ALT001" FundName="Alternatives Fund 1" BaseCcy="USD">
    <ShareClass Class="A" NAV="1000000" Shares="10000"/>
    <ShareClass Class="B" NAV="500000" Shares="5000"/>
  </Fund>
</GenevaPortfolios>
-->

<!-- XSLT Transformation -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:bms="http://blackmountainsystems.com/ltd/b2b">
  
  <xsl:output method="xml" indent="yes"/>
  
  <!-- Main transformation -->
  <xsl:template match="/">
    <DataImportRequest Type="BMS.LTD.Domain.Portfolio.Portfolio">
      <DataObjectImports>
        <xsl:for-each select="//Fund">
          <DataObjectImport Type="BMS.LTD.Domain.Portfolio.Portfolio">
            <DataProperties>
              <DataProperty Name="CodeName">
                <SimpleDataProperty Value="{@FundCode}"/>
              </DataProperty>
              <DataProperty Name="Name">
                <SimpleDataProperty Value="{@FundName}"/>
              </DataProperty>
              <DataProperty Name="CurrencyType" ReferenceType="ObjectMemberName">
                <DataObjectDataProperty Type="BMS.LTD.Domain.Reference.CurrencyType">
                  <Lookup>
                    <DataProperties>
                      <DataProperty name="CodeName" value="{@BaseCcy}"/>
                    </DataProperties>
                  </Lookup>
                </DataObjectDataProperty>
              </DataProperty>
            </DataProperties>
          </DataObjectImport>
          
          <!-- Also create SubPortfolios for each share class -->
          <xsl:for-each select="ShareClass">
            <DataObjectImport Type="BMS.LTD.Domain.Portfolio.SubPortfolio">
              <DataProperties>
                <DataProperty Name="CodeName">
                  <SimpleDataProperty Value="{../@FundCode}_{@Class}"/>
                </DataProperty>
                <DataProperty Name="Name">
                  <SimpleDataProperty Value="{../@FundName} - Class {translate(@Class, 'ABC', 'Class A|B|C')}"/>
                </DataProperty>
                <DataProperty Name="PortfolioCodeName">
                  <SimpleDataProperty Value="{../@FundCode}"/>
                </DataProperty>
              </DataProperties>
            </DataObjectImport>
          </xsl:for-each>
        </xsl:for-each>
      </DataObjectImports>
    </DataImportRequest>
  </xsl:template>
  
</xsl:stylesheet>

<!-- Output: Allvue Portfolio + SubPortfolio XML ready to import -->
```

### Example 2: Custodian Cash Balance Feed

```xml
<!-- Source: Custodian SFTP feed -->
<!--
<CustodianFeed>
  <CashAccount CustAccountNum="CH-12345" Currency="USD" AvailCash="500000" PendingCash="50000"/>
  <CashAccount CustAccountNum="CH-12346" Currency="EUR" AvailCash="300000" PendingCash="0"/>
</CustodianFeed>
-->

<!-- XSLT: Convert to Allvue CashAccount -->
<xsl:template match="/">
  <DataImportRequest Type="BMS.LTD.Domain.Portfolio.CashAccount">
    <DataObjectImports>
      <xsl:for-each select="//CashAccount">
        <DataObjectImport Type="BMS.LTD.Domain.Portfolio.CashAccount">
          <DataProperties>
            <DataProperty Name="ExternalID">
              <SimpleDataProperty Value="{@CustAccountNum}"/>
            </DataProperty>
            <DataProperty Name="CurrencyID">
              <DataObjectDataProperty Type="BMS.LTD.Domain.Reference.CurrencyType">
                <Lookup>
                  <DataProperties>
                    <DataProperty name="ISOCode" value="{@Currency}"/>
                  </DataProperties>
                </Lookup>
              </DataObjectDataProperty>
            </DataProperty>
            <DataProperty Name="AvailableBalance">
              <SimpleDataProperty Value="{@AvailCash}"/>
            </DataProperty>
            <DataProperty Name="PendingBalance">
              <SimpleDataProperty Value="{@PendingCash}"/>
            </DataProperty>
            <DataProperty Name="TotalBalance">
              <SimpleDataProperty Value="{@AvailCash + @PendingCash}"/>
            </DataProperty>
            <DataProperty Name="LastUpdated">
              <SimpleDataProperty Value="{current-dateTime()}"/>
            </DataProperty>
          </DataProperties>
        </DataObjectImport>
      </xsl:for-each>
    </DataObjectImports>
  </DataImportRequest>
</xsl:template>

<!-- Output: CashAccount records ready to sync -->
```

---

## XSLT Functions Reference

| Function | Example | Result |
|----------|---------|--------|
| **String** | | |
| substring | substring("12345", 1, 3) | "123" |
| concat | concat("A", "-", "B") | "A-B" |
| translate | translate("ABC", "ABC", "XYZ") | "XYZ" |
| normalize-space | normalize-space("  A  B  ") | "A B" |
| **Count/Sum** | | |
| count | count(//Trade) | 42 |
| sum | sum(//Trade/@Quantity) | 10000 |
| **Numeric** | | |
| round | round(3.14159, 2) | 3.14 |
| floor | floor(3.9) | 3 |
| ceiling | ceiling(3.1) | 4 |
| **Logical** | | |
| not() | not(Status='Pending') | true/false |
| boolean() | boolean(Quantity) | true if exists |
| **Node** | | |
| position() | position() | 1, 2, 3... |
| last() | last() | last position |
| current() | current()/@ID | current node value |

---

## XSLT Development Process

### Step 1: Understand Source Format
```xml
Read source data sample and identify:
- Root element name
- Element hierarchy
- Attribute names
- Data types and formats
```

### Step 2: Understand Target Format
```xml
Read target (Allvue) schema and identify:
- Required elements
- Element structure
- Allowed values
- Data type requirements
```

### Step 3: Design Mapping Logic
```
Source → Target mapping:
- Field 1 (Source) → Field A (Target)
- Field 2 (Source) → Field B (Target)
- Calculated field → Field C
- Filtered field → Field D
```

### Step 4: Build XSLT Skeleton
```xml
<xsl:stylesheet version="1.0" ...>
  <xsl:template match="/">
    <!-- Main transformation -->
  </xsl:template>
  <xsl:template name="helperFunction">
    <!-- Reusable functions -->
  </xsl:template>
</xsl:stylesheet>
```

### Step 5: Implement Transformation Logic
```xml
- Add element selection
- Add conditionals
- Add calculations
- Add string/date formatting
- Add filtering
```

### Step 6: Test with Sample Data
```
- Test with valid data
- Test with edge cases
- Test with missing/null values
- Validate XML output against schema
```

### Step 7: Deploy & Monitor
```
- Deploy transformation script
- Monitor import/export jobs
- Handle errors gracefully
- Log transformations
```

---

## Common XSLT Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| "Undefined namespace" | Missing xmlns declaration | Add xmlns:prefix="URI" to stylesheet |
| "Invalid predicate" | Wrong XPath syntax | Use [condition] not [@condition] |
| "Type mismatch" | String vs number | Convert with number() or string() |
| "Element not found" | Wrong element name | Verify against source structure |
| "Null reference" | Element doesn't exist | Add xsl:if test before referencing |

---

## Implementation Checklist

- [ ] Understand source and target formats
- [ ] Design mapping logic
- [ ] Build XSLT stylesheet
- [ ] Test with sample data
- [ ] Handle edge cases
- [ ] Validate output XML
- [ ] Add error handling
- [ ] Document transformation
- [ ] Get business review
- [ ] Deploy to production
- [ ] Monitor execution

---

This skill answers: **"How do I transform XML data between systems and Allvue format?"**
