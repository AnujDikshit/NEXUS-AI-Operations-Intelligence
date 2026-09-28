from database import get_connection
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def get_ml_demand_forecast():
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

    train = df.dropna().copy()

    feature_columns = [
        "lag_1",
        "lag_2",
        "lag_3",
        "lag_4",
        "lag_5",
        "lag_6",
        "lag_7",
        "day_of_week"
    ]

    X = train[feature_columns]
    y = train["order_count"]

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X, y)

    history = df[["order_day", "order_count"]].copy()

    forecasts = []

    for _ in range(7):
        next_date = history["order_day"].max() + pd.Timedelta(days=1)

        lag_values = [
            history["order_count"].iloc[-lag]
            for lag in range(1, 8)
        ]

        features = pd.DataFrame([{
            "lag_1": lag_values[0],
            "lag_2": lag_values[1],
            "lag_3": lag_values[2],
            "lag_4": lag_values[3],
            "lag_5": lag_values[4],
            "lag_6": lag_values[5],
            "lag_7": lag_values[6],
            "day_of_week": next_date.dayofweek
        }])

        prediction = max(0, model.predict(features)[0])

        forecasts.append({
            "date": next_date,
            "predicted_orders": round(prediction, 2)
        })

        history = pd.concat([
            history,
            pd.DataFrame([{
                "order_day": next_date,
                "order_count": prediction
            }])
        ], ignore_index=True)

    return forecasts
