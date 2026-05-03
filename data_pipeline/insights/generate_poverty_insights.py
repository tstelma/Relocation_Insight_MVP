from pathlib import Path
import sys
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR / "data_pipeline"))

from utils.config_loader import load_yaml_config


INPUT_PATH = Path("data") / "clean" / "poverty_risk_mvp_countries.csv"
OUTPUT_PATH = Path("data") / "clean" / "poverty_pressure_insights.csv"


def classify_poverty_pressure(rate: float) -> str:
    if pd.isna(rate):
        return "Unknown"
    if rate < 10:
        return "Low"
    if rate < 15:
        return "Moderate"
    if rate < 20:
        return "High"
    return "Very High"


def create_title(pressure_label: str) -> str:
    if pressure_label == "Low":
        return "Poverty risk looks low"
    if pressure_label == "Moderate":
        return "Poverty risk is noticeable"
    if pressure_label == "High":
        return "Poverty risk is high"
    if pressure_label == "Very High":
        return "Poverty risk is very high"
    return "Poverty risk is unclear"


def create_main_message(rate: float, pressure_label: str) -> str:
    if pd.isna(rate):
        return "At-risk-of-poverty rate could not be calculated for the latest period."

    return (
        f"Latest at-risk-of-poverty rate is {rate:.1f}%, "
        f"which suggests {pressure_label.lower()} social pressure."
    )


def create_why_it_matters(pressure_label: str) -> str:
    if pressure_label == "Low":
        return (
            "Lower poverty risk suggests fewer people are living close to the income threshold used to define financial vulnerability."
        )

    if pressure_label == "Moderate":
        return (
            "Moderate poverty risk means a meaningful share of people may still be financially vulnerable, even if overall conditions look stable."
        )

    if pressure_label == "High":
        return (
            "High poverty risk suggests broader financial vulnerability across society, not only isolated cost pressure."
        )

    if pressure_label == "Very High":
        return (
            "Very high poverty risk may indicate that financial pressure affects a large part of the population."
        )

    return "The available data is not enough to explain poverty pressure clearly."


def generate_poverty_insight_cards(input_path: Path = INPUT_PATH) -> pd.DataFrame:
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
        classify_poverty_pressure
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

    # Rename value column to poverty_risk_rate
    result = result.rename(columns={"value": "poverty_risk_rate"})

    return result


if __name__ == "__main__":
    result = generate_poverty_insight_cards()
    result.to_csv(OUTPUT_PATH, index=False)

    print(result[["country_code", "country_name", "title", "poverty_risk_rate", "pressure_label"]])
    print(f"\nSaved poverty insight cards to: {OUTPUT_PATH}")