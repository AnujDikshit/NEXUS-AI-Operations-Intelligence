# NEXUS — AI-Powered Business Operations Intelligence

NEXUS is an end-to-end business intelligence platform that combines SQL analytics, machine learning, anomaly detection, root-cause analysis, forecasting, and AI-powered business querying to turn operational data into actionable insights.


## Key Features

- Business KPI monitoring with PostgreSQL
- Revenue and customer-segment analytics
- Inventory risk and reorder intelligence
- Demand forecasting with machine learning
- Revenue anomaly detection
- Automated revenue root-cause analysis
- Delivery performance and risk analysis
- Payment and return analysis
- AI-powered business query layer
- Action-oriented inventory recommendations
- FastAPI backend
- Streamlit business intelligence dashboard
- Automated backend tests with pytest


## Tech Stack

### Data & Database
- Python
- PostgreSQL
- SQL
- Pandas
- NumPy

### Machine Learning
- Scikit-learn
- Random Forest
- Logistic Regression
- Time-series forecasting
- Anomaly detection

### Backend
- FastAPI
- Pydantic
- REST API

### Dashboard & Visualization
- Streamlit
- Matplotlib
- Power BI

### Engineering
- Git
- GitHub
- Pytest
- Virtual Environment


## Project Modules

| Module | Purpose |
|---|---|
| Data Pipeline | Generates, validates, cleans, and profiles operational data |
| SQL Analytics | Business KPIs and operational analysis using PostgreSQL |
| Revenue Intelligence | Category, warehouse, segment, and revenue analysis |
| Inventory Intelligence | Stock risk, demand coverage, and reorder analysis |
| Demand Forecasting | ML-based order demand forecasting |
| Anomaly Detection | Detects unusual revenue spikes and drops |
| Root Cause Analysis | Identifies supporting and non-supporting business signals |
| Delivery Intelligence | Carrier performance and delivery-risk analysis |
| Recommendation Engine | Converts inventory signals into recommended actions |
| AI Query Layer | Converts business questions into structured database queries |
| FastAPI Backend | Exposes NEXUS intelligence through REST APIs |
| Streamlit Dashboard | Interactive business operations command center |
| Testing | Automated validation of database, KPI, and analytics services |


## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API health check |
| GET | `/kpis` | Returns core business KPIs |
| POST | `/query` | Processes natural-language business questions |
| GET | `/recommendations` | Returns inventory action recommendations |

Interactive API documentation is available through FastAPI Swagger UI at `/docs` when the API is running locally.

## Testing

Current automated backend test suite: **4 passed, 0 failed**.

Run tests with: `python -m pytest -v`
