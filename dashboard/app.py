import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from ai_query_service import execute_interpreted_query
from root_cause_service import get_revenue_root_causes, generate_rca_explanation, build_revenue_root_cause
import sys
from pathlib import Path

import requests
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "src"))

from kpi_service import get_kpi_summary
from analytics_service import (
    get_revenue_by_category,
    get_revenue_by_warehouse,
    get_inventory_risk,
    get_inventory_risk_summary,
    get_revenue_by_segment,
    get_delivery_performance,
    get_payment_performance,
    get_return_analysis,
    get_revenue_anomalies
)

st.set_page_config(
    page_title="NEXUS",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 NEXUS — AI Operations Intelligence")
st.caption("Business Operations Command Center")

import requests

response = requests.get("http://127.0.0.1:8000/kpis", timeout=5)
response.raise_for_status()
kpi_data = response.json()

kpi = (
    kpi_data["total_revenue"],
    kpi_data["total_orders"],
    kpi_data["average_order_value"],
    kpi_data["returned_orders"],
    kpi_data["return_rate"]
)

total_revenue = kpi[0]
total_orders = kpi[1]
average_order_value = kpi[2]
returned_orders = kpi[3]
return_rate = kpi[4]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Revenue", f"₹{total_revenue:,.2f}")

with col2:
    st.metric("Total Orders", f"{total_orders:,}")

with col3:
    st.metric("Average Order Value", f"₹{average_order_value:,.2f}")

with col4:
    st.metric("Returned Orders", f"{returned_orders:,}")

with col5:
    st.metric("Return Rate", f"{return_rate:.2f}%")

st.divider()

st.header("📊 Revenue Analytics")

category_data = get_revenue_by_category()

category_df = pd.DataFrame(
    category_data,
    columns=["Category", "Revenue"]
)

category_df["Revenue"] = category_df["Revenue"].astype(float)

st.subheader("💰 Revenue by Category")

st.bar_chart(
    category_df,
    x="Category",
    y="Revenue"
)

warehouse_data = get_revenue_by_warehouse()

warehouse_df = pd.DataFrame(
    warehouse_data,
    columns=["Warehouse", "Revenue"]
)

warehouse_df["Revenue"] = warehouse_df["Revenue"].astype(float)

st.subheader("🏭 Revenue by Warehouse")

st.bar_chart(
    warehouse_df,
    x="Warehouse",
    y="Revenue"
)

st.divider()

st.header("📦 Inventory Intelligence")

inventory_data = get_inventory_risk()

inventory_df = pd.DataFrame(
    inventory_data,
    columns=[
        "Product",
        "Category",
        "Warehouse",
        "Current Stock",
        "Reorder Level",
        "Shortage"
    ]
)

st.subheader("⚠️ Products Requiring Reorder")

st.dataframe(
    inventory_df,
    use_container_width=True,
    hide_index=True
)

inventory_summary = get_inventory_risk_summary()

products_at_risk = inventory_summary[0]
total_shortage = inventory_summary[1]
warehouses_affected = inventory_summary[2]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Products at Risk", f"{products_at_risk:,}")

with col2:
    st.metric("Total Stock Shortage", f"{total_shortage:,}")

with col3:
    st.metric("Warehouses Affected", f"{warehouses_affected:,}")

st.divider()

st.header("Customer Intelligence")

segment_data = get_revenue_by_segment()

segment_df = pd.DataFrame(
    segment_data,
    columns=[
        "Customer Segment",
        "Orders",
        "Revenue",
        "Average Order Value"
    ]
)

segment_df["Revenue"] = segment_df["Revenue"].astype(float)
segment_df["Average Order Value"] = segment_df["Average Order Value"].astype(float)

st.subheader("Revenue by Customer Segment")

st.dataframe(
    segment_df,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    segment_df,
    x="Customer Segment",
    y="Revenue"
)

st.divider()

st.header("Delivery Intelligence")

delivery_data = get_delivery_performance()

delivery_df = pd.DataFrame(
    delivery_data,
    columns=[
        "Carrier",
        "Total Deliveries",
        "Delayed Deliveries",
        "Delay Rate",
        "Average Delay Days"
    ]
)

delivery_df["Delay Rate"] = delivery_df["Delay Rate"].astype(float)
delivery_df["Average Delay Days"] = delivery_df["Average Delay Days"].astype(float)

st.subheader("Carrier Delivery Performance")

st.dataframe(
    delivery_df,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    delivery_df,
    x="Carrier",
    y="Delay Rate"
)

st.divider()

st.header("Payment Intelligence")

payment_data = get_payment_performance()

payment_df = pd.DataFrame(
    payment_data,
    columns=[
        "Payment Method",
        "Total Payments",
        "Failed Payments",
        "Failure Rate"
    ]
)

payment_df["Failure Rate"] = payment_df["Failure Rate"].astype(float)

st.subheader("Payment Method Performance")

st.dataframe(
    payment_df,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    payment_df,
    x="Payment Method",
    y="Failure Rate"
)

st.divider()

st.header("Return Intelligence")

return_data = get_return_analysis()

return_df = pd.DataFrame(
    return_data,
    columns=[
        "Return Reason",
        "Return Count",
        "Return Percentage"
    ]
)

return_df["Return Percentage"] = return_df["Return Percentage"].astype(float)

st.subheader("Return Reasons")

st.dataframe(
    return_df,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    return_df,
    x="Return Reason",
    y="Return Count"
)

st.divider()

st.header("Revenue Anomaly Detection")

anomaly_data = get_revenue_anomalies()

anomaly_df = pd.DataFrame(
    anomaly_data,
    columns=[
        "Date",
        "Revenue",
        "7-Day Rolling Average",
        "Deviation %",
        "Anomaly Type"
    ]
)

anomaly_df["Revenue"] = anomaly_df["Revenue"].astype(float)
anomaly_df["7-Day Rolling Average"] = anomaly_df["7-Day Rolling Average"].astype(float)
anomaly_df["Deviation %"] = anomaly_df["Deviation %"].astype(float)

st.subheader("Detected Revenue Anomalies")

st.dataframe(
    anomaly_df,
    use_container_width=True,
    hide_index=True
)

st.subheader("Anomaly Summary")

total_anomalies = len(anomaly_df)
revenue_spikes = (anomaly_df["Anomaly Type"] == "Revenue Spike").sum()
revenue_drops = (anomaly_df["Anomaly Type"] == "Revenue Drop").sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Anomalies", f"{total_anomalies:,}")

with col2:
    st.metric("Revenue Spikes", f"{revenue_spikes:,}")

with col3:
    st.metric("Revenue Drops", f"{revenue_drops:,}")
from forecast_service import get_demand_forecast

st.divider()

st.header("Demand Forecasting")

forecast_data = get_demand_forecast()

forecast_df = pd.DataFrame(
    forecast_data,
    columns=[
        "Date",
        "Actual Orders",
        "7-Day Forecast"
    ]
)

forecast_df["Actual Orders"] = forecast_df["Actual Orders"].astype(float)
forecast_df["7-Day Forecast"] = forecast_df["7-Day Forecast"].astype(float)

st.subheader("Actual Demand vs 7-Day Forecast")

st.line_chart(
    forecast_df.set_index("Date")[["Actual Orders", "7-Day Forecast"]]
)

st.dataframe(
    forecast_df.tail(30),
    use_container_width=True,
    hide_index=True
)
from ml_forecast_service import get_ml_demand_forecast
from evaluate_forecast import evaluate_forecast

st.divider()

st.header("ML Demand Forecast")

evaluation = evaluate_forecast()

st.subheader("Model Performance")

col1, col2 = st.columns(2)

with col1:
    st.metric("MAE", f"{evaluation['mae']:.2f} orders/day")

with col2:
    st.metric("RMSE", f"{float(evaluation['rmse']):.2f} orders/day")



ml_forecast_data = get_ml_demand_forecast()

ml_forecast_df = pd.DataFrame(ml_forecast_data)

ml_forecast_df = ml_forecast_df.rename(
    columns={
        "date": "Date",
        "predicted_orders": "Predicted Orders"
    }
)

ml_forecast_df["Date"] = pd.to_datetime(ml_forecast_df["Date"])
ml_forecast_df["Predicted Orders"] = ml_forecast_df["Predicted Orders"].astype(float)

st.subheader("Next 7 Days — Predicted Order Demand")

st.line_chart(
    ml_forecast_df.set_index("Date")[["Predicted Orders"]]
)

st.dataframe(
    ml_forecast_df,
    use_container_width=True,
    hide_index=True
)
from inventory_demand_service import get_inventory_demand_intelligence
st.divider()

st.header("Inventory Demand Intelligence")

inventory_demand_data = get_inventory_demand_intelligence()

inventory_demand_df = pd.DataFrame(
    inventory_demand_data,
    columns=[
        "Product ID",
        "Product",
        "Category",
        "Warehouse",
        "Current Stock",
        "Reorder Level",
        "Units Sold (30D)",
        "Avg Daily Demand",
        "Estimated Stock Days",
        "Inventory Status"
    ]
)

st.subheader("Inventory Risk Based on Demand")

status_counts = inventory_demand_df["Inventory Status"].value_counts()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Critical", int(status_counts.get("Critical", 0)))

with col2:
    st.metric("High Risk", int(status_counts.get("High Risk", 0)))

with col3:
    st.metric("Medium Risk", int(status_counts.get("Medium Risk", 0)))

with col4:
    st.metric("Healthy", int(status_counts.get("Healthy", 0)))

st.dataframe(
    inventory_demand_df.head(50),
    use_container_width=True,
    hide_index=True
)
from reorder_service import get_reorder_recommendations
st.divider()

st.header("Reorder Recommendations")

reorder_data = get_reorder_recommendations()

reorder_df = pd.DataFrame(
    reorder_data,
    columns=[
        "Product ID",
        "Product",
        "Category",
        "Warehouse",
        "Current Stock",
        "Reorder Level",
        "Units Sold (30D)",
        "Avg Daily Demand",
        "Target Stock",
        "Recommended Reorder Qty"
    ]
)

st.subheader("Products Requiring Replenishment")

total_reorder_units = reorder_df["Recommended Reorder Qty"].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Products Requiring Reorder",
        f"{len(reorder_df):,}"
    )

