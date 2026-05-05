from pathlib import Path
import sys

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(BASE_DIR / "data_pipeline"))

from utils.config_loader import load_yaml_config


CLEAN_DATA_DIR = BASE_DIR / "data" / "clean"
OUTPUT_PATH = CLEAN_DATA_DIR / "all_mvp_timeseries.csv"

OUTPUT_COLUMNS = [
    "country_code",
    "country_name",
    "indicator",
    "time_period",
    "metric_value",
    "unit",
    "better_direction",
    "source",
]

INDICATOR_EXPORTS = [
    {
        "indicator": "inflation_pressure",
        "input_file": "hicp_annual_inflation_mvp_countries.csv",
        "value_column": "annual_inflation_rate",
        "unit": "percent",
        "better_direction": "lower_is_better",
        "source": "Eurostat HICP",
    },
    {
        "indicator": "housing_pressure",
        "input_file": "housing_overburden_mvp_countries.csv",
        "value_column": "value",
        "unit": "percent",
        "better_direction": "lower_is_better",
        "source": "Eurostat SILC",
    },
    {
        "indicator": "poverty_pressure",
        "input_file": "poverty_risk_mvp_countries.csv",
        "value_column": "value",
        "unit": "percent",
        "better_direction": "lower_is_better",
        "source": "Eurostat SILC",
    },
    {
        "indicator": "income_capacity",
        "input_file": "income_capacity_mvp_countries.csv",
        "value_column": "value",
        "unit": "PPS",
        "better_direction": "higher_is_better",
        "source": "Eurostat ilc_di03",
    },
    {
        "indicator": "net_earnings_capacity",
        "input_file": "net_earnings_capacity_mvp_countries.csv",
        "value_column": "value",
        "unit": "PPS",
        "better_direction": "higher_is_better",
        "source": "Eurostat earn_nt_net",
    },
]


def load_country_names() -> dict[str, str]:
    countries_config = load_yaml_config("countries.yml")
    return {
        country["code"]: country["name"]
        for country in countries_config["countries"]
    }


def add_year_column(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    time_as_text = df["time_period"].astype(str)
    df["_year"] = pd.to_numeric(
        time_as_text.str.extract(r"(\d{4})", expand=False),
        errors="coerce",
    )

    parsed_time = pd.to_datetime(time_as_text, errors="coerce")
    parsed_year = pd.to_datetime(
        df["_year"].astype("Int64").astype(str),
        format="%Y",
        errors="coerce",
    )
    df["_sort_time"] = parsed_time.where(parsed_time.notna(), parsed_year)

    return df


def standardize_indicator_timeseries(
    config: dict[str, str],
    country_name_map: dict[str, str],
) -> pd.DataFrame:
    input_path = CLEAN_DATA_DIR / config["input_file"]

    if not input_path.exists():
        print(f"Warning: missing input file, skipping: {input_path}")
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    df = pd.read_csv(input_path)
    required_columns = {"country_code", "time_period", config["value_column"]}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        print(
            "Warning: skipping "
            f"{input_path} because it is missing columns: {sorted(missing_columns)}"
        )
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    df = add_year_column(df)
    df = df.dropna(subset=["_year"]).copy()
    df["_year"] = df["_year"].astype(int).astype(str)

    yearly_df = (
        df.sort_values(["country_code", "_year", "_sort_time"])
        .groupby(["country_code", "_year"], as_index=False)
        .tail(1)
        .copy()
    )

    result = pd.DataFrame(
        {
            "country_code": yearly_df["country_code"],
            "country_name": yearly_df["country_code"].map(country_name_map),
            "indicator": config["indicator"],
            "time_period": yearly_df["_year"],
            "metric_value": yearly_df[config["value_column"]],
            "unit": config["unit"],
            "better_direction": config["better_direction"],
            "source": config["source"],
        }
    )

    return result[OUTPUT_COLUMNS]


def export_all_mvp_timeseries(output_path: Path = OUTPUT_PATH) -> pd.DataFrame:
    country_name_map = load_country_names()

    frames = [
        standardize_indicator_timeseries(config, country_name_map)
        for config in INDICATOR_EXPORTS
    ]

    if frames:
        result = pd.concat(frames, ignore_index=True)
    else:
        result = pd.DataFrame(columns=OUTPUT_COLUMNS)

    result = result.sort_values(
        ["country_code", "indicator", "time_period"],
        ignore_index=True,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)

    return result


if __name__ == "__main__":
    timeseries_df = export_all_mvp_timeseries()

    print(f"Saved standardized MVP time-series data to: {OUTPUT_PATH}")
    print(f"Rows exported: {len(timeseries_df)}")
    if not timeseries_df.empty:
        print(timeseries_df.groupby("indicator").size())
