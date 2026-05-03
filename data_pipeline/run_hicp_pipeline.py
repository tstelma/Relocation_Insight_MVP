from pathlib import Path
import sys
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "data_pipeline"))

from extract.fetch_eurostat import fetch_dataset
from transform.parse_eurostat import parse_single_geo_time_series
from transform.calculate_hicp_metrics import calculate_annual_inflation_rate
from utils.config_loader import load_yaml_config


CLEAN_DATA_DIR = BASE_DIR / "data" / "clean"

HICP_INDEX_OUTPUT_PATH = CLEAN_DATA_DIR / "hicp_index_mvp_countries.csv"
HICP_INFLATION_OUTPUT_PATH = CLEAN_DATA_DIR / "hicp_annual_inflation_mvp_countries.csv"


def fetch_hicp_for_all_countries() -> pd.DataFrame:
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

    return pd.concat(all_country_frames, ignore_index=True)


if __name__ == "__main__":
    CLEAN_DATA_DIR.mkdir(parents=True, exist_ok=True)

    hicp_df = fetch_hicp_for_all_countries()
    hicp_df.to_csv(HICP_INDEX_OUTPUT_PATH, index=False)

    print(f"\nSaved HICP index data to: {HICP_INDEX_OUTPUT_PATH}")

    inflation_df = calculate_annual_inflation_rate(hicp_df)
    inflation_df.to_csv(HICP_INFLATION_OUTPUT_PATH, index=False)

    print(f"Saved annual inflation data to: {HICP_INFLATION_OUTPUT_PATH}")
    print("\nLatest annual inflation by country:")
    print(
        inflation_df.sort_values("time_period")
        .groupby("country_code")
        .tail(1)[["country_code", "time_period", "annual_inflation_rate"]]
    )