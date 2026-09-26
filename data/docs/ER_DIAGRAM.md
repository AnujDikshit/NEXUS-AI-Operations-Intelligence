# NEXUS — Entity Relationship Diagram

## Core Entities

- Customers
- Orders
- Order Items
- Products
- Payments
- Inventory
- Warehouses
- Deliveries
- Returns

## Relationships

Customers
→ Orders

Orders
→ Order Items
→ Payments
→ Deliveries
→ Returns

Products
→ Order Items
→ Inventory
→ Returns

Warehouses
→ Orders
→ Inventory

## Relationship Details

- One Customer can place many Orders.
- One Order can contain many Order Items.
- One Product can appear in many Order Items.
- One Order can have one or more Payments.
- One Product can exist in multiple Warehouses through Inventory.
- One Warehouse can store many Products.
- One Order has a Delivery record.
- One Order can have Returns.
- One Product can have multiple Return records.

## Analytical Flow

Customer
↓
Order
↓
Order Items
↓
Product
↓
Inventory

Order
↓
Payment

Order
↓
Delivery

Order
↓
Return

Warehouse
↓
Inventory