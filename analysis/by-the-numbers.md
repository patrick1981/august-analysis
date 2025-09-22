# Library Website Traffic Analysis

**Analysis Date:** September, 22 2025  
**Data Period:** September 2020 – September 2025 (61 months, 5 years)  
**Analyst:** Duff, Patrick T.
**Purpose:** Provide documented justification for August vacation scheduling using website traffic and ticket workload data.

---

## DATA SOURCES

- **Website Traffic**: `5-year-data-cleaned.txt`  
  * 14 service pages × 61 months (Sept 2020–Sept 2025)  
  * Monthly visit counts validated for completeness and accuracy  

- **Ticketing Data**: `ticketstats.csv`  
  * Customer service categories including ILL (“I’m looking for an article/book”), Ask a Librarian, and general inquiries  
  * Extracted and normalized to monthly counts (2016–2025 span, 5-year focus for workload trend)

---

## METHODOLOGY

### Step 1. Data Validation
- Verified **61 months × 14 pages = 854 data points** (traffic)  
- Confirmed continuous monthly sequence  
- Ticket data validated for 10 years, aggregated to monthly/yearly totals  

### Step 2. Data Transformation
- Reshaped traffic data from wide (Page × Month) to long format (Page–Month pairs)  
- Created site-wide totals by summing across pages per month  
- For tickets, extracted August vs. overall monthly counts for workload comparison  

### Step 3. Core Calculations

#### Website Traffic (5 years)
- **Median all months (site-wide):** 8,903 visits/month  
- **Median August (site-wide):** 8,089 visits/month  
- **Reduction:** 814 visits → **−9.1%**

#### Ticket Workload (5 years)
- **Median monthly tickets:** ~350  
- **Median August tickets:** ~143  
- **Reduction:** ~207 tickets → **−59%**

---

## KEY FINDINGS

### Site Traffic Reductions (Page-Level Examples)
- **Home Page:** −9.5% (598 fewer visits)  
- **Databases:** −6.4% (119 fewer visits)  
- **eJournals & eBooks:** −14.3% (73 fewer visits)  
- **Subject Portals:** −8.4% (10 fewer visits)  
- **Ask a Librarian (support page views):** −5.2% (4 fewer visits)

### Ticket Reductions (Service-Level)
- **Ask a Librarian tickets:** ~59% lower in August vs. typical months  
- **Article/Book requests (ILL):** August consistently among lowest intake months  
- **Overall ticket volume:** August ~200 fewer tickets than median → direct workload reduction

---

## VISUALIZATION

A smoothed business cycle chart (Jan–Oct) shows:  
- **Crest:** March–April (peak workload)  
- **Stable shoulder:** April–May (flat around baseline)  
- **Trough:** August (clear dip, −9.1% traffic, −59% tickets)  
- **Excluded Nov–Dec:** staffing volatility offsets low demand  

---

## VALIDATION

- **Cross-method confirmed** (Python pipeline + Excel pivot checks)  
- **Audit trail** maintained with raw data, scripts (`build-artifacts.py`), and artifacts folder  
- **Replicable**: All calculations reproducible from raw source files  

---

## CONCLUSION

**Five years of usage and ticketing data (Sept 2020–Sept 2025) confirm:**

- **Website traffic:** August is **−9.1% below median** (814 fewer visits/month)  
- **Ticket workload:** August is **~59% below median** (~200 fewer tickets/month)  
- **Cross-service validation:** Both technical workload and user demand decline in August  
