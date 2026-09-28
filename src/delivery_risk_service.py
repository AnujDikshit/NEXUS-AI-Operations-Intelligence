from database import get_connection
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score


def get_delivery_risk_predictions():
    connection = get_connection()

    query = """
        SELECT
            d.delivery_id,
            d.order_id,
            d.carrier,
            d.shipped_date,
            d.expected_delivery,
            d.actual_delivery,
            d.delivery_delay_days,
            o.warehouse_id,
            o.total_amount,
            o.shipping_cost,
            EXTRACT(DAY FROM (d.expected_delivery - d.shipped_date)) AS planned_shipping_days,
            EXTRACT(DOW FROM o.order_date) AS order_day_of_week,
            EXTRACT(MONTH FROM o.order_date) AS order_month
        FROM deliveries d
        JOIN orders o
            ON d.order_id = o.order_id
        WHERE d.actual_delivery IS NOT NULL
          AND d.delivery_delay_days IS NOT NULL;
    """

    df = pd.read_sql(query, connection)
    connection.close()

    df["is_delayed"] = (
        df["delivery_delay_days"] > 0
    ).astype(int)

    feature_columns = [
        "carrier",
        "warehouse_id",
        "total_amount",
        "shipping_cost",
        "planned_shipping_days",
        "order_day_of_week",
        "order_month"
    ]

    X = df[feature_columns]
    y = df["is_delayed"]

    categorical_features = [
        "carrier",
        "warehouse_id"
    ]

    numeric_features = [
        "total_amount",
        "shipping_cost",
        "planned_shipping_days",
        "order_day_of_week",
        "order_month"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categorical_features
            ),
            (
                "numeric",
                "passthrough",
                numeric_features
            )
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    random_state=42
                )
            )
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model.fit(X_train, y_train)

    test_predictions = model.predict(X_test)
    test_probabilities = model.predict_proba(X_test)[:, 1]

    print("\nDELIVERY RISK MODEL EVALUATION")
    print("-" * 35)
    print(f"Accuracy : {accuracy_score(y_test, test_predictions):.3f}")
    print(f"Precision: {precision_score(y_test, test_predictions, zero_division=0):.3f}")
    print(f"Recall   : {recall_score(y_test, test_predictions, zero_division=0):.3f}")
    print(f"ROC-AUC  : {roc_auc_score(y_test, test_probabilities):.3f}")

    df["delay_probability"] = (
        model.predict_proba(X)[:, 1] * 100
    )

    df["risk_level"] = pd.cut(
        df["delay_probability"],
        bins=[-1, 30, 60, 100],
        labels=[
            "Low Risk",
            "Medium Risk",
            "High Risk"
        ]
    )

    return df[
        [
            "delivery_id",
            "order_id",
            "carrier",
            "warehouse_id",
            "delay_probability",
            "risk_level",
            "delivery_delay_days"
        ]
    ].sort_values(
        "delay_probability",
        ascending=False
    )
