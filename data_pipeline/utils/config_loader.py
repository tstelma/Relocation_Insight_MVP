from pathlib import Path
import yaml


BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = BASE_DIR / "data_pipeline" / "config"


def load_yaml_config(file_name: str) -> dict:
    file_path = CONFIG_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Config file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)