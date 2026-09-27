import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("data/raw")
PROCESSED_DATA_PATH = Path("data/processed")

PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

print("NEXUS Data Cleaning Started")
print("-" * 40)


def clean_dataset(filename):
    input_path = RAW_DATA_PATH / filename
    output_path = PROCESSED_DATA_PATH / filename

    df = pd.read_csv(input_path)

    df = df.drop_duplicates()
    df = df.dropna(how="all")

    text_columns = df.select_dtypes(include="object").columns

    for column in text_columns:
        df[column] = df[column].str.strip()

    date_columns = [
        "date_of_birth",
        "signup_date",
        "order_date",
        "payment_date",
        "last_updated",
        "shipped_date",
        "expected_delivery",
        "actual_delivery",
        "return_date"
    ]

    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    df.to_csv(output_path, index=False)

    print(f"{filename}: {len(df)} rows cleaned")


datasets = [
    "customers.csv",
    "products.csv",
    "orders.csv",
    "order_items.csv",
    "payments.csv",
    "warehouses.csv",
    "inventory.csv",
    "deliveries.csv",
    "returns.csv"
]


for dataset in datasets:
    clean_dataset(dataset)

print("\nAll datasets cleaned successfully.")
