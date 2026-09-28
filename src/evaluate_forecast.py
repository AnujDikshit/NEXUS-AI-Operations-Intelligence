from database import get_connection
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


def evaluate_forecast():
    connection = get_connection()

    query = """
        SELECT
            DATE(order_date) AS order_day,
            COUNT(*) AS order_count
        FROM orders
        WHERE order_status <> 'Cancelled'
        GROUP BY DATE(order_date)
        ORDER BY order_day;
    """

    df = pd.read_sql(query, connection)
    connection.close()

    df["order_day"] = pd.to_datetime(df["order_day"])

    df = df[df["order_day"] < df["order_day"].max()].copy()

    date_range = pd.date_range(
        start=df["order_day"].min(),
        end=df["order_day"].max(),
        freq="D"
    )

    df = (
        df.set_index("order_day")
        .reindex(date_range, fill_value=0)
        .rename_axis("order_day")
        .reset_index()
    )

    df["order_count"] = df["order_count"].astype(float)

    for lag in range(1, 8):
        df[f"lag_{lag}"] = df["order_count"].shift(lag)

    df["day_of_week"] = df["order_day"].dt.dayofweek

    feature_columns = [
        "lag_1", "lag_2", "lag_3", "lag_4",
        "lag_5", "lag_6", "lag_7",
        "day_of_week"
    ]

    df = df.dropna().reset_index(drop=True)

    train = df.iloc[:-7]
    test = df.iloc[-7:]

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    model.fit(train[feature_columns], train["order_count"])

    predictions = model.predict(test[feature_columns])

    mae = mean_absolute_error(
        test["order_count"],
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            test["order_count"],
            predictions
        )
    )

    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "actual": test["order_count"].tolist(),
        "predicted": [round(float(x), 2) for x in predictions]
    }


if __name__ == "__main__":
    result = evaluate_forecast()

    print("\nNEXUS ML FORECAST EVALUATION")
    print("-" * 35)
    print(f"MAE  : {result['mae']}")
    print(f"RMSE : {result['rmse']}")

    print("\nActual vs Predicted")
    print("-" * 35)

    for actual, predicted in zip(
        result["actual"],
        result["predicted"]
    ):
        print(f"Actual: {actual:.0f} | Predicted: {predicted:.2f}")
