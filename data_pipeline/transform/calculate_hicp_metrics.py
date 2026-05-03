from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data") / "clean" / "hicp_index_mvp_countries.csv"
OUTPUT_PATH = Path("data") / "clean" / "hicp_annual_inflation_mvp_countries.csv"


def calculate_annual_inflation_rate(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["time_period"] = pd.to_datetime(df["time_period"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    df = df.sort_values(["country_code", "time_period"])

    df["value_12_months_ago"] = df.groupby("country_code")["value"].shift(12)

    df["annual_inflation_rate"] = (
        (df["value"] / df["value_12_months_ago"] - 1) * 100
    ).round(2)

    result = df[
        [
            "dataset_code",
            "indicator_name",
            "country_code",
            "time_period",
            "value",
            "value_12_months_ago",
            "annual_inflation_rate",
        ]
    ]

    return result


if __name__ == "__main__":
    input_df = pd.read_csv(INPUT_PATH)

    result_df = calculate_annual_inflation_rate(input_df)

    result_df.to_csv(OUTPUT_PATH, index=False)

    print(result_df.tail(20))
    print(f"\nSaved annual inflation data to: {OUTPUT_PATH}")