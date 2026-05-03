from pathlib import Path
import sys
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR / "data_pipeline"))

from utils.config_loader import load_yaml_config

INPUT_PATH = Path("data") / "clean" / "hicp_annual_inflation_mvp_countries.csv"
OUTPUT_PATH = Path("data") / "clean" / "inflation_pressure_insights.csv"


def classify_inflation_pressure(rate: float) -> str:
    if pd.isna(rate):
        return "Unknown"
    if rate < 2:
        return "Low"
    if rate < 5:
        return "Moderate"
    if rate < 10:
        return "High"
    return "Very High"


def create_title(pressure_label: str) -> str:
    if pressure_label == "Low":
        return "Inflation pressure looks low"
    if pressure_label == "Moderate":
        return "Inflation pressure is noticeable"
    if pressure_label == "High":
        return "Inflation pressure is high"
    if pressure_label == "Very High":
        return "Inflation pressure is very high"
    return "Inflation pressure is unclear"


def create_main_message(rate: float, pressure_label: str) -> str:
    if pd.isna(rate):
        return "Annual inflation could not be calculated for the latest period."

    return (
        f"Latest annual inflation is {rate:.2f}%, "
        f"which suggests {pressure_label.lower()} inflation pressure."
    )


def create_why_it_matters(pressure_label: str) -> str:
    if pressure_label == "Low":
        return (
            "Lower inflation pressure usually means everyday prices are rising more slowly, "
            "which can make financial planning feel more stable."
        )

    if pressure_label == "Moderate":
        return (
            "Moderate inflation still affects everyday life. Even if income rises, "
            "people may feel pressure when prices keep moving upward."
        )

    if pressure_label == "High":
        return (
            "High inflation can reduce purchasing power quickly, especially when wages "
            "do not grow at the same pace."
        )

    if pressure_label == "Very High":
        return (
            "Very high inflation can create strong financial stress because everyday costs "
            "change faster than many households can adjust."
        )

    return "The available data is not enough to explain inflation pressure clearly."


if __name__ == "__main__":
    df = pd.read_csv(INPUT_PATH)
    countries_config = load_yaml_config("countries.yml")
    country_name_map = {
        country["code"]: country["name"]
        for country in countries_config["countries"]
    }
    df["time_period"] = pd.to_datetime(df["time_period"])

    latest_df = (
        df.sort_values("time_period")
        .groupby("country_code")
        .tail(1)
        .copy()
    )
    latest_df["country_name"] = latest_df["country_code"].map(country_name_map)

    latest_df["pressure_label"] = latest_df["annual_inflation_rate"].apply(
        classify_inflation_pressure
    )

    latest_df["title"] = latest_df["pressure_label"].apply(create_title)

    latest_df["main_message"] = latest_df.apply(
        lambda row: create_main_message(
            row["annual_inflation_rate"],
            row["pressure_label"],
        ),
        axis=1,
    )

    latest_df["why_it_matters"] = latest_df["pressure_label"].apply(
        create_why_it_matters
    )

    latest_df["confidence_level"] = "High"
    latest_df["source"] = "Eurostat HICP"

    result = latest_df[
        [
            "country_code",
            "country_name",
            "time_period",
            "annual_inflation_rate",
            "pressure_label",
            "title",
            "main_message",
            "why_it_matters",
            "confidence_level",
            "source",
        ]
    ]

    result.to_csv(OUTPUT_PATH, index=False)

    print(result[["country_code", "country_name", "title", "main_message", "confidence_level"]])
    print(f"\nSaved inflation insight cards to: {OUTPUT_PATH}")