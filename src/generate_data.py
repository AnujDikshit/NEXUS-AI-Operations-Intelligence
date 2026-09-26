from faker import Faker
import pandas as pd
import random

fake = Faker("en_IN")

# Reproducibility
Faker.seed(42)
random.seed(42)

print("NEXUS data generator initialized successfully.")

# -----------------------------
# Generate Customers
# -----------------------------

NUM_CUSTOMERS = 10000

customers = []

for customer_id in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        "customer_id": customer_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "gender": random.choice(["Male", "Female"]),
        "date_of_birth": fake.date_of_birth(
            minimum_age=18,
            maximum_age=70
        ),
        "city": fake.city(),
        "state": fake.state(),
        "country": "India",
        "signup_date": fake.date_between(
            start_date="-3y",
            end_date="today"
        ),
        "customer_segment": random.choice([
            "Regular",
            "Premium",
            "VIP"
        ])
    })

customers_df = pd.DataFrame(customers)

print(f"Customers generated: {len(customers_df)}")
print(customers_df.head())

# Save customers data
customers_df.to_csv(
    "data/raw/customers.csv",
    index=False
)

print("customers.csv saved successfully.")

# -----------------------------
# Generate Products
# -----------------------------

NUM_PRODUCTS = 500

products = []

categories = {
    "Electronics": ["Mobile", "Laptop", "Accessories"],
    "Fashion": ["Men", "Women", "Shoes"],
    "Home": ["Furniture", "Kitchen", "Decor"],
    "Beauty": ["Skincare", "Haircare", "Makeup"],
    "Sports": ["Fitness", "Outdoor", "Equipment"]
}

for product_id in range(1, NUM_PRODUCTS + 1):
    category = random.choice(list(categories.keys()))
    subcategory = random.choice(categories[category])

    unit_cost = round(random.uniform(100, 20000), 2)
    selling_price = round(
        unit_cost * random.uniform(1.15, 1.60), 2
    )

    products.append({
        "product_id": product_id,
        "product_name": fake.catch_phrase(),
        "category": category,
        "subcategory": subcategory,
        "brand": fake.company(),
        "supplier_id": random.randint(1, 100),
        "unit_cost": unit_cost,
        "selling_price": selling_price
    })

products_df = pd.DataFrame(products)

products_df.to_csv(
    "data/raw/products.csv",
    index=False
)

print(f"Products generated: {len(products_df)}")
print("products.csv saved successfully.")

# -----------------------------
# Generate Warehouses
# -----------------------------

NUM_WAREHOUSES = 20

warehouses = []

for warehouse_id in range(1, NUM_WAREHOUSES + 1):
    warehouses.append({
        "warehouse_id": warehouse_id,
        "warehouse_name": f"Warehouse {warehouse_id}",
        "city": fake.city(),
        "state": fake.state(),
        "capacity": random.randint(5000, 50000),
        "operating_cost": round(random.uniform(50000, 500000), 2)
    })

warehouses_df = pd.DataFrame(warehouses)

warehouses_df.to_csv(
    "data/raw/warehouses.csv",
    index=False
)

print(f"Warehouses generated: {len(warehouses_df)}")
print("warehouses.csv saved successfully.")

# -----------------------------
# Generate Orders
# -----------------------------

NUM_ORDERS = 50000

orders = []

order_statuses = [
    "Completed",
    "Completed",
    "Completed",
    "Shipped",
    "Processing",
    "Cancelled"
]

for order_id in range(1, NUM_ORDERS + 1):
    customer_id = random.randint(1, NUM_CUSTOMERS)
    warehouse_id = random.randint(1, NUM_WAREHOUSES)

    order_date = fake.date_time_between(
        start_date="-2y",
        end_date="now"
    )

    total_amount = round(random.uniform(300, 50000), 2)
    discount_amount = round(
        total_amount * random.uniform(0, 0.20), 2
    )
    shipping_cost = round(
        random.uniform(40, 500), 2
    )

    orders.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "warehouse_id": warehouse_id,
        "order_date": order_date,
        "order_status": random.choice(order_statuses),
        "total_amount": total_amount,
        "discount_amount": discount_amount,
        "shipping_cost": shipping_cost
    })

orders_df = pd.DataFrame(orders)

orders_df.to_csv(
    "data/raw/orders.csv",
    index=False
)

print(f"Orders generated: {len(orders_df)}")
print("orders.csv saved successfully.")

# -----------------------------
# Generate Order Items
# -----------------------------

order_items = []

for order_id in range(1, NUM_ORDERS + 1):
    num_items = random.randint(1, 5)

    selected_products = random.sample(
        range(1, NUM_PRODUCTS + 1),
        num_items
    )

    for product_id in selected_products:
        product = products_df.loc[
            products_df["product_id"] == product_id
        ].iloc[0]

        quantity = random.randint(1, 5)
        unit_price = product["selling_price"]

        discount = round(
            unit_price * random.uniform(0, 0.15),
            2
        )

        order_items.append({
            "order_item_id": len(order_items) + 1,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price,
            "discount": discount
        })

