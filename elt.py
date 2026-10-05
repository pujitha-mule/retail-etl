import pandas as pd
import sqlite3
import logging

logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def extract():
    logging.info("EXTRACT: reading 3 sources")
    df1 = pd.read_csv("data/source1.csv")
    df2 = pd.read_csv("data/source2.csv")
    df3 = pd.read_json("data/source3.json")
    df = pd.concat([df1, df2, df3], ignore_index=True)
    logging.info(f"Extracted {len(df)} raw records")
    return df

def transform(df):
    logging.info("TRANSFORM: cleaning")
    before = len(df)

    df = df.drop_duplicates(subset=["order_id"])
    df = df.dropna(subset=["order_id", "customer_id", "amount"])
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])
    df["category"] = df["category"].astype(str).str.strip().str.title()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df[df["amount"] > 0]

    after = len(df)
    logging.info(f"Cleaned: {before} -> {after} records ({before - after} removed)")
    return df

def validate(df):
    logging.info("VALIDATE: running checks")
    checks = {
        "no null order_id": df["order_id"].notna().all(),
        "order_id unique": df["order_id"].is_unique,
        "no null customer_id": df["customer_id"].notna().all(),
        "amount positive": (df["amount"] > 0).all(),
        "valid dates": df["order_date"].notna().all(),
        "no null product": df["product"].notna().all(),
        "category present": df["category"].notna().all(),
        "quantity >= 1": (df["quantity"] >= 1).all(),
    }
    for name, ok in checks.items():
        status = "PASS" if ok else "FAIL"
        logging.info(f"  {name}: {status}")
        assert ok, f"Validation failed: {name}"
    logging.info(f"All {len(checks)} checks passed")
    return df

def load(df):
    logging.info("LOAD: writing to SQLite star schema")
    conn = sqlite3.connect("warehouse.db")

    # dim_date
    dim_date = df[["order_date"]].drop_duplicates().copy()
    dim_date["date_key"] = dim_date["order_date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["year"] = dim_date["order_date"].dt.year
    dim_date["month"] = dim_date["order_date"].dt.month
    dim_date["day"] = dim_date["order_date"].dt.day
    dim_date.to_sql("dim_date", conn, if_exists="replace", index=False)

    # dim_product
    dim_product = df[["product", "category"]].drop_duplicates().reset_index(drop=True)
    dim_product["product_key"] = dim_product.index + 1
    dim_product.to_sql("dim_product", conn, if_exists="replace", index=False)

    # dim_customer
    dim_customer = df[["customer_id"]].drop_duplicates().reset_index(drop=True)
    dim_customer["customer_key"] = dim_customer.index + 1
    dim_customer.to_sql("dim_customer", conn, if_exists="replace", index=False)

    # fact_sales
    fact = df.merge(dim_product, on=["product", "category"], how="left") \
             .merge(dim_customer, on="customer_id", how="left")
    fact["date_key"] = fact["order_date"].dt.strftime("%Y%m%d").astype(int)
    fact_sales = fact[["order_id", "product_key", "customer_key", "date_key",
                       "quantity", "price", "amount"]]
    fact_sales.to_sql("fact_sales", conn, if_exists="replace", index=False)

    conn.close()
    logging.info("Loaded: fact_sales + 3 dims")

def run_queries():
    logging.info("QUERIES: generating insights")
    conn = sqlite3.connect("warehouse.db")

    queries = {
        "Top 5 products by revenue": """
            SELECT p.product, ROUND(SUM(f.amount), 2) AS revenue
            FROM fact_sales f JOIN dim_product p ON f.product_key = p.product_key
            GROUP BY p.product ORDER BY revenue DESC LIMIT 5
        """,
        "Revenue by category": """
            SELECT p.category, ROUND(SUM(f.amount), 2) AS revenue
            FROM fact_sales f JOIN dim_product p ON f.product_key = p.product_key
            GROUP BY p.category ORDER BY revenue DESC
        """,
        "Monthly revenue trend": """
            SELECT d.year, d.month, ROUND(SUM(f.amount), 2) AS revenue
            FROM fact_sales f JOIN dim_date d ON f.date_key = d.date_key
            GROUP BY d.year, d.month ORDER BY d.year, d.month
        """,
        "Top 5 customers by spend": """
            SELECT c.customer_id, ROUND(SUM(f.amount), 2) AS total_spend
            FROM fact_sales f JOIN dim_customer c ON f.customer_key = c.customer_key
            GROUP BY c.customer_id ORDER BY total_spend DESC LIMIT 5
        """,
        "Avg order value": """
            SELECT ROUND(AVG(amount), 2) AS avg_order_value FROM fact_sales
        """,
        "Orders per month": """
            SELECT d.year, d.month, COUNT(*) AS orders
            FROM fact_sales f JOIN dim_date d ON f.date_key = d.date_key
            GROUP BY d.year, d.month ORDER BY d.year, d.month
        """,
        "Revenue per product": """
            SELECT p.product, ROUND(SUM(f.amount), 2) AS revenue
            FROM fact_sales f JOIN dim_product p ON f.product_key = p.product_key
            GROUP BY p.product ORDER BY revenue DESC
        """,
        "Total quantity sold": """
            SELECT SUM(quantity) AS total_units FROM fact_sales
        """,
    }

    for name, q in queries.items():
        result = pd.read_sql(q, conn)
        logging.info(f"\n{name}:\n{result.to_string(index=False)}")

    conn.close()
    logging.info("All 8 queries complete")

if __name__ == "__main__":
    logging.info("=" * 50)
    logging.info("PIPELINE START")
    df = extract()
    df = transform(df)
    df = validate(df)
    load(df)
    run_queries()
    logging.info("PIPELINE END")
    print("\nDone. Check pipeline.log and warehouse.db")