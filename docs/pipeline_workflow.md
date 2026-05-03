# Data Pipeline Workflow

## Current pipeline: HICP Inflation

The current working pipeline pulls HICP index data from Eurostat for MVP countries, calculates annual inflation rates, and generates user-facing inflation insight cards.

## Command

```powershell
python data_pipeline\run_hicp_pipeline.py