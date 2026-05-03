# Relocation Insight MVP — Project Handoff

## Project Overview

**Project Name:** Relocation Insight MVP

**Product Goal:**
Eurostat-based decision-support MVP for comparing European countries by financial and social pressure indicators. Provides early-stage insights into inflation, housing, and poverty pressures to support relocation research.

## Current Status

- ✅ Python environment working
- ✅ Git repo initialized
- ✅ Eurostat API ingestion working
- ✅ Master MVP pipeline working
- ✅ Streamlit MVP viewer working

## Current Indicators

1. **inflation_pressure**
   - Source: Eurostat HICP (Harmonized Index of Consumer Prices)
   - Metric: Annual inflation rate (%)
   - Data: Annual averages for configured countries

2. **housing_pressure**
   - Source: Eurostat SILC (Statistics on Income and Living Conditions)
   - Metric: Housing overburden rate (%)
   - Definition: Share of population spending >40% of income on housing

3. **poverty_pressure**
   - Source: Eurostat SILC (Statistics on Income and Living Conditions)
   - Metric: At-risk-of-poverty rate (%)
   - Definition: Share of population with income <60% of median

## Current Country Coverage

**28 European countries:**
Austria, Belgium, Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Norway, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden.

### Important Country-Code Notes

- **Greece:** Uses Eurostat code `EL`, not `GR`. This is critical for API queries.
- **Norway:** In YAML configuration, code must be quoted as `"NO"` because unquoted `NO` can be parsed as Boolean `False`.

## Key Commands

**Activate virtual environment:**
```powershell
.venv\Scripts\Activate
```

**Run master MVP pipeline (all 4 stages):**
```powershell
python data_pipeline/run_mvp_pipeline.py
```

**Launch Streamlit viewer:**
```powershell
streamlit run frontend/streamlit_app.py
```

**Check Git status:**
```powershell
git status
```

## Current Data Outputs

**Raw/Intermediate Data:**
- `data/clean/hicp_index_mvp_countries.csv` — HICP index values
- `data/clean/hicp_annual_inflation_mvp_countries.csv` — Annual inflation rates
- `data/clean/housing_overburden_mvp_countries.csv` — Housing burden rates
- `data/clean/poverty_risk_mvp_countries.csv` — Poverty risk rates

**Insight Cards:**
- `data/clean/inflation_pressure_insights.csv` — Inflation pressure insight cards
- `data/clean/housing_pressure_insights.csv` — Housing pressure insight cards
- `data/clean/poverty_pressure_insights.csv` — Poverty pressure insight cards

**Final Combined Output:**
- `data/clean/all_mvp_insights.csv` — Unified standardized format for all three indicators

## Current Frontend Features

**Country Selection:**
- Dropdown selector for all 28 countries

**Country Pressure Summary:**
- Total insights count
- High/Very High pressure count
- Individual metric values: Inflation, Housing burden, Poverty risk
- **Overall pressure snapshot** (pattern-based assessment)

**Individual Insight Cards:**
- Per-category title, message, and detailed explanation
- Pressure label (Low, Moderate, High, Very High)
- Source and confidence level
- Relative ranking within indicator category

**Comparison Features:**
- Two-country selector
- Multi-metric comparison table
- Difference calculations with +/- indicators
- "Better country" identification per metric

**Comparison Intelligence:**
- Trade-off labels (Clear advantage, Mixed trade-off, No major difference)
- Plain-language summaries
- Threshold-based analysis (0.5% for "No major difference")

**Disclaimer:**
- Clearly states MVP compares only three indicators
- Lists excluded factors: salary, taxes, career opportunities, language, culture, lifestyle, healthcare, personal circumstances

## Current Limitations

- **Geography:** Country-level only, no city/regional data yet
- **Scope:** Early-stage financial pressure insights only
- **Excluded factors:** 
  - Salary levels and wage growth
  - Tax systems and social benefits
  - Career opportunities and job markets
  - Language and cultural factors
  - Lifestyle preferences and fit
  - Healthcare systems and quality
  - Personal circumstances and preferences
  - Employment rates and job security
  - Cost of living beyond housing
- **Not included:** Full relocation recommendation engine

## Next Planned Stage

**Stage 48:** Update README.md and docs/pipeline_workflow.md to reflect expanded MVP with poverty indicator.

*(Current stage documentation has been completed.)*

## Working Style & Collaboration

### For Future Development

- **Stage-by-stage approach:** Guide one stage at a time with concise instructions
- **Focus:** Current stage only, clear next steps
- **Execution:** User runs commands/code in VS Code and reports outputs
- **Feedback loop:** Minimal context, maximum clarity

### Key Contacts & Resources

- Eurostat API: https://ec.europa.eu/eurostat/web/main/home
- HICP documentation: HICP annual index and inflation rates
- SILC documentation: Housing overburden and poverty risk indicators
- VS Code environment: Streamlit extension recommended for viewer development

## Technical Stack

- **Language:** Python 3.x
- **Data:** pandas, pathlib
- **APIs:** requests (Eurostat HTTP)
- **Configuration:** PyYAML
- **Frontend:** Streamlit
- **Data Format:** CSV (UTF-8)
- **Version Control:** Git

## Project Structure

```
relocation_insight_mvp/
├── README.md                          # Project overview
├── requirements.txt                   # Python dependencies
├── data/
│   └── clean/                        # All CSV outputs
├── data_pipeline/
│   ├── run_mvp_pipeline.py           # Master orchestrator
│   ├── run_hicp_pipeline.py          # Inflation pipeline
│   ├── run_indicator_export.py       # Generic indicator export
│   ├── config/                       # Configuration files
│   │   ├── countries.yml
│   │   └── datasets.yml
│   ├── extract/                      # Data extraction
│   ├── transform/                    # Data transformation
│   ├── insights/                     # Insight generation
│   └── utils/                        # Shared utilities
├── frontend/
│   └── streamlit_app.py              # Streamlit viewer
├── docs/
│   ├── pipeline_workflow.md
│   ├── metric_definitions.md
│   ├── data_sources.md
│   ├── mvp_scope.md
│   └── project_handoff.md            # This file
└── .venv/                            # Virtual environment
```

## Critical Paths & Entry Points

- **Pipeline entry:** `data_pipeline/run_mvp_pipeline.py`
- **Viewer entry:** `frontend/streamlit_app.py`
- **Config:** `data_pipeline/config/datasets.yml` and `countries.yml`
- **Data source:** Eurostat API via `data_pipeline/extract/fetch_eurostat.py`

---

**Last Updated:** May 3, 2026  
**Status:** MVP complete with three indicators, ready for next development phase
