from pathlib import Path
import sys
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR / "data_pipeline"))

from utils.config_loader import load_yaml_config


INPUT_PATH = Path("data") / "clean" / "housing_overburden_mvp_countries.csv"
OUTPUT_PATH = Path("data") / "clean" / "housing_pressure_insights.csv"


def classify_housing_pressure(rate: float) -> str:
    if pd.isna(rate):
        return "Unknown"
    if rate < 5:
        return "Low"
    if rate < 10:
        return "Moderate"
    if rate < 15:
        return "High"
    return "Very High"


def create_title(pressure_label: str) -> str:
    if pressure_label == "Low":
        return "Housing pressure looks low"
    if pressure_label == "Moderate":
        return "Housing pressure is noticeable"
    if pressure_label == "High":
        return "Housing pressure is high"
    if pressure_label == "Very High":
        return "Housing pressure is very high"
    return "Housing pressure is unclear"


def create_main_message(rate: float, pressure_label: str) -> str:
    if pd.isna(rate):
        return "Housing overburden rate could not be calculated for the latest period."

    return (
        f"Latest housing overburden rate is {rate:.1f}%, "
        f"which suggests {pressure_label.lower()} housing pressure."
    )


def create_why_it_matters(pressure_label: str) -> str:
    if pressure_label == "Low":
        return (
            "Lower housing overburden suggests fewer households spend a very high share of income on housing costs."
        )

    if pressure_label == "Moderate":
        return (
            "Moderate housing pressure means housing costs may still affect financial comfort, especially for lower-income households."
        )

    if pressure_label == "High":
        return (
            "High housing overburden can create financial stress because many households spend a large share of income on housing."
        )

    if pressure_label == "Very High":
        return (
            "Very high housing overburden suggests housing costs may be a major source of financial stress."
        )

    return "The available data is not enough to explain housing pressure clearly."


def generate_housing_insight_cards(input_path: Path = INPUT_PATH) -> pd.DataFrame:
    df = pd.read_csv(input_path)

    countries_config = load_yaml_config("countries.yml")
    country_name_map = {
        country["code"]: country["name"]
        for country in countries_config["countries"]
    }

    latest_df = (
        df.sort_values("time_period")
        .groupby("country_code")
        .tail(1)
        .copy()
    )

    latest_df["country_name"] = latest_df["country_code"].map(country_name_map)

    latest_df["pressure_label"] = latest_df["value"].apply(
        classify_housing_pressure
    )

    latest_df["title"] = latest_df["pressure_label"].apply(create_title)

    latest_df["main_message"] = latest_df.apply(
        lambda row: create_main_message(
            row["value"],
            row["pressure_label"],
        ),
        axis=1,
    )

    latest_df["why_it_matters"] = latest_df["pressure_label"].apply(
        create_why_it_matters
    )

    latest_df["confidence_level"] = "High"
    latest_df["source"] = "Eurostat SILC"

    result = latest_df[
        [
            "country_code",
            "country_name",
            "time_period",
            "value",
            "pressure_label",
            "title",
            "main_message",
            "why_it_matters",
            "confidence_level",
            "source",
        ]
    ]

    # Rename value column to housing_overburden_rate
    result = result.rename(columns={"value": "housing_overburden_rate"})

    return result


if __name__ == "__main__":
    result = generate_housing_insight_cards()
    result.to_csv(OUTPUT_PATH, index=False)

    print(result[["country_code", "country_name", "title", "housing_overburden_rate", "pressure_label"]])
    print(f"\nSaved housing insight cards to: {OUTPUT_PATH}")