order_items_df = pd.DataFrame(order_items)

order_items_df.to_csv(
    "data/raw/order_items.csv",
    index=False
)

print(f"Order items generated: {len(order_items_df)}")
print("order_items.csv saved successfully.")

# -----------------------------
# Generate Payments
# -----------------------------

payments = []

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery"
]

payment_statuses = [
    "Paid",
    "Paid",
    "Paid",
    "Failed",
    "Pending"
]

for payment_id, order_id in enumerate(
    range(1, NUM_ORDERS + 1),
    start=1
):
    order = orders_df.loc[
        orders_df["order_id"] == order_id
    ].iloc[0]

    payments.append({
        "payment_id": payment_id,
        "order_id": order_id,
        "payment_date": order["order_date"],
        "payment_method": random.choice(payment_methods),
        "payment_status": random.choice(payment_statuses),
        "amount": order["total_amount"]
    })

payments_df = pd.DataFrame(payments)

payments_df.to_csv(
    "data/raw/payments.csv",
    index=False
)

print(f"Payments generated: {len(payments_df)}")
print("payments.csv saved successfully.")

# -----------------------------
# Generate Inventory
# -----------------------------

inventory = []

for product_id in range(1, NUM_PRODUCTS + 1):
    for warehouse_id in range(1, NUM_WAREHOUSES + 1):

        stock_quantity = random.randint(0, 1000)
        reorder_level = random.randint(50, 200)

        inventory.append({
            "inventory_id": len(inventory) + 1,
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "stock_quantity": stock_quantity,
            "reorder_level": reorder_level,
            "last_updated": fake.date_time_between(
                start_date="-30d",
                end_date="now"
            )
        })

inventory_df = pd.DataFrame(inventory)

inventory_df.to_csv(
    "data/raw/inventory.csv",
    index=False
)

print(f"Inventory records generated: {len(inventory_df)}")
print("inventory.csv saved successfully.")

# -----------------------------
# Generate Deliveries
# -----------------------------

deliveries = []

carriers = [
    "Delhivery",
    "Blue Dart",
    "Ecom Express",
    "DTDC",
    "XpressBees"
]

delivery_statuses = [
    "Delivered",
    "Delivered",
    "Delivered",
    "In Transit",
    "Delayed"
]

for delivery_id, order_id in enumerate(
    range(1, NUM_ORDERS + 1),
    start=1
):
    order = orders_df.loc[
        orders_df["order_id"] == order_id
    ].iloc[0]

    shipped_date = order["order_date"]

    expected_delivery = shipped_date + pd.Timedelta(
        days=random.randint(2, 7)
    )

    actual_delivery = expected_delivery + pd.Timedelta(
        days=random.randint(-2, 4)
    )

    delay_days = max(
        0,
        (actual_delivery - expected_delivery).days
    )

    deliveries.append({
        "delivery_id": delivery_id,
        "order_id": order_id,
        "carrier": random.choice(carriers),
        "shipped_date": shipped_date,
        "expected_delivery": expected_delivery,
        "actual_delivery": actual_delivery,
        "delivery_status": random.choice(delivery_statuses),
        "delivery_delay_days": delay_days
    })

deliveries_df = pd.DataFrame(deliveries)

deliveries_df.to_csv(
    "data/raw/deliveries.csv",
    index=False
)

print(f"Deliveries generated: {len(deliveries_df)}")
print("deliveries.csv saved successfully.")

# -----------------------------
# Generate Returns
# -----------------------------

returns = []

return_reasons = [
    "Damaged",
    "Wrong Product",
    "Quality Issue",
    "Size Issue",
    "Changed Mind"
]

# Sample a smaller subset of orders for returns
return_orders = random.sample(
    range(1, NUM_ORDERS + 1),
    int(NUM_ORDERS * 0.08)
)

for return_id, order_id in enumerate(return_orders, start=1):

    order_items_for_order = order_items_df[
        order_items_df["order_id"] == order_id
    ]

    item = order_items_for_order.sample(1).iloc[0]

    return_quantity = random.randint(
        1,
        int(item["quantity"])
    )

    refund_amount = round(
        item["unit_price"] * return_quantity
        - item["discount"],
        2
    )

    returns.append({
        "return_id": return_id,
        "order_id": order_id,
        "product_id": item["product_id"],
        "return_date": fake.date_between(
            start_date="-1y",
            end_date="today"
        ),
        "return_reason": random.choice(return_reasons),
        "return_quantity": return_quantity,
        "refund_amount": refund_amount
    })

returns_df = pd.DataFrame(returns)

returns_df.to_csv(
    "data/raw/returns.csv",
    index=False
)

print(f"Returns generated: {len(returns_df)}")
print("returns.csv saved successfully.")

