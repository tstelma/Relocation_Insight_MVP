# Relocation Insight MVP

Early MVP for exploring financial pressure insights across selected European countries.

The current version uses Eurostat data to generate:

- inflation pressure insights
- housing pressure insights
- combined MVP insight cards
- a simple Streamlit viewer

## Setup

Create and activate the virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate
## Current MVP functionality

- Eurostat HICP inflation pipeline
- Eurostat housing overburden export
- Inflation pressure insight cards
- Housing pressure insight cards
- Combined insights export
- Streamlit viewer with country selector
- Country pressure summary
- Relative ranking context
- Two-country comparison mode
- Plain-language comparison summary
- Trade-off label
- MVP limitation disclaimer

## Run commands

Run the complete MVP pipeline:

`powershell
python data_pipeline\run_mvp_pipeline.py
` 

Launch the Streamlit viewer:

`powershell
streamlit run frontend\streamlit_app.py
` 

## Current indicators

- Inflation pressure
- Housing burden

## Current limitations

- Country-level only
- Selected countries only
- No salary/tax/career/lifestyle factors yet
- Not a full relocation recommendation engine yet
