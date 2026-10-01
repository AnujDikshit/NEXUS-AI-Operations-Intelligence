from pathlib import Path
import pandas as pd


def load_dataset(file_path):
    path = Path(file_path)

    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)

    elif path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(path)

    else:
        raise ValueError(
            "Unsupported file type. Please upload CSV or Excel."
        )


def detect_column_types(df):
    numeric = df.select_dtypes(include="number").columns.tolist()
    categorical = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    datetime_columns = []

    for column in categorical.copy():
        converted = pd.to_datetime(
            df[column],
            format="mixed",
            errors="coerce"
        )

        if converted.notna().mean() >= 0.8:
            datetime_columns.append(column)
            categorical.remove(column)

    return {
        "numeric": numeric,
        "categorical": categorical,
        "datetime": datetime_columns
    }


def profile_dataset(df):
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_names": df.columns.tolist(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "column_types": detect_column_types(df)
    }


def data_quality_report(df):
    missing = df.isna().sum()

    return {
        "total_missing_values": int(missing.sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "columns_with_missing_values": {
            column: {
                "missing_count": int(missing[column]),
                "missing_percentage": round(
                    missing[column] / len(df) * 100, 2
                )
            }
            for column in df.columns
            if missing[column] > 0
        },
        "unique_values": {
            column: int(df[column].nunique(dropna=True))
            for column in df.columns
        }
    }
