# Relocation Insight MVP - Project Handoff

**Last Updated:** May 5, 2026  
**Current Stage:** Stage 86 complete. Continue from **Stage 87**.

## 1. Project Overview

Relocation Insight MVP is a Eurostat-based Streamlit app for comparing European countries using early-stage relocation pressure and income-capacity signals.

The app is a decision-support MVP, not a full relocation recommendation engine. It currently helps users compare countries by inflation pressure, housing pressure, poverty pressure, and purchasing-power-adjusted income capacity.

## 2. Current Project Status

The 4-indicator MVP is working end to end:

1. `inflation_pressure`
2. `housing_pressure`
3. `poverty_pressure`
4. `income_capacity`

Current state:

- Eurostat ingestion and MVP pipeline are working.
- Streamlit frontend is working.
- `all_mvp_insights.csv` still powers the current insight cards.
- `all_mvp_timeseries.csv` now powers historical trend charts.
- Frontend has been redesigned toward a more compact, modern, readable experience.
- Historical trend views are available, with time-range controls and outlier context.

## 3. Current MVP Indicators

| Indicator | Source | Metric | Unit | Direction |
|---|---|---|---|---|
| `inflation_pressure` | Eurostat HICP | Annual inflation rate | % | Lower is better |
| `housing_pressure` | Eurostat SILC | Housing overburden rate | % | Lower is better |
| `poverty_pressure` | Eurostat SILC | At-risk-of-poverty rate | % | Lower is better |
| `income_capacity` | Eurostat `ilc_di03` | Median equivalised net income | PPS | Higher is better |

Important rules:

- `income_capacity` uses Eurostat `ilc_di03`, median equivalised net income, PPS.
- `income_capacity` is higher-is-better and should be displayed as PPS.
- The three pressure indicators are lower-is-better.
- `income_capacity` is not a pressure indicator and should not be selected as the Key Risk Driver.
- Percent indicator absolute changes should be treated as percentage points where shown.
- `income_capacity` values and changes should use PPS.

## 4. Data Outputs

Current frontend data dependencies:

- `data/clean/all_mvp_insights.csv` powers the current insight cards and current-value profile views.
- `data/clean/all_mvp_timeseries.csv` powers historical trend charts.

Key clean outputs include:

- `data/clean/hicp_annual_inflation_mvp_countries.csv`
- `data/clean/housing_overburden_mvp_countries.csv`
- `data/clean/poverty_risk_mvp_countries.csv`
- `data/clean/income_capacity_mvp_countries.csv`
- `data/clean/all_mvp_insights.csv`
- `data/clean/all_mvp_timeseries.csv`

## 5. Current Frontend Features

Current Streamlit app features:

- Country selector
- Country Profile
- Key Signals
- Key Risk Driver
- Income capacity section
- Detailed Indicator Cards
- Current-value Country Comparison
- Compact redesigned Country Comparison section
- Country Comparison appears above Historical Trends
- Historical Trends section
- Time-range selector:
  - Last 10 years
  - Last 20 years
  - Full available history
- Historical outlier handling/context note
- Cross-country Historical Trend Comparison
- Indicator Focus Mode
- Methodology notes
- MVP disclaimer
- CSV export for selected country profile

## 6. Recent UI Decisions

The frontend should feel modern, minimalistic, premium, calm, and readable.

Design decisions to preserve:

- Avoid spreadsheet-like layouts.
- Keep visible cards compact.
- Move long explanations into popovers or expanders.
- Keep descriptions readable in dark mode.
- Avoid raw HTML rendering bugs.
- Keep Country Comparison compact; it was redesigned because the previous version used too much vertical space.
- Prefer clear information hierarchy over dense tables.

## 7. Historical Trend Rules

Historical trend charts are factual/contextual only.

Rules:

- Do not add trend interpretation for now.
- Do not use forecast or prediction language.
- Time-range defaults should avoid old extreme outliers dominating the chart.
- Full available history should remain accessible.
- Missing data should not be interpolated.
- Percent indicator absolute changes should be shown as percentage points where applicable.
- `income_capacity` values and changes should use PPS.
- Historical outlier handling should be explained with a short context note rather than hidden.

## 8. Country Coverage

The MVP covers 28 European countries:

Austria, Belgium, Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Norway, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden.

Important notes:

- Greece uses Eurostat code `EL`, not `GR`.
- Norway must be quoted as `"NO"` in YAML because unquoted `NO` can be parsed as Boolean `False`.

## 9. Key Commands

Activate virtual environment:

```powershell
.venv\Scripts\Activate
```

Run MVP pipeline:

```powershell
python data_pipeline/run_mvp_pipeline.py
```

Launch Streamlit app:

```powershell
streamlit run frontend/streamlit_app.py
```

Check Git status:

```powershell
git status
```

## 10. Technical Stack

- Python 3.x
- pandas
- requests
- PyYAML
- Streamlit
- CSV outputs
- Git

Key entry points:

- Pipeline: `data_pipeline/run_mvp_pipeline.py`
- Frontend: `frontend/streamlit_app.py`
- Config: `data_pipeline/config/datasets.yml` and `data_pipeline/config/countries.yml`
- Handoff: `docs/project_handoff.md`

## 11. Current Limitations

- Country-level only; no city or regional data yet.
- Early-stage financial/social signals only.
- No trend interpretation, forecasting, or prediction.
- No salary, tax, benefits, job-market, language, culture, healthcare, lifestyle, or personal-fit model yet.
- No transparent composite scoring yet.
- No final relocation recommendation engine.

## 12. Future Roadmap

Continue from **Stage 87**.

Recommended next options:

1. Refine Indicator Focus Mode.
2. Polish Cross-country Historical Trend Comparison.
3. Prepare portfolio/LinkedIn presentation.
4. Later add `net_earnings_capacity` using Eurostat `earn_nt_net`.
5. Later add employment/job-market indicators.
6. Later consider transparent composite scoring.
