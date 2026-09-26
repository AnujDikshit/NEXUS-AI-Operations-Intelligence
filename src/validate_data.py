import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("data/raw")

print("NEXUS Data Validation Started")
print("-" * 40)

csv_files = list(RAW_DATA_PATH.glob("*.csv"))

print(f"CSV files found: {len(csv_files)}")

for file in csv_files:
    df = pd.read_csv(file)

    print(f"\n{file.name}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nChecking missing values...")

for file in csv_files:
    df = pd.read_csv(file)

    missing = df.isnull().sum().sum()

    print(f"{file.name}: {missing} missing values")


    