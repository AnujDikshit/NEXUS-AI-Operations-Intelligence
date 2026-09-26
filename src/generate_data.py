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