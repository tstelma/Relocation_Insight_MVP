from extract.fetch_eurostat import fetch_dataset
from transform.parse_eurostat import parse_single_geo_time_series


params = {
    "geo": "DE",
    "coicop": "CP00",
    "unit": "I15",
    "lang": "en",
}

dataset_code = "prc_hicp_midx"

data = fetch_dataset(dataset_code, params=params)

df = parse_single_geo_time_series(
    data=data,
    dataset_code=dataset_code,
    indicator_name="hicp_index",
    country_code="DE",
)

print(df.head())
print("\nRows:", len(df))
print("\nLatest rows:")
print(df.tail())