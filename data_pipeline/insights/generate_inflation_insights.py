from pathlib import Path
import pandas as pd


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


def create_message(country_code: str, rate: float, pressure_label: str) -> str:
    if pd.isna(rate):
        return f"{country_code}: Inflation pressure could not be calculated."

    return (
        f"{country_code}: Annual inflation is {rate:.2f}%, "
        f"which indicates {pressure_label.lower()} inflation pressure."
    )


if __name__ == "__main__":
    df = pd.read_csv(INPUT_PATH)
    df["time_period"] = pd.to_datetime(df["time_period"])

    latest_df = (
        df.sort_values("time_period")
        .groupby("country_code")
        .tail(1)
        .copy()
    )

    latest_df["pressure_label"] = latest_df["annual_inflation_rate"].apply(
        classify_inflation_pressure
    )

    latest_df["insight_message"] = latest_df.apply(
        lambda row: create_message(
            row["country_code"],
            row["annual_inflation_rate"],
            row["pressure_label"],
        ),
        axis=1,
    )

    result = latest_df[
        [
            "country_code",
            "time_period",
            "annual_inflation_rate",
            "pressure_label",
            "insight_message",
        ]
    ]

    result.to_csv(OUTPUT_PATH, index=False)

    print(result)
    print(f"\nSaved inflation insights to: {OUTPUT_PATH}")