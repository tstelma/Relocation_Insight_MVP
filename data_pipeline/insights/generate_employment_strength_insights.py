from pathlib import Path
import sys
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR / "data_pipeline"))

from utils.config_loader import load_yaml_config


INPUT_PATH = Path("data") / "clean" / "employment_strength_mvp_countries.csv"
OUTPUT_PATH = Path("data") / "clean" / "employment_strength_insights.csv"


def classify_employment_strength(value: float, quartiles: dict[float, float]) -> str:
    if pd.isna(value):
        return "Unknown"
    if value < quartiles[0.25]:
        return "Low"
    if value < quartiles[0.5]:
        return "Moderate"
    if value < quartiles[0.75]:
        return "High"
    return "Very High"


def create_title(strength_label: str) -> str:
    if strength_label == "Low":
        return "Employment signal appears weaker"
    if strength_label == "Moderate":
        return "Employment signal is moderate"
    if strength_label == "High":
        return "Employment signal is strong"
    if strength_label == "Very High":
        return "Employment signal is very strong"
    return "Employment data unavailable"


def create_main_message(value: float, strength_label: str) -> str:
    if pd.isna(value):
        return "Latest working-age employment rate is unavailable for this country."

    label_text = {
        "Low": "a weaker employment signal",
        "Moderate": "a moderate employment signal",
        "High": "a strong employment signal",
        "Very High": "a very strong employment signal",
    }.get(strength_label, "an unknown employment signal")

    return (
        f"Latest working-age employment rate is {value:.2f}%, "
        f"which suggests {label_text}."
    )


def create_why_it_matters(strength_label: str) -> str:
    if strength_label == "Low":
        return (
            "A weaker employment signal may indicate fewer people in the working-age population are employed, "
            "but it does not describe job availability for a specific profession."
        )
    if strength_label == "Moderate":
        return (
            "A moderate employment signal gives broad labour-market context, but role-specific job research is still needed."
        )
    if strength_label == "High":
        return (
            "A strong employment signal suggests a comparatively active labour market for the working-age population."
        )
    if strength_label == "Very High":
        return (
            "A very strong employment signal suggests a high share of the working-age population is employed."
        )
    return "The available employment data is not enough to describe labour-market strength clearly."


def generate_employment_strength_insight_cards(input_path: Path = INPUT_PATH) -> pd.DataFrame:
    df = pd.read_csv(input_path)

    required_columns = {"country_code", "time_period", "value"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"employment_strength input is missing required columns: {sorted(missing_columns)}"
        )

    if df["value"].isna().all():
        raise RuntimeError(
            "employment_strength insights cannot be generated because all exported values are NaN."
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
            "employment_strength insights cannot be generated because latest values are all NaN."
        )

    quartiles = valid_values.quantile([0.25, 0.5, 0.75]).to_dict()

    latest_df["pressure_label"] = latest_df["value"].apply(
        lambda v: classify_employment_strength(v, quartiles)
    )

    latest_df["title"] = latest_df["pressure_label"].apply(create_title)

    latest_df["main_message"] = latest_df.apply(
        lambda row: create_main_message(row["value"], row["pressure_label"]),
        axis=1,
    )

    latest_df["why_it_matters"] = latest_df["pressure_label"].apply(create_why_it_matters)

    latest_df["confidence_level"] = "High"
    latest_df["source"] = "Eurostat lfsi_emp_a"

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

    result = result.rename(columns={"value": "employment_rate"})
    return result


if __name__ == "__main__":
    result = generate_employment_strength_insight_cards()
    result.to_csv(OUTPUT_PATH, index=False)

    print(result[["country_code", "country_name", "title", "employment_rate", "pressure_label"]])
    print(f"\nSaved employment strength insight cards to: {OUTPUT_PATH}")