with col2:
    st.metric(
        "Total Recommended Units",
        f"{int(total_reorder_units):,}"
    )

st.dataframe(
    reorder_df.head(50),
    use_container_width=True,
    hide_index=True
)
from forecast_reorder_service import get_forecast_adjusted_reorder
st.divider()

st.header("Forecast-Aware Reorder Recommendations")

forecast_reorder_data = get_forecast_adjusted_reorder()

forecast_reorder_df = pd.DataFrame(forecast_reorder_data)

forecast_reorder_df = forecast_reorder_df.rename(
    columns={
        "product_id": "Product ID",
        "product_name": "Product",
        "category": "Category",
        "warehouse": "Warehouse",
        "current_stock": "Current Stock",
        "reorder_level": "Reorder Level",
        "avg_daily_demand": "Avg Daily Demand",
        "forecast_adjusted_daily_demand": "Forecast-Adjusted Daily Demand",
        "recommended_reorder_qty": "Recommended Reorder Qty"
    }
)

total_forecast_reorder_units = forecast_reorder_df[
    "Recommended Reorder Qty"
].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Products Requiring Reorder",
        f"{len(forecast_reorder_df):,}"
    )

with col2:
    st.metric(
        "Forecast-Adjusted Reorder Units",
        f"{int(total_forecast_reorder_units):,}"
    )

