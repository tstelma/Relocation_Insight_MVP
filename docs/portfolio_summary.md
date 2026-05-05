# Relocation Insight MVP - Portfolio Summary

## 1. Project Title

**Relocation Insight MVP:** Eurostat-based country comparison tool for early-stage relocation research.

## 2. Short Project Summary

Relocation Insight MVP is a data-driven Streamlit application that compares 28 European countries using selected financial and social indicators from Eurostat. The project combines a Python/pandas data pipeline with a compact interactive frontend for country profiles, indicator rankings, comparisons, and historical context.

The app is not a full relocation recommendation engine. It is designed as a transparent research aid for exploring country-level signals before deeper personal, professional, and city-level research.

## 3. Problem / Motivation

Relocation decisions often require comparing many countries across economic pressure, affordability, and income context. Public datasets are available, but they can be difficult to transform into a clear, user-friendly view.

This MVP addresses that gap by turning selected Eurostat indicators into structured insights, current-value comparisons, and historical charts with clear interpretation rules.

## 4. Data Sources

Primary source: **Eurostat**

- HICP data for annual inflation pressure.
- SILC data for housing overburden and poverty risk.
- `ilc_di03` for median equivalised net income in PPS.
- `earn_nt_net` for annual net earnings in PPS for a single person without children earning 100% of average earnings.

Key frontend datasets:

- `data/clean/all_mvp_insights.csv` powers current insight cards, country profiles, Top 5 rankings, and current-value comparison.
- `data/clean/all_mvp_timeseries.csv` powers historical charts.

## 5. Indicators Used

| Indicator | Description | Unit | Interpretation |
|---|---|---|---|
| `inflation_pressure` | Annual inflation rate from Eurostat HICP | % | Lower is better |
| `housing_pressure` | Share of people spending more than 40% of income on housing | % | Lower is better |
| `poverty_pressure` | Share of people below 60% of national median income | % | Lower is better |
| `income_capacity` | Median equivalised net income from Eurostat `ilc_di03` | PPS | Higher is better |
| `net_earnings_capacity` | Annual net earnings from Eurostat `earn_nt_net` for a single person without children earning 100% of average earnings | PPS | Higher is better |

`income_capacity` and `net_earnings_capacity` are not pressure indicators. They provide income and working-person earnings context alongside the three lower-is-better pressure indicators.

## 6. Technical Workflow

1. Configure supported countries and Eurostat datasets.
2. Fetch indicator data from Eurostat.
3. Clean and standardize country-level outputs with Python and pandas.
4. Generate current insight records and historical time-series outputs.
5. Load standardized CSV files into Streamlit.
6. Render country profiles, rankings, comparisons, historical charts, glossary content, and export options.

## 7. Main App Features

- Country Profile with selected country display and real country flag image.
- Key Signals across the three pressure indicators.
- Key Risk Driver based only on pressure indicators.
- Income and earnings capacity section with PPS formatting.
- Top 5 by Indicator with indicator-specific ranks, medals, and flags.
- Compact Country Comparison for current values, including net earnings capacity.
- Historical Trends with time-range controls, including net earnings capacity.
- Cross-country Historical Trend Comparison, including net earnings capacity.
- Searchable Indicator Glossary.
- Methodology notes and MVP disclaimer.
- CSV export for the selected country profile.

## 8. Key Analytical Decisions

- Pressure indicators are treated as lower-is-better.
- `income_capacity` and `net_earnings_capacity` are treated as higher-is-better and displayed in PPS.
- Current insights and historical charts are separated into dedicated CSV outputs.
- Historical charts are factual/contextual only, with no forecast or prediction language.
- Missing historical data is not interpolated.
- Percent indicator changes are treated as percentage points where shown.
- Top 5 rankings are indicator-specific and do not represent an overall relocation ranking.
- The frontend prioritizes compact, readable layouts over spreadsheet-like tables.

## 9. Limitations

- Country-level only; no city or regional analysis yet.
- Does not include full salary modeling, detailed tax/benefit simulation, employment, healthcare, language, culture, lifestyle, immigration, or personal preferences.
- `net_earnings_capacity` is scenario-based and represents one selected worker profile, not all households or professions.
- Does not provide a final relocation recommendation.
- Indicator labels are simplified MVP signals, not full economic diagnostics.
- Historical charts provide context, not trend forecasts.

## 10. Future Roadmap

- Polish Top 5 and Indicator Focus workflows.
- Improve cross-country historical trend comparison.
- Prepare a public-facing case study or LinkedIn project post.
- Add employment or job-market indicators.
- Consider transparent composite scoring later, if methodology remains explainable.

## 11. Tools Used

- Python
- pandas
- Streamlit
- Eurostat REST API
- PyYAML
- CSV-based data outputs
- Git / GitHub
- ChatGPT / Codex
