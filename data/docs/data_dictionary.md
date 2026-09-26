# NEXUS — Data Dictionary v1.0

## Purpose

This document defines the database structure used by NEXUS.

The database represents a realistic e-commerce/retail business and supports analytics, machine learning, anomaly detection, forecasting, and decision support.

---

# 1. customers

Stores customer-level information.

| Column | Type | Key | Description |
|---|---|---|---|
| customer_id | BIGINT | PK | Unique customer identifier |
| first_name | VARCHAR | | Customer first name |
| last_name | VARCHAR | | Customer last name |
| gender | VARCHAR | | Customer gender |
| date_of_birth | DATE | | Customer birth date |
| city | VARCHAR | | Customer city |
| state | VARCHAR | | Customer state |
| country | VARCHAR | | Customer country |
| signup_date | DATE | | Account creation date |
| customer_segment | VARCHAR | | Business/customer segment |

---

# 2. products

Stores product catalog information.

| Column | Type | Key | Description |
|---|---|---|---|
| product_id | BIGINT | PK | Unique product identifier |
| product_name | VARCHAR | | Product name |
| category | VARCHAR | | Product category |
| subcategory | VARCHAR | | Product subcategory |
| brand | VARCHAR | | Product brand |
| supplier_id | BIGINT | | Supplier identifier |
| unit_cost | DECIMAL | | Product acquisition cost |
| selling_price | DECIMAL | | Current selling price |

---

# 3. orders

Stores order-level information.

| Column | Type | Key | Description |
|---|---|---|---|
| order_id | BIGINT | PK | Unique order identifier |
| customer_id | BIGINT | FK | Customer placing the order |
| warehouse_id | BIGINT | FK | Fulfillment warehouse |
| order_date | TIMESTAMP | | Order creation timestamp |
| order_status | VARCHAR | | Current order status |
| total_amount | DECIMAL | | Gross order value |
| discount_amount | DECIMAL | | Total discount |
| shipping_cost | DECIMAL | | Shipping cost |

---

# 4. order_items

Stores individual products within an order.

| Column | Type | Key | Description |
|---|---|---|---|
| order_item_id | BIGINT | PK | Unique order item |
| order_id | BIGINT | FK | Related order |
| product_id | BIGINT | FK | Ordered product |
| quantity | INT | | Quantity purchased |
| unit_price | DECIMAL | | Selling price per unit |
| discount | DECIMAL | | Item-level discount |

---

# 5. payments

Stores payment transactions.

| Column | Type | Key | Description |
|---|---|---|---|
| payment_id | BIGINT | PK | Unique payment |
| order_id | BIGINT | FK | Related order |
| payment_date | TIMESTAMP | | Payment timestamp |
| payment_method | VARCHAR | | Payment method |
| payment_status | VARCHAR | | Payment status |
| amount | DECIMAL | | Amount paid |

---

# 6. inventory

Stores product stock information.

| Column | Type | Key | Description |
|---|---|---|---|
| inventory_id | BIGINT | PK | Unique inventory record |
| product_id | BIGINT | FK | Product |
| warehouse_id | BIGINT | FK | Warehouse |
| stock_quantity | INT | | Current stock |
| reorder_level | INT | | Minimum stock threshold |
| last_updated | TIMESTAMP | | Last inventory update |

---

# 7. warehouses

Stores warehouse information.

| Column | Type | Key | Description |
|---|---|---|---|
| warehouse_id | BIGINT | PK | Unique warehouse |
| warehouse_name | VARCHAR | | Warehouse name |
| city | VARCHAR | | Warehouse city |
| state | VARCHAR | | Warehouse state |
| capacity | INT | | Maximum storage capacity |
| operating_cost | DECIMAL | | Operational cost |

---

# 8. deliveries

Stores delivery and logistics information.

| Column | Type | Key | Description |
|---|---|---|---|
| delivery_id | BIGINT | PK | Unique delivery |
| order_id | BIGINT | FK | Related order |
| carrier | VARCHAR | | Delivery carrier |
| shipped_date | TIMESTAMP | | Shipment timestamp |
| expected_delivery | TIMESTAMP | | Expected delivery |
| actual_delivery | TIMESTAMP | | Actual delivery |
| delivery_status | VARCHAR | | Delivery status |
| delivery_delay_days | INT | | Delay duration |

---

# 9. returns

Stores returned-order information.

| Column | Type | Key | Description |
|---|---|---|---|
| return_id | BIGINT | PK | Unique return |
| order_id | BIGINT | FK | Related order |
| product_id | BIGINT | FK | Returned product |
| return_date | DATE | | Return date |
| return_reason | VARCHAR | | Reason for return |
| return_quantity | INT | | Quantity returned |
| refund_amount | DECIMAL | | Refund amount |

---

# Relationships

customers → orders

orders → order_items

products → order_items

orders → payments

products → inventory

warehouses → inventory

warehouses → orders

orders → deliveries

orders → returns

products → returns

---

# NEXUS Analytical Objectives

The database must support:

1. Revenue analysis
2. Customer segmentation
3. Product performance analysis
4. Inventory optimization
5. Demand forecasting
6. Delivery delay prediction
7. Return-rate analysis
8. Anomaly detection
9. Operational risk analysis
10. Business recommendations