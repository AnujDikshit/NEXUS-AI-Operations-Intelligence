from reorder_service import get_reorder_recommendations


def get_inventory_recommendations():
    recommendations = get_reorder_recommendations()

    results = []

    for item in recommendations:
        (
            product_id,
            product_name,
            category,
            warehouse,
            current_stock,
            reorder_level,
            units_sold_30d,
            avg_daily_demand,
            target_stock,
            recommended_reorder_qty
        ) = item

        qty = float(recommended_reorder_qty)

        if qty > 0:
            stock_ratio = current_stock / max(reorder_level, 1)

            if stock_ratio <= 0.10:
                priority = "Critical"
            elif stock_ratio <= 0.25:
                priority = "High"
            else:
                priority = "Medium"

            results.append({
                "product_id": product_id,
                "product_name": product_name,
                "category": category,
                "warehouse": warehouse,
                "current_stock": current_stock,
                "reorder_level": reorder_level,
                "recommended_reorder_qty": qty,
                "priority": priority,
                "reason": (
    f"Current stock is {current_stock} units, "
    f"while 30-day demand was {units_sold_30d} units. "
    f"Recommended reorder: {qty:.0f} units."
)
            })

    priority_order = {
        "Critical": 1,
        "High": 2,
        "Medium": 3
    }

    results.sort(key=lambda x: (
        priority_order[x["priority"]],
        -x["recommended_reorder_qty"]
    ))

    return results
