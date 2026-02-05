# RTFTI Protocol Documentation

## 📖 What is RTFTI?

**Real-Time Financial Trust Infrastructure (RTFTI)** is a protocol that transforms raw financial data from MSMEs into a standardized, verifiable trust score. It bridges the information asymmetry between small businesses, financial institutions, and regulators.

**The Problem:** MSMEs struggle to access formal credit because banks cannot efficiently verify their financial health. Traditional audits are expensive, slow, and periodic.

**The Solution:** RTFTI creates a continuous, automated trust pipeline that processes real-time financial data through 5 layers to produce an objective Financial Trust Score (FTS).

---

## 🏗️ Protocol Architecture

### Layer 1: Data Sources

| Source | Description | Data Type |
|--------|-------------|-----------|
| **General Ledger (GL)** | Daily journal entries | Debits, credits, accounts, dates |
| **Bank Statements** | Transaction records | Deposits, withdrawals, balances |
| **GST Returns** | Tax filings | Invoice details, tax collected, input credits |
| **Payroll Records** | Employee data | Salaries, PF contributions, ESI |

*In production:* Connected via APIs to Tally, banking portals, GST portal, payroll software.

---

### Layer 2: Ingestion Gateway

- Connects to all configured data sources
- Validates data format and completeness
- Counts records and checks connectivity
- Flags missing or corrupted data streams

**Metrics:**
- Total records ingested
- Sources connected
- Data freshness

---

### Layer 3: Normalization Engine

- Maps diverse data formats to unified schema
- Standardizes date formats, currency, account codes
- Deduplicates records across sources
- Calculates coverage: `unique_entities / total_records`

**Output:** Normalized dataset ready for validation

---

### Layer 4: Validation Engine

5 validation rules, each producing a score (0-100):

| Rule | What It Checks | Formula | Weight |
|------|----------------|---------|--------|
| **Revenue Integrity** | GL vs Bank vs GST match | `100 - deviation × 2` | 25% |
| **Cash Flow Behaviour** | Inflow/Outflow ratio | `100 - \|ratio-1\| × 100` | 25% |
| **Tax Compliance** | GST filing & match rate | `filed% + match%` | 20% |
| **Payroll Consistency** | PF/ESI compliance | `(pf + esi) / 2` | 15% |
| **Audit Readiness** | Voucher trail completeness | `matched / total` | 15% |

**Status Thresholds:**
- 🟢 **PASS:** score ≥ 80
- 🟡 **WARN:** score 50-79
- 🔴 **ALERT:** score < 50

---

### Layer 5: Trust Output

**Financial Trust Score (FTS):** 0-100

Weighted average of all validation scores:

```python
FTS = (
    revenue_score × 0.25 +
    cashflow_score × 0.25 +
    tax_score × 0.20 +
    payroll_score × 0.15 +
    audit_score × 0.15
)
```

**Confidence:** Based on data completeness and consistency (0-100%)

---

## 🏭 Real-World Implementation

### How to Deploy RTFTI in Production

#### Step 1: Data Source Integration

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Tally/Zoho │     │  Bank APIs  │     │ GST Portal  │     │  Payroll SW │
│   (GL Data) │     │ (Statements)│     │ (Returns)   │     │  (HR Data)  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │                   │
       └───────────────────┴───────────────────┴───────────────────┘
                                   │
                           ┌───────▼───────┐
                           │ RTFTI Gateway │
                           └───────────────┘
```

#### Step 2: API Connections Required

| Source | Integration Method | Data Frequency |
|--------|-------------------|----------------|
| Tally Prime | Tally Connector API | Daily sync |
| Bank | Account Aggregator (AA) / Open Banking | Real-time |
| GST | GST Portal API / GSP | Monthly |
| Payroll | HRMS API (Zoho, GreytHR) | Monthly |

#### Step 3: Continuous Processing

1. Data pulls scheduled every 24 hours (or real-time via webhooks)
2. Validation runs automatically on new data
3. FTS recalculated and timestamped
4. Historical scores stored for trend analysis

---

## 🎯 Use Cases & Stakeholder Benefits

### 🏢 For MSMEs

| Before RTFTI | With RTFTI |
|--------------|------------|
| 45-90 day loan approval | 2-3 day approval |
| High collateral requirements | Reduced collateral needs |
| Expensive CA audits | Continuous compliance monitoring |
| Opaque rejection reasons | Clear improvement guidance |

**Value:** Access to formal credit at better rates

---

### 🏦 For Banks/NBFCs

| Before RTFTI | With RTFTI |
|--------------|------------|
| Manual document verification | Automated verification |
| High NPA risk from information gaps | Real-time risk monitoring |
| Limited MSME portfolio | Expanded MSME lending |
| Expensive due diligence | Behaviour-based pricing |

**Value:** Lower NPAs, larger market

---

### 📊 For Regulators

| Before RTFTI | With RTFTI |
|--------------|------------|
| Periodic audits (annual) | Continuous monitoring |
| Reactive enforcement | Early warning alerts |
| Limited visibility into MSME sector | Sector-wide risk heatmaps |

**Value:** Systemic risk prevention

---

## ⚙️ Technical Specifications

### Data Requirements

- Minimum **3 months** of historical data
- At least **2 data sources** connected
- Data refresh: **Daily** recommended

### Validation Rules in Detail

#### Revenue Integrity
- Compares total credits in GL vs deposits in Bank vs sales in GST
- Deviation > 10% triggers WARN
- Deviation > 25% triggers ALERT

#### Cash Flow Behaviour
- Ratio = Total Inflows / Total Outflows
- Healthy range: 0.85 - 1.15
- Outside range indicates stress

#### Tax Compliance
- Checks GST filing status per month
- Matches invoices to filed returns
- Delays > 30 days reduce score

#### Payroll Consistency
- Verifies PF and ESI compliance percentage
- Checks salary disbursement regularity
- Flags statutory non-compliance

#### Audit Readiness
- Measures voucher trail completeness
- Checks document availability
- GL to Bank reconciliation accuracy

---

## 🚀 Future Roadmap

| Phase | Feature | Status |
|-------|---------|--------|
| v1.0 | Core 5-layer protocol | ✅ Complete |
| v1.1 | Account Aggregator integration | 🔄 In Progress |
| v1.2 | Multi-entity comparison | 📋 Planned |
| v2.0 | ML-based anomaly detection | 📋 Planned |
| v2.1 | Blockchain audit trail | 📋 Planned |
| v3.0 | Cross-border MSME support | 📋 Planned |

---

## 📚 Glossary

| Term | Definition |
|------|------------|
| **FTS** | Financial Trust Score (0-100) |
| **GL** | General Ledger |
| **GST** | Goods and Services Tax |
| **PF** | Provident Fund |
| **ESI** | Employee State Insurance |
| **MSME** | Micro, Small, and Medium Enterprises |
| **NPA** | Non-Performing Asset |
| **AA** | Account Aggregator |

---

## 🔗 References

- [RBI Guidelines on MSME Lending](https://www.rbi.org.in)
- [GST Portal API Documentation](https://www.gst.gov.in)
- [Account Aggregator Framework](https://sahamati.org.in)
- [Tally Integration Guide](https://tallysolutions.com)

---

*RTFTI Protocol v1.0 — Real-Time Financial Trust Infrastructure*
