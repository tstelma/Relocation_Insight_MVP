# Relocation Insight MVP

Early MVP for exploring financial pressure insights across 28 selected European countries.

The current version uses Eurostat data to generate insights across three key financial pressure indicators:

- **Inflation pressure** (annual inflation rate from HICP)
- **Housing burden** (housing overburden rate)
- **Poverty risk** (at-risk-of-poverty rate)

## Setup

Create and activate the virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
```

## Current MVP functionality

### Data Pipeline
- Eurostat HICP inflation pipeline
- Eurostat housing overburden export
- Eurostat poverty risk export
- Automatic insight card generation for all three indicators
- Combined insights export (unified standardized format)

### Streamlit Viewer
- Country selector with expandable insight cards
- Country pressure summary with metric values
- Overall pressure snapshot (pattern-based assessment)
- Relative ranking context within each indicator
- Two-country comparison mode
- Multi-metric trade-off analysis
- Plain-language comparison summaries
- Disclaimer about excluded factors

## Run commands

Run the complete MVP pipeline:

```powershell
python data_pipeline/run_mvp_pipeline.py
```

Launch the Streamlit viewer:

```powershell
streamlit run frontend/streamlit_app.py
```

## Current indicators and coverage

**Indicators:**
- Inflation pressure (Annual inflation rate, %)
- Housing burden (Housing overburden rate, %)
- Poverty risk (At-risk-of-poverty rate, %)

**Country coverage:** 28 European countries selected based on available Eurostat data

## Current limitations and excluded factors

This MVP does **not yet include**:
- Salary levels and wage growth
- Taxes and social benefits
- Career opportunities and job markets
- Language and cultural factors
- Lifestyle preferences
- Healthcare systems and quality
- Personal circumstances and preferences
- Sub-national regional variations
- Cost of living beyond housing
- Employment rates or job security

This is an early-stage exploration tool, not a comprehensive relocation recommendation engine.
