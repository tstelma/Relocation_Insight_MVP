from pathlib import Path
import sys
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR / "data_pipeline"))

from utils.config_loader import load_yaml_config


INPUT_PATH = Path("data") / "clean" / "income_capacity_mvp_countries.csv"
OUTPUT_PATH = Path("data") / "clean" / "income_capacity_insights.csv"


def classify_income_capacity(value: float, quartiles: dict[float, float]) -> str:
    if pd.isna(value):
        return "Unknown"
    if value < quartiles[0.25]:
        return "Low"
    if value < quartiles[0.5]:
        return "Moderate"
    if value < quartiles[0.75]:
        return "High"
    return "Very High"


def create_title(capacity_label: str) -> str:
    if capacity_label == "Low":
        return "Income capacity appears weak"
    if capacity_label == "Moderate":
        return "Income capacity is moderate"
    if capacity_label == "High":
        return "Income capacity is strong"
    if capacity_label == "Very High":
        return "Income capacity is very strong"
    return "Income capacity data unavailable"


def create_main_message(value: float, capacity_label: str) -> str:
    if pd.isna(value):
        return "Latest median equivalised net income is unavailable for this country."

    return (
        f"Latest median equivalised net income is {value:,.0f} EUR, "
        f"which suggests {capacity_label.lower()} income capacity."
    )


def create_why_it_matters(capacity_label: str) -> str:
    if capacity_label == "Low":
        return (
            "Lower income capacity can limit relocation options because households may have less buffer for housing, "
            "services, and unexpected expenses."
        )
    if capacity_label == "Moderate":
        return (
            "Moderate income capacity means there is some room for relocation, but care is still needed to compare local costs."
        )
    if capacity_label == "High":
        return (
            "Strong income capacity suggests the median household has more flexibility to manage relocation-related expenses."
        )
    if capacity_label == "Very High":
        return (
            "Very strong income capacity suggests the median household is well positioned to absorb relocation costs and local price differences."
        )
    return "The available income data is not enough to describe income capacity clearly."


def generate_income_capacity_insight_cards(input_path: Path = INPUT_PATH) -> pd.DataFrame:
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

    valid_values = latest_df["value"].dropna()
    if valid_values.empty:
        quartiles = {0.25: 0.0, 0.5: 0.0, 0.75: 0.0}
    else:
        quartiles = valid_values.quantile([0.25, 0.5, 0.75]).to_dict()

    latest_df["pressure_label"] = latest_df["value"].apply(
        lambda v: classify_income_capacity(v, quartiles)
    )

    latest_df["title"] = latest_df["pressure_label"].apply(create_title)

    latest_df["main_message"] = latest_df.apply(
        lambda row: create_main_message(row["value"], row["pressure_label"]),
        axis=1,
    )

    latest_df["why_it_matters"] = latest_df["pressure_label"].apply(create_why_it_matters)

    latest_df["confidence_level"] = "High"
    latest_df["source"] = "Eurostat ilc_di03"

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

    result = result.rename(columns={"value": "median_equivalised_net_income"})
    return result


if __name__ == "__main__":
    result = generate_income_capacity_insight_cards()
    result.to_csv(OUTPUT_PATH, index=False)

    print(result[["country_code", "country_name", "title", "median_equivalised_net_income", "pressure_label"]])
    print(f"\nSaved income capacity insight cards to: {OUTPUT_PATH}")
