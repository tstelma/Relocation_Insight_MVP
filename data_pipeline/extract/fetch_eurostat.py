import requests


BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"


def fetch_dataset(dataset_code: str, params: dict | None = None) -> dict:
    url = f"{BASE_URL}/{dataset_code}"

    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()

    return response.json()