import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)
n = 3000

products = ["Laptop", "Phone", "Tablet", "Headphones",
            "Keyboard", "Mouse", "Monitor", "Cable"]
categories = {
    "Laptop": "Electronics", "Phone": "Electronics", "Tablet": "Electronics",
    "Headphones": "Audio", "Keyboard": "Accessories", "Mouse": "Accessories",
    "Monitor": "Electronics", "Cable": "Accessories"
}
customers = [f"C{1000+i}" for i in range(300)]

rows = []
start = datetime(2025, 1, 1)
for i in range(n):
    pid = random.choice(products)
    qty = random.randint(1, 5)
    price = round(random.uniform(10, 1500), 2)
    rows.append({
        "order_id": f"ORD{10000+i}",
        "customer_id": random.choice(customers),
        "product": pid,
        "category": categories[pid],
        "quantity": qty,
        "price": price,
        "order_date": (start + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
        "amount": round(qty * price, 2)
    })

df = pd.DataFrame(rows)

# Inject messiness so cleaning is real
df.loc[df.sample(100).index, "customer_id"] = None
df.loc[df.sample(50).index, "order_date"] = "INVALID"
df = pd.concat([df, df.sample(80)], ignore_index=True)

# Split into 2 CSV + 1 JSON
df.iloc[:1200].to_csv("data/source1.csv", index=False)
df.iloc[1200:2400].to_csv("data/source2.csv", index=False)
df.iloc[2400:].to_json("data/source3.json", orient="records", indent=2)

print(f"Generated {len(df)} rows across 3 sources")