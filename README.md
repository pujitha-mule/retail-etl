# Retail Sales ETL Pipeline

A simple ETL pipeline that combines retail sales data from 3 sources (2 CSV + 1 JSON)
into a cleaned dataset, validates it, and loads it into a SQLite star schema.

## Stack
Python, Pandas, SQL, SQLite

## Pipeline
1. **Extract** — reads 3 sources (2 CSV + 1 JSON)
2. **Transform** — handles missing values, duplicates, date/category standardization
3. **Validate** — 8 checks (null keys, duplicate IDs, positive amounts, valid dates, etc.)
4. **Load** — SQLite star schema (1 fact + 3 dims)
5. **Query** — 8 business insights via SQL

## Run
```bash
pip install pandas
python generate_data.py
python etl.py