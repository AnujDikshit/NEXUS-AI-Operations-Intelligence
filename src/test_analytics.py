from analytics_service import get_revenue_by_category, get_revenue_by_warehouse

print("Revenue by Category")
print("-------------------")

for category, revenue in get_revenue_by_category():
    print(f"{category}: ₹{revenue:,.2f}")

print("\nRevenue by Warehouse")
print("--------------------")

for warehouse, revenue in get_revenue_by_warehouse():
    print(f"{warehouse}: ₹{revenue:,.2f}")
