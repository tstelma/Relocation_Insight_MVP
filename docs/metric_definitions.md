# Metric Definitions

The MVP currently uses five Eurostat-based indicators.

| Indicator | Definition | Unit | Direction | Role |
|---|---|---|---|---|
| `inflation_pressure` | Annual inflation rate from Eurostat HICP. | % | Lower is better | Pressure indicator |
| `housing_pressure` | Housing overburden rate: share of people spending more than 40% of income on housing. | % | Lower is better | Pressure indicator |
| `poverty_pressure` | At-risk-of-poverty rate: share of people below 60% of national median income. | % | Lower is better | Pressure indicator |
| `income_capacity` | Median equivalised net income from Eurostat `ilc_di03`, adjusted with Purchasing Power Standard. | PPS | Higher is better | Income capacity signal |
| `net_earnings_capacity` | Annual net earnings from Eurostat `earn_nt_net` for a single person, no children, earning 100% of average earnings. | PPS | Higher is better | Working-person earnings signal |

The first three metrics are pressure indicators. `income_capacity` and `net_earnings_capacity` are higher-is-better capacity signals and should not be treated as pressure indicators.

`net_earnings_capacity` is scenario-based. It represents one selected worker profile, not all households, professions, or personal circumstances.
