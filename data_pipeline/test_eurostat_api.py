from extract.fetch_eurostat import fetch_dataset


params = {
    "geo": "DE",
    "coicop": "CP00",
    "unit": "I15",
    "lang": "en",
}

data = fetch_dataset("prc_hicp_midx", params=params)

print("Top-level keys:")
print(data.keys())

print("\nDataset label:")
print(data.get("label"))

print("\nAvailable dimensions:")
print(data.get("id"))

print("\nSize:")
print(data.get("size"))