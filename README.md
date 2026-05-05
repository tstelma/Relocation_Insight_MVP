# Relocation Insight MVP

Early-stage exploration tool for comparing European countries by financial and social pressure indicators using Eurostat data.

**This is not a relocation recommendation engine.** It provides structured context for research only.

## What This MVP Does

Compares 28 European countries across four current indicators:

1. **Inflation pressure** - annual inflation rate from Eurostat HICP
2. **Housing pressure** - housing overburden rate, or the share of people spending more than 40% of income on housing
3. **Poverty pressure** - at-risk-of-poverty rate, or the share of people below 60% of national median income
4. **Income capacity** - median equivalised net income in PPS from Eurostat `ilc_di03`

The three pressure indicators are lower-is-better. `income_capacity` is higher-is-better, uses PPS, and is not a pressure indicator.

## Current App Features

- Modernized Streamlit UI with a compact, readable layout
- Country selector with selected-country profile display and real flag images
- Key signals, key risk driver, income capacity, and detailed indicator cards
- Compact **Top 5 by indicator** section with real flag images and medals for the top 3
- Current-value country comparison, redesigned to use less vertical space
- Historical trends with time ranges:
  - Last 10 years
  - Last 20 years
  - Full available history
- Historical outlier context notes
- Cross-country historical trend comparison
- Searchable indicator glossary
- Methodology notes, MVP disclaimer, and CSV export for the selected country profile

Historical charts are factual/contextual only. The app does not use forecast, prediction, or strong trend-interpretation language.

## App Preview

### Country Profile
![Country Profile](docs/screenshots/country_profile.png)
*Individual country assessment showing pressure indicators and income capacity.*

### Country Comparison
![Country Comparison](docs/screenshots/country_comparison.png)
*Compact side-by-side comparison of two countries across the current MVP indicators.*

### Methodology Notes
![Methodology Notes](docs/screenshots/methodology_notes.png)
*Data sources and methodology details for transparency.*

## Quick Start

Create and activate the virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
```

Generate data:

```powershell
python data_pipeline/run_mvp_pipeline.py
```

Run the app:

```powershell
streamlit run frontend/streamlit_app.py
```

## Country Coverage

Austria, Belgium, Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Norway, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden.

Important Eurostat codes:

- Greece uses code `EL`, not `GR`.
- Norway code `"NO"` must be quoted in YAML configuration because unquoted `NO` can parse as Boolean.

## Data Outputs

Key clean outputs in `data/clean/` include:

- `hicp_annual_inflation_mvp_countries.csv`
- `housing_overburden_mvp_countries.csv`
- `poverty_risk_mvp_countries.csv`
- `income_capacity_mvp_countries.csv`
- `all_mvp_insights.csv` - powers current insights and profile cards
- `all_mvp_timeseries.csv` - powers historical trend charts

## What Is Not Included

This MVP does not include salary levels, taxes, job markets, healthcare, language, culture, lifestyle fit, city-level data, personal preferences, immigration policies, or a final relocation recommendation engine.

## Technical Stack

- Python 3.x
- Eurostat REST API
- pandas
- Streamlit
- PyYAML
- CSV outputs

## For Developers

See `docs/pipeline_workflow.md` for technical pipeline details.  
See `docs/project_handoff.md` for current project handoff notes.
