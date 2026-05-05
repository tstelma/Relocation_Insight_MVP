from pathlib import Path
import sys
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR / "data_pipeline"))

from utils.config_loader import load_yaml_config


INPUT_PATH = Path("data") / "clean" / "net_earnings_capacity_mvp_countries.csv"
OUTPUT_PATH = Path("data") / "clean" / "net_earnings_capacity_insights.csv"


def classify_net_earnings_capacity(value: float, quartiles: dict[float, float]) -> str:
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
        return "Net earnings capacity appears weaker"
    if capacity_label == "Moderate":
        return "Net earnings capacity is moderate"
    if capacity_label == "High":
        return "Net earnings capacity is strong"
    if capacity_label == "Very High":
        return "Net earnings capacity is very strong"
    return "Net earnings capacity data unavailable"


def create_main_message(value: float, capacity_label: str) -> str:
    if pd.isna(value):
        return "Latest annual net earnings for the selected worker scenario are unavailable for this country."

    label_text = {
        "Low": "weaker net earnings capacity",
        "Moderate": "moderate net earnings capacity",
        "High": "strong net earnings capacity",
        "Very High": "very strong net earnings capacity",
    }.get(capacity_label, "unknown net earnings capacity")

    return (
        f"Latest annual net earnings for a single person without children earning 100% of average earnings "
        f"are {value:,.0f} PPS, which suggests {label_text}."
    )


def create_why_it_matters(capacity_label: str) -> str:
    if capacity_label == "Low":
        return (
            "Weaker net earnings capacity may limit financial flexibility for workers after taxes and social contributions."
        )
    if capacity_label == "Moderate":
        return (
            "Moderate net earnings capacity gives a working-person earnings signal, but local costs still need separate review."
        )
    if capacity_label == "High":
        return (
            "Strong net earnings capacity suggests better after-tax earnings potential for the selected worker scenario."
        )
    if capacity_label == "Very High":
        return (
            "Very strong net earnings capacity suggests comparatively high after-tax earnings for the selected worker scenario."
        )
    return "The available earnings data is not enough to describe net earnings capacity clearly."


def generate_net_earnings_capacity_insight_cards(input_path: Path = INPUT_PATH) -> pd.DataFrame:
    df = pd.read_csv(input_path)

    required_columns = {"country_code", "time_period", "value"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"net_earnings_capacity input is missing required columns: {sorted(missing_columns)}"
        )

    if df["value"].isna().all():
        raise RuntimeError(
            "net_earnings_capacity insights cannot be generated because all exported values are NaN."
        )

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
        raise RuntimeError(
            "net_earnings_capacity insights cannot be generated because latest values are all NaN."
        )

    quartiles = valid_values.quantile([0.25, 0.5, 0.75]).to_dict()

    latest_df["pressure_label"] = latest_df["value"].apply(
        lambda v: classify_net_earnings_capacity(v, quartiles)
    )

    latest_df["title"] = latest_df["pressure_label"].apply(create_title)

    latest_df["main_message"] = latest_df.apply(
        lambda row: create_main_message(row["value"], row["pressure_label"]),
        axis=1,
    )

    latest_df["why_it_matters"] = latest_df["pressure_label"].apply(create_why_it_matters)

    latest_df["confidence_level"] = "High"
    latest_df["source"] = "Eurostat earn_nt_net"

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

    result = result.rename(columns={"value": "annual_net_earnings"})
    return result


if __name__ == "__main__":
    result = generate_net_earnings_capacity_insight_cards()
    result.to_csv(OUTPUT_PATH, index=False)

    print(result[["country_code", "country_name", "title", "annual_net_earnings", "pressure_label"]])
    print(f"\nSaved net earnings capacity insight cards to: {OUTPUT_PATH}")
