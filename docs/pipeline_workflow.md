
# Data Pipeline Workflow

## Overview

The MVP pipeline has four sequential stages that fetch Eurostat data, generate pressure insights, combine them into a unified format, and feed the result to the Streamlit viewer.

## Pipeline Stages

### Stage 1: HICP Inflation Pipeline

**Script:** `data_pipeline/run_hicp_pipeline.py`

**What it does:**
1. Fetches annual HICP (Harmonized Index of Consumer Prices) index values from Eurostat
2. Calculates year-over-year annual inflation rates
3. Classifies each country's inflation as Low/Moderate/High/Very High
4. Generates inflation pressure insight cards

**Outputs:**
- `data/clean/hicp_index_mvp_countries.csv` — Raw HICP index values
- `data/clean/hicp_annual_inflation_mvp_countries.csv` — Calculated inflation rates
- `data/clean/inflation_pressure_insights.csv` — Inflation insight cards (country, pressure_label, title, main_message, etc.)

### Stage 2: Housing Overburden Export

**Script:** `data_pipeline/run_indicator_export.py housing_overburden`

**What it does:**
1. Exports housing overburden data from Eurostat SILC
2. Housing overburden = % of population spending >40% of income on housing
3. Classifies each country's housing pressure
4. Automatically generates housing pressure insight cards

**Outputs:**
- `data/clean/housing_overburden_mvp_countries.csv` — Raw housing data
- `data/clean/housing_pressure_insights.csv` — Housing insight cards

### Stage 3: Poverty Risk Export

**Script:** `data_pipeline/run_indicator_export.py poverty_risk`

**What it does:**
1. Exports poverty risk data from Eurostat SILC
2. Poverty risk = % of population with income <60% of median
3. Classifies each country's poverty pressure
4. Automatically generates poverty pressure insight cards

**Outputs:**
- `data/clean/poverty_risk_mvp_countries.csv` — Raw poverty risk data
- `data/clean/poverty_pressure_insights.csv` — Poverty insight cards

### Stage 4: Combined Insights Export

**Script:** `data_pipeline/insights/combine_insights.py`

**What it does:**
1. Reads all three insight card files
2. Standardizes them into a unified format
3. Adds `insight_category` field (inflation_pressure, housing_pressure, poverty_pressure)
4. Renames metric columns to uniform `metric_value`
5. Ensures all rows have the same column structure

**Output:**
- `data/clean/all_mvp_insights.csv` — Unified input for Streamlit viewer

**Unified Column Structure:**
```
insight_category       (inflation_pressure | housing_pressure | poverty_pressure)
country_code           (AT, BE, BG, etc.)
country_name           (Austria, Belgium, Bulgaria, etc.)
time_period            (Year or date range)
metric_value           (Normalized percentage value)
pressure_label         (Low | Moderate | High | Very High)
title                  (Human-readable insight title)
main_message           (Key finding summary)
why_it_matters         (Context and implications)
confidence_level       (High | Medium | Low)
source                 (Eurostat HICP / Eurostat SILC)
```

## Running the Pipeline

**Execute all four stages:**
```powershell
python data_pipeline/run_mvp_pipeline.py
```

The master pipeline script (`run_mvp_pipeline.py`) runs each stage sequentially, printing progress and status for each stage.

## Streamlit Viewer

**Input File:** `data/clean/all_mvp_insights.csv` (output from Stage 4)

**Viewer Features:**
- **Country selector** — Dropdown to choose any of 28 countries
- **Country pressure summary** — Overview with metric values and overall snapshot
- **Individual insight cards** — One card per indicator showing title, message, ranking, and source
- **Relative ranking** — Shows where each country ranks within each indicator
- **Overall pressure snapshot** — Pattern-based assessment: "Generally low pressure", "Broad pressure risk", "Uneven pressure profile", etc.
- **Two-country comparison** — Select two countries to compare all three metrics side-by-side
- **Difference calculations** — Shows +/- differences for each metric
- **Better country identification** — Identifies which country is better on each metric
- **Trade-off labels** — "Clear advantage", "Mixed trade-off", or "No major difference"
- **Plain-language summary** — Explains the comparison result in readable text
- **MVP disclaimer** — Lists factors not included in this analysis

**Launch the viewer:**
```powershell
streamlit run frontend/streamlit_app.py
```

## Complete Data Flow

```
┌─ Eurostat APIs ─┐
│                 │
├─ HICP data ────→ [Stage 1: HICP Pipeline]
│                   ↓
├─ SILC data ───→ [Stage 2: Housing Export]
│  (housing)       ↓
├─ SILC data ───→ [Stage 3: Poverty Export]
│  (poverty)       ↓
└─────────────────→ [Stage 4: Combine Insights]
                      ↓
              all_mvp_insights.csv
                      ↓
            [Streamlit Viewer]
                      ↓
          Interactive MVP Dashboard
```

## Configuration

**Countries:** Defined in `data_pipeline/config/countries.yml`
**Indicators & Eurostat codes:** Defined in `data_pipeline/config/datasets.yml`

**Important notes:**
- Greece uses Eurostat code `EL` (not `GR`)
- Norway code must be quoted in YAML as `"NO"` (unquoted NO parses as Boolean False)

## For Development

- **Individual pipeline stages** can be run separately
- **Test files** in `data_pipeline/` test individual components
- **Insight generation** is modular — each indicator has its own insight generator
- **Configuration-driven** — Add new countries or indicators by editing YAML configs

