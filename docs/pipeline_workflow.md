
# Data Pipeline Workflow

## Master MVP Pipeline

The master pipeline (`run_mvp_pipeline.py`) orchestrates four sequential stages:

### Stage 1: HICP Inflation Pipeline
**Script:** `data_pipeline/run_hicp_pipeline.py`
- Fetches HICP annual data from Eurostat API
- Calculates annual inflation rates for all configured countries
- Generates inflation pressure insight cards
- **Output:** `data/clean/inflation_pressure_insights.csv`

### Stage 2: Housing Overburden Export
**Script:** `data_pipeline/run_indicator_export.py housing_overburden`
- Exports housing overburden data for configured countries
- Automatically generates housing pressure insight cards
- **Output:** `data/clean/housing_pressure_insights.csv`

### Stage 3: Poverty Risk Export
**Script:** `data_pipeline/run_indicator_export.py poverty_risk`
- Exports poverty risk data for configured countries
- Automatically generates poverty pressure insight cards
- **Output:** `data/clean/poverty_pressure_insights.csv`

### Stage 4: Combined Insights Export
**Script:** `data_pipeline/insights/combine_insights.py`
- Merges inflation, housing, and poverty insights into unified format
- Adds standardized insight_category field for each row
- Aligns all metrics to common column structure
- **Output:** `data/clean/all_mvp_insights.csv`

**Unified Output Format:**
- insight_category (inflation_pressure, housing_pressure, poverty_pressure)
- country_code, country_name
- time_period
- metric_value (normalized across all indicators)
- pressure_label (Low, Moderate, High, Very High)
- title, main_message, why_it_matters
- confidence_level, source

## Master Pipeline Command

Run the complete MVP pipeline:

```powershell
python data_pipeline/run_mvp_pipeline.py
```

This executes all four stages sequentially and produces the final combined insights file.

## Streamlit Viewer

**Input:** Reads `data/clean/all_mvp_insights.csv` (output from stage 4)

**Features:**
- Country selector with expandable insight cards for all three indicators
- Country pressure summary with metric values
- Overall pressure snapshot (pattern-based assessment across three indicators)
- Relative ranking context (comparison within each indicator category)
- Two-country comparison with multi-metric trade-off analysis
- Trade-off labels (Clear advantage, Mixed trade-off, No major difference)
- Plain-language comparison summaries
- Disclaimer about excluded factors

## Streamlit Viewer Command

Launch the interactive viewer:

```powershell
streamlit run frontend/streamlit_app.py
```

## Data Flow Summary

```
Eurostat APIs
    ↓
[HICP Pipeline] → inflation_pressure_insights.csv
[Housing Export] → housing_pressure_insights.csv  
[Poverty Export] → poverty_pressure_insights.csv
    ↓
[Combine Insights]
    ↓
all_mvp_insights.csv (unified format)
    ↓
[Streamlit Viewer]
    ↓
Interactive MVP Dashboard
```

