from pathlib import Path
import sys
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR / "data_pipeline"))

INFLATION_INSIGHTS_PATH = Path("data") / "clean" / "inflation_pressure_insights.csv"
HOUSING_INSIGHTS_PATH = Path("data") / "clean" / "housing_pressure_insights.csv"
OUTPUT_PATH = Path("data") / "clean" / "all_mvp_insights.csv"


def combine_insights() -> pd.DataFrame:
    # Read inflation insights
    inflation_df = pd.read_csv(INFLATION_INSIGHTS_PATH)
    inflation_df["insight_category"] = "inflation_pressure"
    inflation_df = inflation_df.rename(columns={"annual_inflation_rate": "metric_value"})

    # Read housing insights
    housing_df = pd.read_csv(HOUSING_INSIGHTS_PATH)
    housing_df["insight_category"] = "housing_pressure"
    housing_df = housing_df.rename(columns={"housing_overburden_rate": "metric_value"})

    # Combine the dataframes
    combined_df = pd.concat([inflation_df, housing_df], ignore_index=True)

    # Select and order the final columns
    final_columns = [
        "insight_category",
        "country_code",
        "country_name",
        "time_period",
        "metric_value",
        "pressure_label",
        "title",
        "main_message",
        "why_it_matters",
        "confidence_level",
        "source",
    ]

    return combined_df[final_columns]


if __name__ == "__main__":
    result_df = combine_insights()
    result_df.to_csv(OUTPUT_PATH, index=False)

    print(result_df[["insight_category", "country_code", "country_name", "metric_value", "pressure_label", "title"]])
    print(f"\nSaved combined insights to: {OUTPUT_PATH}")