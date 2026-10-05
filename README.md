# Retail ETL Pipeline

A Python-based ETL pipeline that extracts retail sales data from multiple sources, cleans and validates the data, loads it into a SQLite star-schema warehouse, and generates analytical business insights.

## Overview

This project demonstrates an end-to-end retail data engineering workflow:

**Extract → Transform → Validate → Load → Analyze**

The pipeline processes data from three source files, performs data cleaning and quality validation, loads the cleaned data into a dimensional warehouse, and executes analytical SQL queries to generate business insights.

## Architecture

```text
                 ┌─────────────────┐
                 │   Source Data   │
                 │                 │
                 │ CSV + JSON      │
                 │ 3 Sources       │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │     EXTRACT     │
                 │ Read 3 Sources  │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   TRANSFORM     │
                 │ Clean & Dedup   │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │    VALIDATE     │
                 │   8 Data Checks │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │      LOAD       │
                 │ SQLite Star     │
                 │     Schema      │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │     ANALYZE     │
                 │ 8 SQL Queries   │
                 └─────────────────┘
```

## Features

- Multi-source data ingestion
- CSV and JSON processing
- Data cleaning and deduplication
- Data quality validation
- SQLite data warehouse
- Star-schema dimensional modeling
- Fact and dimension tables
- Automated analytical SQL queries
- Pipeline logging
- Reproducible synthetic data generation

## Project Structure

```text
retail-etl/
│
├── data/
│   ├── source1.csv
│   ├── source2.csv
│   └── source3.json
│
├── elt.py
├── generate_data.py
├── README.md
├── .gitignore
├── pipeline.log
└── warehouse.db
```

## Data Pipeline

### 1. Extract

The pipeline reads retail sales records from three different source files.

The generated dataset contains:

- **3,080 raw records**
- **3 source systems**

### 2. Transform

The transformation stage cleans the incoming data and removes invalid or duplicate records.

```text
Raw records:       3,080
Clean records:     2,850
Records removed:     230
```

### 3. Validate

The pipeline performs eight automated data-quality checks:

| Validation | Result |
|---|---|
| No null `order_id` | PASS |
| `order_id` uniqueness | PASS |
| No null `customer_id` | PASS |
| Positive order amount | PASS |
| Valid dates | PASS |
| No null product | PASS |
| Category present | PASS |
| Quantity >= 1 | PASS |

**Result: 8/8 validation checks passed.**

### 4. Load

Cleaned data is loaded into a SQLite warehouse using a star-schema design.

### Warehouse Schema

```text
                 ┌───────────────┐
                 │   dim_date    │
                 └───────┬───────┘
                         │
                         │
┌─────────────────┐      ▼      ┌──────────────────┐
│ dim_customer    │──── fact_sales ────│ dim_product │
└─────────────────┘             └──────────────────┘
```

Tables:

- `fact_sales`
- `dim_date`
- `dim_product`
- `dim_customer`

## Analytics

The pipeline automatically generates eight analytical outputs:

1. Top 5 products by revenue
2. Revenue by category
3. Monthly revenue trend
4. Top 5 customers by spending
5. Average order value
6. Orders per month
7. Revenue per product
8. Total quantity sold

## Sample Results

### Top Products by Revenue

| Product | Revenue |
|---|---:|
| Cable | 863,261.52 |
| Tablet | 851,469.23 |
| Laptop | 831,310.54 |
| Phone | 829,990.42 |
| Monitor | 817,920.94 |

### Revenue by Category

| Category | Revenue |
|---|---:|
| Electronics | 3,330,691.13 |
| Accessories | 2,423,571.22 |
| Audio | 771,556.82 |

### Overall Metrics

- **Clean records:** 2,850
- **Total quantity sold:** 8,606
- **Average order value:** 2,289.76
- **Validation checks passed:** 8/8

## Technologies

- **Python 3.11**
- **Pandas**
- **NumPy**
- **SQLite**
- **SQL**
- **Python logging**
- **Git / GitHub**

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/pujitha-mule/retail-etl.git
cd retail-etl
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install pandas numpy
```

## Run the Pipeline

### Generate source data

```powershell
python generate_data.py
```

Expected output:

```text
Generated 3080 rows across 3 sources
```

### Run the ETL pipeline

```powershell
python elt.py
```

Expected output:

```text
Done. Check pipeline.log and warehouse.db
```

The pipeline generates:

- `warehouse.db` — SQLite data warehouse
- `pipeline.log` — execution and validation log

## Data Quality

The pipeline is designed to fail fast when critical data-quality conditions are not satisfied.

Validation includes:

- Null checks
- Uniqueness checks
- Numeric validation
- Date validation
- Required-field validation
- Quantity validation

This helps ensure that only trusted data reaches the warehouse.

## Reproducibility

The `generate_data.py` script creates synthetic retail data, allowing the complete pipeline to be reproduced locally without requiring external datasets or credentials.

## Key Outcome

The completed pipeline successfully:

```text
3,080 raw records
        ↓
2,850 clean records
        ↓
8/8 validation checks passed
        ↓
SQLite star schema
        ↓
8 analytical queries
        ↓
Business insights
```

## Author

**Pujitha Mule**

GitHub: https://github.com/pujitha-mule
