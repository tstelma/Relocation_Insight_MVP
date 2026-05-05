# Data Pipeline Workflow

## Overview

The MVP pipeline fetches Eurostat data, generates indicator-specific insight cards, exports standardized historical time series, and feeds the Streamlit app.

The current MVP has five indicators:

1. `inflation_pressure`
2. `housing_pressure`
3. `poverty_pressure`
4. `income_capacity`
5. `net_earnings_capacity`

## Pipeline Stages

### Stage 1: HICP Inflation Pipeline

**Script:** `data_pipeline/run_hicp_pipeline.py`

What it does:

1. Fetches HICP index values from Eurostat.
2. Calculates annual inflation rates.
3. Classifies inflation pressure.
4. Generates inflation pressure insight cards.

Outputs:

- `data/clean/hicp_index_mvp_countries.csv`
- `data/clean/hicp_annual_inflation_mvp_countries.csv`
- `data/clean/inflation_pressure_insights.csv`

### Stage 2: Housing Overburden Export

**Script:** `data_pipeline/run_indicator_export.py housing_overburden`

What it does:

1. Exports housing overburden data from Eurostat SILC.
2. Uses the share of people spending more than 40% of income on housing.
3. Classifies housing pressure.
4. Generates housing pressure insight cards.

Outputs:

- `data/clean/housing_overburden_mvp_countries.csv`
- `data/clean/housing_pressure_insights.csv`

### Stage 3: Poverty Risk Export

**Script:** `data_pipeline/run_indicator_export.py poverty_risk`

What it does:

1. Exports poverty risk data from Eurostat SILC.
2. Uses the share of people below 60% of national median income.
3. Classifies poverty pressure.
4. Generates poverty pressure insight cards.

Outputs:

- `data/clean/poverty_risk_mvp_countries.csv`
- `data/clean/poverty_pressure_insights.csv`

### Stage 4: Income Capacity Export

**Script:** `data_pipeline/run_indicator_export.py income_capacity`

Source: Eurostat `ilc_di03`  
Metric: median equivalised net income  
Unit: PPS  
Direction: higher is better

Outputs:

- `data/clean/income_capacity_mvp_countries.csv`
- `data/clean/income_capacity_insights.csv`

### Stage 5: Net Earnings Capacity Export

**Script:** `data_pipeline/run_indicator_export.py net_earnings_capacity`

Source: Eurostat `earn_nt_net`  
Metric: annual net earnings  
Scenario: single person, no children, earning 100% of average earnings  
Unit: PPS  
Direction: higher is better

This is a working-person earnings signal. It complements `income_capacity` and is not a pressure indicator.

Outputs:

- `data/clean/net_earnings_capacity_mvp_countries.csv`
- `data/clean/net_earnings_capacity_insights.csv`

### Stage 6: Historical Time-Series Export

**Script:** `data_pipeline/transform/export_timeseries.py`

What it does:

1. Reads clean indicator exports.
2. Standardizes them into one historical format.
3. Adds unit, source, and better-direction metadata.

Output:

- `data/clean/all_mvp_timeseries.csv`

For `net_earnings_capacity`, the standardized rows use:

- `indicator = net_earnings_capacity`
- `unit = PPS`
- `better_direction = higher_is_better`
- `source = Eurostat earn_nt_net`

### Stage 7: Combined Insights Export

**Script:** `data_pipeline/insights/combine_insights.py`

What it does:

1. Reads all five insight card files.
2. Standardizes them into a unified schema.
3. Adds `insight_category`.
4. Renames metric columns to `metric_value`.

Output:

- `data/clean/all_mvp_insights.csv`

Unified column structure:

```text
insight_category
country_code
country_name
time_period
metric_value
pressure_label
title
main_message
why_it_matters
confidence_level
source
```

`all_mvp_insights.csv` preserves the same schema while adding `insight_category = net_earnings_capacity`.

## Running the Pipeline

Run the full MVP pipeline:

```powershell
python data_pipeline/run_mvp_pipeline.py
```

Run the new indicator stage only:

```powershell
python data_pipeline/run_indicator_export.py net_earnings_capacity
```

## Streamlit Viewer

Inputs:

- `data/clean/all_mvp_insights.csv`
- `data/clean/all_mvp_timeseries.csv`

Current viewer features:

- Country selector and Country Profile.
- Key Signals for pressure indicators.
- Key Risk Driver based only on `inflation_pressure`, `housing_pressure`, and `poverty_pressure`.
- Income and earnings capacity section with PPS formatting.
- Detailed Indicator Cards.
- Top 5 by Indicator, including net earnings capacity.
- Current-value Country Comparison, including net earnings capacity.
- Historical Trends and Cross-country Historical Trend Comparison, including net earnings capacity.
- Indicator Glossary, methodology notes, MVP disclaimer, and CSV export.

Direction logic:

- Lower is better for `inflation_pressure`, `housing_pressure`, and `poverty_pressure`.
- Higher is better for `income_capacity` and `net_earnings_capacity`.

Launch the viewer:

```powershell
streamlit run frontend/streamlit_app.py
```

## Complete Data Flow

```text
Eurostat HICP       -> inflation pipeline        -> inflation_pressure_insights.csv
Eurostat SILC       -> housing export            -> housing_pressure_insights.csv
Eurostat SILC       -> poverty export            -> poverty_pressure_insights.csv
Eurostat ilc_di03   -> income capacity export    -> income_capacity_insights.csv
Eurostat earn_nt_net -> net earnings export      -> net_earnings_capacity_insights.csv

clean indicator exports -> all_mvp_timeseries.csv
insight card files      -> all_mvp_insights.csv

all_mvp_insights.csv + all_mvp_timeseries.csv -> Streamlit app
```

## Configuration

Countries are defined in `data_pipeline/config/countries.yml`.  
Indicators and Eurostat filters are defined in `data_pipeline/config/datasets.yml`.

Important notes:

- Greece uses Eurostat code `EL`, not `GR`.
- Norway code must be quoted in YAML as `"NO"` because unquoted `NO` can parse as Boolean `False`.
- `net_earnings_capacity` is scenario-based and should be interpreted as a directional working-person earnings signal, not as a universal salary model.
