# build_artifacts.py
# Transparent pipeline to turn test-cleaned.csv into analysis-ready CSVs
# Author: ChatGPT (2025-09-20)

import pandas as pd
import numpy as np
from pathlib import Path

# -------- Setup --------
# Input CSV must match the one you uploaded earlier
src = Path("test-cleaned.csv")
df = pd.read_csv(src)

base = Path("artifacts")
base.mkdir(parents=True, exist_ok=True)

# -------- 1) Reshape to long format --------
long = df.melt(id_vars=["Page Name"], var_name="ym", value_name="visits")
long["date"] = pd.to_datetime(long["ym"] + "-01")
long["year"] = long["date"].dt.year
long["month_num"] = long["date"].dt.month
long["month_name"] = long["date"].dt.strftime("%b")

long.to_csv(base / "01_long_format.csv", index=False)

# -------- 2) Page × Month stats --------
page_month = (
    long.groupby(["Page Name", "month_num"], as_index=False)
    .agg(
        n_points=("visits", "count"),
        mean_visits=("visits", "mean"),
        median_visits=("visits", "median"),
    )
)
page_month["month_name"] = pd.to_datetime(
    page_month["month_num"], format="%m"
).dt.strftime("%b")
page_month["is_august"] = (page_month["month_num"] == 8).astype(int)

page_month.to_csv(base / "02_page_month_stats.csv", index=False)

# -------- 3) Monthly mean-of-medians --------
per_page_median = (
    long.groupby(["Page Name", "month_num"], as_index=False)["visits"]
    .median()
    .rename(columns={"visits": "per_page_month_median"})
)
agg_medians = (
    per_page_median.groupby("month_num", as_index=False)
    .agg(
        mean_of_medians=("per_page_month_median", "mean"),
        median_of_medians=("per_page_month_median", "median"),
        n_pages=("per_page_month_median", "count"),
    )
)
agg_medians["month_name"] = pd.to_datetime(
    agg_medians["month_num"], format="%m"
).dt.strftime("%b")
agg_medians = agg_medians.sort_values("month_num")

agg_medians.to_csv(base / "03_monthly_mean_of_medians.csv", index=False)

# -------- 4) Per-page August vs All --------
per_page = []
for page, g in long.groupby("Page Name"):
    aug = g[g["month_num"] == 8]["visits"]
    allm = g["visits"]

    aug_mean = aug.mean() if len(aug) > 0 else np.nan
    all_mean = allm.mean() if len(allm) > 0 else np.nan
    mean_diff_pct = (
        (aug_mean - all_mean) / all_mean * 100
        if all_mean and not np.isnan(all_mean)
        else np.nan
    )

    aug_median = aug.median() if len(aug) > 0 else np.nan
    all_median = allm.median() if len(allm) > 0 else np.nan
    med_diff_pct = (
        (aug_median - all_median) / all_median * 100
        if all_median and not np.isnan(all_median)
        else np.nan
    )

    per_page.append(
        {
            "Page": page,
            "n_points_total": len(allm),
            "n_points_august": len(aug),
            "avg_august": aug_mean,
            "avg_all_months": all_mean,
            "aug_vs_all_mean_pct": mean_diff_pct,
            "median_august": aug_median,
            "median_all_months": all_median,
            "aug_vs_all_median_pct": med_diff_pct,
        }
    )

per_page_df = pd.DataFrame(per_page).sort_values("aug_vs_all_mean_pct")
per_page_df.to_csv(base / "04_per_page_august_summary.csv", index=False)

# -------- 5) Site-wide monthly totals by year --------
site_monthly_totals = (
    long.groupby(["year", "month_num"], as_index=False)["visits"].sum()
    .rename(columns={"visits": "site_total"})
)
site_monthly_totals["month_name"] = pd.to_datetime(
    site_monthly_totals["month_num"], format="%m"
).dt.strftime("%b")
site_monthly_totals = site_monthly_totals.sort_values(["year", "month_num"])

site_monthly_totals.to_csv(base / "05_site_monthly_totals_by_year.csv", index=False)

# -------- 6) Site-wide averages across years --------
site_monthly_avg = (
    site_monthly_totals.groupby("month_num")["site_total"]
    .agg(
        avg_total_across_years="mean",
        median_total_across_years="median",
        n_years="count",
    )
    .reset_index()
)
site_monthly_avg["month_name"] = pd.to_datetime(
    site_monthly_avg["month_num"], format="%m"
).dt.strftime("%b")
site_monthly_avg["rank_by_avg_total"] = site_monthly_avg[
    "avg_total_across_years"
].rank(method="min")

site_monthly_avg.to_csv(base / "06_site_monthly_avg_by_month.csv", index=False)

# -------- 7) August totals by year --------
aug_totals = site_monthly_totals[site_monthly_totals["month_num"] == 8].copy()
aug_totals = aug_totals.sort_values("year")
aug_totals.to_csv(base / "07_august_totals_by_year.csv", index=False)

# -------- 8) Jan–Sep cropped series --------
jan_sep_series = agg_medians[agg_medians["month_num"].between(1, 9)].copy()
jan_sep_series.to_csv(base / "08_mean_of_medians_jan_sep.csv", index=False)

# -------- 9) Logic README --------
logic_md = """# Logic & Data Lineage

This folder contains CSVs to audit the analysis.

- 01_long_format.csv — reshaped raw data
- 02_page_month_stats.csv — per page × month mean/median
- 03_monthly_mean_of_medians.csv — aggregate seasonal medians
- 04_per_page_august_summary.csv — August vs all months (mean & median)
- 05_site_monthly_totals_by_year.csv — site totals by year × month
- 06_site_monthly_avg_by_month.csv — average & median totals across years by calendar month
- 07_august_totals_by_year.csv — August totals (site-wide)
- 08_mean_of_medians_jan_sep.csv — cropped Jan–Sep mean-of-medians series

Formulas:
- Per-page monthly median: median of a page’s visits for a given calendar month across years.
- Mean of medians: average of per-page medians for that month.
- August vs All: compares August’s mean/median to all-months mean/median.
- Site-wide totals: sum across all pages for each month.
"""

with open(base / "00_README_logic.md", "w") as f:
    f.write(logic_md)

print("Artifacts written to:", base.resolve())
