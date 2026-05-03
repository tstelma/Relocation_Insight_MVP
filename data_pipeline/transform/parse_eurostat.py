import pandas as pd


def parse_single_geo_time_series(
    data: dict,
    dataset_code: str,
    indicator_name: str,
    country_code: str,
) -> pd.DataFrame:
    """
    Parses a Eurostat JSON-stat response filtered to:
    - one frequency
    - one unit
    - one coicop/item
    - one country
    - multiple time periods
    """

    time_dimension = data["dimension"]["time"]["category"]["index"]
    time_labels = sorted(time_dimension.items(), key=lambda item: item[1])

    values = data.get("value", {})

    rows = []

    for time_period, position in time_labels:
        value = values.get(str(position))

        rows.append(
            {
                "dataset_code": dataset_code,
                "indicator_name": indicator_name,
                "country_code": country_code,
                "time_period": time_period,
                "value": value,
            }
        )

    return pd.DataFrame(rows)