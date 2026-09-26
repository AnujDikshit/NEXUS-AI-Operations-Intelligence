# NEXUS Raw Data

This folder contains the original source datasets used by the NEXUS platform.

## Planned Data Sources

- Customers
- Products
- Orders
- Order Items
- Payments
- Warehouses
- Inventory
- Deliveries
- Returns

## Data Rules

- Raw files must remain unchanged.
- Data cleaning will be performed separately.
- Processed datasets will be stored in `data/processed/`.
- No fabricated business results will be presented as real-world results.

## Data Pipeline

Raw Data
↓
Data Validation
↓
Data Cleaning
↓
Data Transformation
↓
Processed Data
↓
SQL / Analytics / ML