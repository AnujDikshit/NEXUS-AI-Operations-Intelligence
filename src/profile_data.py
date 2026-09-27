import pandas as pd
from pathlib import Path

PROCESSED_DATA_PATH = Path("data/processed")

print("NEXUS Data Profiling Started")
print("-" * 40)

def profile_dataset(filename):
    file_path = PROCESSED_DATA_PATH / filename

    df = pd.read_csv(file_path)

    print(f"\n{'=' * 50}")
    print(f"Dataset: {filename}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Duplicate Rows: {df.duplicated().sum()}")
    print(f"Missing Values: {df.isnull().sum().sum()}")

    print("\nData Types:")
    print(df.dtypes)


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
    profile_dataset(dataset)

print("\nData profiling completed.")