st.subheader("Forecast-Aware Replenishment Plan")

st.dataframe(
    forecast_reorder_df.head(50),
    use_container_width=True,
    hide_index=True
)
from explainability_service import get_inventory_risk_explanations
st.divider()

st.header("Why Is This Product At Risk?")

explanation_data = get_inventory_risk_explanations()

explanation_df = pd.DataFrame(explanation_data)

explanation_df = explanation_df.rename(
    columns={
        "product_id": "Product ID",
        "product_name": "Product",
        "category": "Category",
        "warehouse": "Warehouse",
        "current_stock": "Current Stock",
        "reorder_level": "Reorder Level",
        "units_sold_30d": "Units Sold (30D)",
        "avg_daily_demand": "Avg Daily Demand",
        "risk_reasons": "Why At Risk"
    }
)

st.dataframe(
    explanation_df.head(50),
    use_container_width=True,
    hide_index=True
)
st.subheader("Root Cause Analysis")

rca_events = get_revenue_root_causes()

if rca_events:
    latest_event = max(rca_events, key=lambda x: x["issue_date"])

    st.write(
        generate_rca_explanation(latest_event["issue_date"])
    )

    rca_result = build_revenue_root_cause(
        latest_event["issue_date"]
    )

    if rca_result["drivers"]:
        st.write("Supporting Evidence")
        st.dataframe(
            pd.DataFrame(rca_result["drivers"]),
            use_container_width=True
        )

    if rca_result["non_supporting_evidence"]:
        st.write("Non-Supporting Evidence")
        st.dataframe(
            pd.DataFrame(rca_result["non_supporting_evidence"]),
            use_container_width=True
        )
