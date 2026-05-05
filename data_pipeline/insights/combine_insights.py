from pathlib import Path
import sys
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR / "data_pipeline"))

INFLATION_INSIGHTS_PATH = Path("data") / "clean" / "inflation_pressure_insights.csv"
HOUSING_INSIGHTS_PATH = Path("data") / "clean" / "housing_pressure_insights.csv"
POVERTY_INSIGHTS_PATH = Path("data") / "clean" / "poverty_pressure_insights.csv"
INCOME_CAPACITY_INSIGHTS_PATH = Path("data") / "clean" / "income_capacity_insights.csv"
NET_EARNINGS_CAPACITY_INSIGHTS_PATH = Path("data") / "clean" / "net_earnings_capacity_insights.csv"
EMPLOYMENT_STRENGTH_INSIGHTS_PATH = Path("data") / "clean" / "employment_strength_insights.csv"
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

    # Read poverty insights
    poverty_df = pd.read_csv(POVERTY_INSIGHTS_PATH)
    poverty_df["insight_category"] = "poverty_pressure"
    poverty_df = poverty_df.rename(columns={"poverty_risk_rate": "metric_value"})

    # Read income capacity insights
    income_capacity_df = pd.read_csv(INCOME_CAPACITY_INSIGHTS_PATH)
    income_capacity_df["insight_category"] = "income_capacity"
    income_capacity_df = income_capacity_df.rename(columns={"median_equivalised_net_income": "metric_value"})

    # Read net earnings capacity insights
    net_earnings_capacity_df = pd.read_csv(NET_EARNINGS_CAPACITY_INSIGHTS_PATH)
    net_earnings_capacity_df["insight_category"] = "net_earnings_capacity"
    net_earnings_capacity_df = net_earnings_capacity_df.rename(columns={"annual_net_earnings": "metric_value"})

    # Read employment strength insights
    employment_strength_df = pd.read_csv(EMPLOYMENT_STRENGTH_INSIGHTS_PATH)
    employment_strength_df["insight_category"] = "employment_strength"
    employment_strength_df = employment_strength_df.rename(columns={"employment_rate": "metric_value"})

    # Combine the dataframes
    combined_df = pd.concat(
        [
            inflation_df,
            housing_df,
            poverty_df,
            income_capacity_df,
            net_earnings_capacity_df,
            employment_strength_df,
        ],
        ignore_index=True,
    )

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
    print("\nValue counts by insight_category:")
    print(result_df["insight_category"].value_counts())
    print(f"\nSaved combined insights to: {OUTPUT_PATH}")
