# Relocation Insight MVP - Project Handoff

**Last Updated:** May 5, 2026  
**Current Stage:** Stage 95 complete. Continue from **Stage 96**.

## 1. Project Overview

Relocation Insight MVP is a Eurostat-based Streamlit app for comparing European countries using early-stage relocation pressure, income-capacity, and working-person net earnings signals.

The app is a decision-support MVP, not a full relocation recommendation engine. It helps users compare countries by inflation pressure, housing pressure, poverty pressure, purchasing-power-adjusted income capacity, and scenario-based net earnings capacity.

## 2. Current Project Status

The 5-indicator MVP is working end to end:

1. `inflation_pressure`
2. `housing_pressure`
3. `poverty_pressure`
4. `income_capacity`
5. `net_earnings_capacity`

Current state:

- Eurostat ingestion and MVP pipeline are working.
- Streamlit frontend is working with a modernized, compact, premium-feeling layout.
- `all_mvp_insights.csv` powers current insights, current-value cards, profile views, Top 5 rankings, and current comparison.
- `all_mvp_timeseries.csv` powers historical trend charts, including net earnings capacity.
- Country Comparison has been redesigned and compacted.
- Country Comparison appears above Historical Trends.
- Historical charts are factual/contextual only, with no forecast or prediction language.
- Indicator Glossary is available as a searchable collapsed reference section.

## 3. Current MVP Indicators

| Indicator | Source | Metric | Unit | Direction |
|---|---|---|---|---|
| `inflation_pressure` | Eurostat HICP | Annual inflation rate | % | Lower is better |
| `housing_pressure` | Eurostat SILC | Housing overburden rate | % | Lower is better |
| `poverty_pressure` | Eurostat SILC | At-risk-of-poverty rate | % | Lower is better |
| `income_capacity` | Eurostat `ilc_di03` | Median equivalised net income | PPS | Higher is better |
| `net_earnings_capacity` | Eurostat `earn_nt_net` | Annual net earnings for a single person, no children, earning 100% of average earnings | PPS | Higher is better |

Important rules:

- `income_capacity` uses Eurostat `ilc_di03`, median equivalised net income, PPS.
- `net_earnings_capacity` uses Eurostat `earn_nt_net`, annual net earnings, PPS, for the selected worker scenario.
- `income_capacity` and `net_earnings_capacity` are higher-is-better and should be displayed as PPS.
- The three pressure indicators are lower-is-better.
- `income_capacity` and `net_earnings_capacity` are not pressure indicators and should not be selected as the Key Risk Driver.
- Percent indicator absolute changes should be treated as percentage points where shown.
- Capacity values and changes should use PPS.
- `net_earnings_capacity` is scenario-based and represents a directional working-person earnings signal, not all households or professions.

## 4. Data Outputs

Current frontend data dependencies:

- `data/clean/all_mvp_insights.csv` powers current insight cards, country profile views, current-value comparison, and Top 5 by Indicator.
- `data/clean/all_mvp_timeseries.csv` powers historical trend charts.

Key clean outputs include:

- `data/clean/hicp_annual_inflation_mvp_countries.csv`
- `data/clean/housing_overburden_mvp_countries.csv`
- `data/clean/poverty_risk_mvp_countries.csv`
- `data/clean/income_capacity_mvp_countries.csv`
- `data/clean/net_earnings_capacity_mvp_countries.csv`
- `data/clean/net_earnings_capacity_insights.csv`
- `data/clean/all_mvp_insights.csv`
- `data/clean/all_mvp_timeseries.csv`

## 5. Current Frontend Features

Current Streamlit app features:

- Country selector with selected-country display.
- Real country flag images in the selected country header and Top 5 section.
- Country Profile.
- Key Signals.
- Key Risk Driver.
- Income and earnings capacity section.
- Detailed Indicator Cards.
- Compact Top 5 by Indicator section, including net earnings capacity.
- Indicator-specific rankings with medals for ranks 1-3.
- Current-value Country Comparison, including net earnings capacity.
- Compact redesigned Country Comparison section.
- Country Comparison appears above Historical Trends.
- Historical Trends section, including net earnings capacity.
- Time-range selector:
  - Last 10 years
  - Last 20 years
  - Full available history
- Historical outlier handling/context note.
- Cross-country Historical Trend Comparison, including net earnings capacity.
- Indicator Glossary / searchable indicator help section.
- Methodology notes.
- MVP disclaimer.
- CSV export for selected country profile.

## 6. Recent UI Decisions

The frontend should feel modern, minimalistic, premium, calm, compact, and readable.

Design decisions to preserve:

- Avoid spreadsheet-like layouts.
- Keep visible cards compact.
- Move long explanations into popovers or expanders.
- Keep descriptions readable in dark mode.
- Avoid raw HTML rendering bugs.
- Keep Country Comparison compact; it was redesigned because the previous version used too much vertical space.
- Keep Top 5 by Indicator as a quick-reference widget, not an overall ranking.
- Treat net earnings capacity as higher-is-better and format it as PPS.
- Use real flag images where flags are shown, while keeping selectors as plain country names.
- Prefer clear information hierarchy over dense tables.

## 7. Historical Trend Rules

Historical trend charts are factual/contextual only.

Rules:

- Do not add strong trend interpretation for now.
- Do not use forecast or prediction language.
- Time-range defaults should avoid old extreme outliers dominating the chart.
- Full available history should remain accessible.
- Missing data should not be interpolated.
- Percent indicator absolute changes should be shown as percentage points where applicable.
- `income_capacity` and `net_earnings_capacity` values and changes should use PPS.
- Historical outlier handling should be explained with a short context note rather than hidden.

## 8. Country Coverage

The MVP covers 28 European countries:

Austria, Belgium, Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Norway, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden.

Important notes:

- Greece uses Eurostat code `EL`, not `GR`.
- For flag display, Eurostat code `EL` maps to ISO flag code `gr`.
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
- Historical charts provide factual context only.
- No forecasting, prediction, or full trend interpretation.
- No full salary, tax, benefits, job-market, language, culture, healthcare, lifestyle, or personal-fit model yet.
- `net_earnings_capacity` represents one selected worker profile only.
- No transparent composite scoring yet.
- No final relocation recommendation engine.

## 12. Future Roadmap

Continue from **Stage 96**.

Recommended next options:

1. Polish Top 5 / Indicator Focus if needed.
2. Polish historical trend comparison.
3. Prepare portfolio/LinkedIn presentation.
4. Later add employment/job-market indicators.
5. Later consider transparent composite scoring.
