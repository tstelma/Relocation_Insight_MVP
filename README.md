# Relocation Insight MVP

Early-stage exploration tool for comparing European countries by financial and social pressure indicators using Eurostat data.

**This is not a relocation recommendation engine.** It provides context for research only.

## What this MVP does

Compares 28 European countries across three key indicators:

1. **Inflation Pressure** — Annual inflation rate from HICP (Harmonized Index of Consumer Prices)
2. **Housing Burden** — Housing overburden rate (% of population spending >40% of income on housing)
3. **Poverty Risk** — At-risk-of-poverty rate (% of population with income <60% of median)

For each indicator, the viewer shows:
- Individual country pressure assessments (Low, Moderate, High, Very High)
- Relative ranking within each indicator
- Overall pressure snapshot (pattern-based assessment combining all three)
- Two-country comparison with trade-off analysis
- Plain-language summaries

## Quick Start

### Setup

Create and activate the virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
```

### Run Commands

**Generate data (master pipeline):**
```powershell
python data_pipeline/run_mvp_pipeline.py
```

**View results in browser:**
```powershell
streamlit run frontend/streamlit_app.py
```

## Country Coverage

Austria, Belgium, Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Norway, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden.

**Important Eurostat codes:**
- Greece uses code `EL` (not `GR`)
- Norway code `"NO"` must be quoted in YAML configuration (unquoted `NO` parses as Boolean)

## Data Outputs

**Raw/intermediate files:**
- `hicp_index_mvp_countries.csv` — HICP index values
- `hicp_annual_inflation_mvp_countries.csv` — Calculated annual inflation rates
- `housing_overburden_mvp_countries.csv` — Housing pressure data
- `poverty_risk_mvp_countries.csv` — Poverty risk data

**Insight files:**
- `inflation_pressure_insights.csv` — Pressure assessment for inflation indicator
- `housing_pressure_insights.csv` — Pressure assessment for housing indicator
- `poverty_pressure_insights.csv` — Pressure assessment for poverty indicator
- `all_mvp_insights.csv` — Combined standardized format (input to Streamlit viewer)

All files saved to `data/clean/`

## What's NOT Included

This MVP does **not** include:
- Salary levels, wage growth, or job markets
- Taxes or social benefits
- Career opportunities or industry presence
- Language, culture, or lifestyle fit
- Healthcare systems or quality
- Regional or city-level data
- Personal preferences or circumstances
- Cost of living factors beyond housing
- Immigration policies or residency requirements

These factors are important for relocation decisions but require separate research.

## Technical Stack

- Python 3.x
- Eurostat REST API
- pandas for data processing
- Streamlit for frontend
- PyYAML for configuration

## For Developers

See `docs/pipeline_workflow.md` for technical pipeline details.
See `docs/project_handoff.md` for complete project reference.
