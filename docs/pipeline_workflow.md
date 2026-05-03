
# Data Pipeline Workflow

## Master MVP Pipeline

The master pipeline runs three steps in order:

1. HICP inflation pipeline (Eurostat data → annual inflation rates → insight cards)
2. Housing overburden export (Eurostat data → housing insights)
3. Combined insights export (merges inflation + housing insights)

The output is data/clean/all_mvp_insights.csv containing standardized insight cards for all indicators.

## Command

Run the complete MVP pipeline:

`powershell
python data_pipeline\run_mvp_pipeline.py
`

## Streamlit Viewer

The Streamlit app reads data/clean/all_mvp_insights.csv and provides:

- Country selector with insight cards
- Country pressure summary
- Relative ranking context
- Two-country comparison mode
- Plain-language summaries and trade-off labels

## Command

Launch the viewer:

`powershell
streamlit run frontend\streamlit_app.py
`