else:
    st.info("No revenue anomalies detected.")
st.subheader("Ask NEXUS")

business_question = st.text_input(
    "Ask a business question",
    placeholder="e.g. Which warehouse has the highest revenue?"
)

if business_question:
    response = requests.post(
        "http://127.0.0.1:8000/query",
        json={"question": business_question},
        timeout=10
    )
    response.raise_for_status()
    result = response.json()

    if result["intent"] == "LATEST_REVENUE_RCA":
        data = result["data"]

        st.markdown("### Revenue Root Cause Analysis")
        st.write(data["explanation"])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Revenue Deviation", f'{data["deviation_percent"]:+.2f}%')

        with col2:
            st.metric("Actual Revenue", f'₹{data["actual_revenue"]:,.2f}')

        with col3:
            st.metric("Baseline Revenue", f'₹{data["baseline_revenue"]:,.2f}')

    elif result["intent"] == "TOP_REVENUE_WAREHOUSE":
        data = result["data"]
        st.write(f"{data['warehouse']} has the highest revenue, generating ₹{data['revenue']:,.2f}.")

    elif result["intent"] == "TOP_REVENUE_CATEGORY":
        data = result["data"]
        st.write(f"{data['category']} is the highest-revenue category, generating ₹{data['revenue']:,.2f}.")

    elif result["intent"] == "TOP_REVENUE_SEGMENT":
        data = result["data"]
        st.write(f"{data['segment']} is the highest-revenue customer segment, generating ₹{data['revenue']:,.2f}.")

    elif result["intent"] == "DEMAND_FORECAST":
        data = result["data"]

        st.markdown("### 7-Day Demand Forecast")

        forecast_df = pd.DataFrame(data["forecast"])

        forecast_df = forecast_df.rename(
            columns={
                "date": "Date",
                "predicted_orders": "Predicted Orders"
            }
        )

        st.dataframe(
            forecast_df,
            use_container_width=True,
            hide_index=True
        )

    elif result["intent"] == "DELIVERY_RISK":
        data = result["data"]

        st.markdown("### Delivery Risk Monitoring")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Deliveries", f'{data["total_deliveries"]:,}')

        with col2:
            st.metric("High Risk", f'{data["high_risk"]:,}')

        with col3:
            st.metric("Medium Risk", f'{data["medium_risk"]:,}')

        st.caption(
            "Risk monitoring only. The current model has limited predictive signal "
            "(ROC-AUC 0.506) and should not be interpreted as a reliable predictor."
        )

    elif result["intent"] == "PRODUCTS_REQUIRING_REORDER":
        data = result["data"]

        st.write(
            f"{data['products_requiring_reorder']:,} products currently require reorder."
        )

        recommendations = data.get("recommendations", [])

        if recommendations:
            recommendation_df = pd.DataFrame(recommendations)

            st.dataframe(
                recommendation_df[
                    [
                        "product_id",
                        "product_name",
                        "category",
                        "warehouse",
                        "current_stock",
                        "units_sold_30d",
                        "recommended_reorder_qty"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

    else:
        st.info("I could not identify that business question.")
st.subheader("Recommended Actions")

from recommendation_service import get_inventory_recommendations

recommendations = get_inventory_recommendations()

if recommendations:
    recommendation_df = pd.DataFrame(recommendations)

    total_products = len(recommendations)
    critical_count = (recommendation_df["priority"] == "Critical").sum()
    high_count = (recommendation_df["priority"] == "High").sum()
    total_reorder_units = recommendation_df["recommended_reorder_qty"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Products Requiring Action", f"{total_products:,}")
    col2.metric("Critical", f"{critical_count:,}")
    col3.metric("High Priority", f"{high_count:,}")
    col4.metric("Recommended Reorder Units", f"{total_reorder_units:,.0f}")

    st.dataframe(
        recommendation_df[
            [
                "priority",
                "product_id",
                "product_name",
                "category",
                "warehouse",
                "current_stock",
                "reorder_level",
                "recommended_reorder_qty",
                "reason"
            ]
        ],
        use_container_width=True
    )
else:
    st.info("No inventory recommendations available.")
