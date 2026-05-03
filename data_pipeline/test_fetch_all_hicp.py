from pathlib import Path
import pandas as pd

from extract.fetch_eurostat import fetch_dataset
from transform.parse_eurostat import parse_single_geo_time_series
from utils.config_loader import load_yaml_config


countries_config = load_yaml_config("countries.yml")
countries = countries_config["countries"]

dataset_code = "prc_hicp_midx"

all_country_frames = []

for country in countries:
    country_code = country["code"]

    print(f"Fetching HICP data for {country_code}...")

    params = {
        "geo": country_code,
        "coicop": "CP00",
        "unit": "I15",
        "lang": "en",
    }

    data = fetch_dataset(dataset_code, params=params)

    df = parse_single_geo_time_series(
        data=data,
        dataset_code=dataset_code,
        indicator_name="hicp_index",
        country_code=country_code,
    )

    all_country_frames.append(df)

combined_df = pd.concat(all_country_frames, ignore_index=True)

output_dir = Path("data") / "clean"
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "hicp_index_mvp_countries.csv"
combined_df.to_csv(output_path, index=False)

print(f"\nSaved clean HICP data to: {output_path}")

print("\nCombined data preview:")
print(combined_df.head())

print("\nCountries loaded:")
print(combined_df["country_code"].unique())

print("\nRows per country:")
print(combined_df.groupby("country_code").size())

print("\nLatest rows per country:")
print(combined_df.sort_values("time_period").groupby("country_code").tail(1))