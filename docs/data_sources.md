# Data Sources

Primary source: **Eurostat**

| Indicator | Eurostat dataset | Source detail |
|---|---|---|
| `inflation_pressure` | HICP | Annual inflation rate based on harmonized consumer price data. |
| `housing_pressure` | SILC | Housing overburden rate. |
| `poverty_pressure` | SILC | At-risk-of-poverty rate. |
| `income_capacity` | `ilc_di03` | Median equivalised net income, PPS. |
| `net_earnings_capacity` | `earn_nt_net` | Annual net earnings, PPS, for a single person without children earning 100% of average earnings. |

Key clean outputs:

- `data/clean/hicp_annual_inflation_mvp_countries.csv`
- `data/clean/housing_overburden_mvp_countries.csv`
- `data/clean/poverty_risk_mvp_countries.csv`
- `data/clean/income_capacity_mvp_countries.csv`
- `data/clean/net_earnings_capacity_mvp_countries.csv`
- `data/clean/income_capacity_insights.csv`
- `data/clean/net_earnings_capacity_insights.csv`
- `data/clean/all_mvp_insights.csv`
- `data/clean/all_mvp_timeseries.csv`

`all_mvp_insights.csv` powers current insight cards, country profile views, Top 5 rankings, and current-value comparison. `all_mvp_timeseries.csv` powers historical charts.

The pressure indicators are lower-is-better. `income_capacity` and `net_earnings_capacity` are higher-is-better capacity signals shown in PPS.
