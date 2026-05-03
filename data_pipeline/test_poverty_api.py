from extract.fetch_eurostat import fetch_dataset


dataset_code = "ilc_li02"

params = {
    "geo": "DE",
    "freq": "A",
    "unit": "PC",
    "indic_il": "LI_R_MD60",
    "sex": "T",
    "age": "TOTAL",
    "lang": "en",
}

data = fetch_dataset(dataset_code, params=params)

print("Top-level keys:")
print(data.keys())

print("\nDataset label:")
print(data.get("label"))

print("\nAvailable dimensions:")
print(data.get("id"))

print("\nSize:")
print(data.get("size"))

print("\nDimension details:")
for dimension_id in data.get("id", []):
    dimension = data["dimension"][dimension_id]
    label = dimension.get("label")
    categories = dimension.get("category", {}).get("label", {})

    print(f"\n{dimension_id}: {label}")
    print("First categories:")
    for code, category_label in list(categories.items())[:15]:
        print(f"  {code}: {category_label}")