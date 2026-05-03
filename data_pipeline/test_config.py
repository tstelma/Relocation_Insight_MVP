from utils.config_loader import load_yaml_config


countries_config = load_yaml_config("countries.yml")
datasets_config = load_yaml_config("datasets.yml")

countries = countries_config["countries"]
datasets = datasets_config["datasets"]

print("Countries loaded:", len(countries))
print("Datasets loaded:", len(datasets))

print("\nCountries:")
for country in countries:
    print(f"- {country['code']} | {country['name']} | {country['currency']}")

print("\nDatasets:")
for dataset_name, dataset_info in datasets.items():
    print(f"- {dataset_name} | {dataset_info['dataset_code']} | {dataset_info['frequency']}")