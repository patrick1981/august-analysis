# Methods Documentation

## Data Source
- Cleaned CSV (`data/test-cleaned.csv`) derived from site usage logs (2020–2025).

## Analytical Approaches
We applied four complementary methods:

1. **Site-wide Totals**
   - Sum all page visits per month across years.
   - Showed August 2025 was lowest August on record.

2. **Mean of Means**
   - Average each page’s monthly mean, then average across pages.
   - August ~9% below baseline.

3. **Medians**
   - Monthly totals, then median across years.
   - August consistently lower than spring months.

4. **Mean of Medians** (**Primary Method**)
   - Median visits per page/month → averaged across services.
   - Robust to outliers and page size differences.
   - August = 669 (2nd lowest, only December lower at 635).

## Tools
- Python (pandas, matplotlib)
- Excel/Power Query (for data validation)
- Charts saved as PNG
