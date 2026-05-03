from pathlib import Path
import sys
import pandas as pd
import argparse


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "data_pipeline"))

from extract.fetch_eurostat import fetch_dataset
from transform.parse_eurostat import parse_single_geo_time_series
from utils.config_loader import load_yaml_config

CLEAN_DATA_DIR = BASE_DIR / "data" / "clean"


def run_indicator_export(indicator_key: str) -> None:
    # Load configs
    datasets_config = load_yaml_config("datasets.yml")
    countries_config = load_yaml_config("countries.yml")

    if indicator_key not in datasets_config["datasets"]:
        raise ValueError(f"Indicator '{indicator_key}' not found in datasets.yml")

    dataset_config = datasets_config["datasets"][indicator_key]
    dataset_code = dataset_config["dataset_code"]
    filters = dataset_config.get("filters", {})

    countries = countries_config["countries"]

    all_country_frames = []

    for country in countries:
        country_code = country["code"]
        print(f"Fetching {indicator_key} data for {country_code}...")

        params = filters.copy()
        params["geo"] = country_code

        data = fetch_dataset(dataset_code, params=params)

        df = parse_single_geo_time_series(
            data=data,
            dataset_code=dataset_code,
            indicator_name=indicator_key,
            country_code=country_code,
        )

        all_country_frames.append(df)

    combined_df = pd.concat(all_country_frames, ignore_index=True)

    CLEAN_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = CLEAN_DATA_DIR / f"{indicator_key}_mvp_countries.csv"
    combined_df.to_csv(output_path, index=False)

    print(f"\nSaved {indicator_key} data to: {output_path}")

    print(f"\nRows per country for {indicator_key}:")
    print(combined_df.groupby("country_code").size())

    if indicator_key == "income_capacity" and combined_df["value"].isna().all():
        raise RuntimeError(
            "income_capacity export produced all NaN values. "
            "Please verify the ilc_di03 filters and unit selection in data_pipeline/config/datasets.yml."
        )

    print(f"\nLatest row per country for {indicator_key}:")
    latest_rows = (
        combined_df.sort_values("time_period")
        .groupby("country_code")
        .tail(1)[["country_code", "time_period", "value"]]
    )
    print(latest_rows)

    # Generate housing insights if housing_overburden was exported
    if indicator_key == "housing_overburden":
        from insights.generate_housing_insights import generate_housing_insight_cards

        print(f"\nGenerating housing pressure insights...")
        insights_df = generate_housing_insight_cards(output_path)
        insights_output_path = CLEAN_DATA_DIR / "housing_pressure_insights.csv"
        insights_df.to_csv(insights_output_path, index=False)

        print(f"Saved housing pressure insights to: {insights_output_path}")
        print("\nHousing pressure insights preview:")
        print(insights_df[["country_code", "country_name", "title", "housing_overburden_rate", "pressure_label"]])

    # Generate poverty insights if poverty_risk was exported
    if indicator_key == "poverty_risk":
        from insights.generate_poverty_insights import generate_poverty_insight_cards

        print(f"\nGenerating poverty pressure insights...")
        insights_df = generate_poverty_insight_cards(output_path)
        insights_output_path = CLEAN_DATA_DIR / "poverty_pressure_insights.csv"
        insights_df.to_csv(insights_output_path, index=False)

        print(f"Saved poverty pressure insights to: {insights_output_path}")
        print("\nPoverty pressure insights preview:")
        print(insights_df[["country_code", "country_name", "title", "poverty_risk_rate", "pressure_label"]])

    # Generate income capacity insights if income_capacity was exported
    if indicator_key == "income_capacity":
        from insights.generate_income_capacity_insights import generate_income_capacity_insight_cards

        print(f"\nGenerating income capacity insights...")
        insights_df = generate_income_capacity_insight_cards(output_path)
        insights_output_path = CLEAN_DATA_DIR / "income_capacity_insights.csv"
        insights_df.to_csv(insights_output_path, index=False)

        print(f"Saved income capacity insights to: {insights_output_path}")
        print("\nIncome capacity insights preview:")
        print(insights_df[["country_code", "country_name", "title", "median_equivalised_net_income", "pressure_label"]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export indicator data for all MVP countries")
    parser.add_argument("indicator_key", help="The indicator key from datasets.yml (e.g., housing_overburden)")

    args = parser.parse_args()
    run_indicator_export(args.indicator_key)