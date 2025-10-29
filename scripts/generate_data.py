import os
import uuid
import random
from datetime import datetime,timedelta
import pandas as pd

random.seed(42)

COUNTRIES = ["BR", "US", "GB", "DE", "FR", "CN", "IN", "RU", "ZA", "MX"]
CHANNELS = ["web", "mobile", "pos"]

COUNTRY_RISK = {c: r for c,r in zip(COUNTRIES,[0.4,0.2,0.25,0.2,0.22,0.5,0.35,0.45,0.38,0.33])}

def make_transactions(n=50000, start=None):
    if start is None:
        start = datetime.now() - timedelta(days=5)
    rows = []
    for _ in range(n):
       tx_time = start + timedelta(seconds=random.randint(0, 5*24*3600))
       amount = max(1, round(random.lognormvariate(3, 1), 2))
       is_fraud = 1 if (amount > 3000 and random.random() < 0.15) or (random.random() < 0.01) else 0
       rows.append({
        "transaction_id": str(uuid.uuid4())[:12],
        "customer_id": f"C{random.randint(1, 2000):05d}",
        "amount": amount,
        "country": random.choice(COUNTRIES),
        "channel": random.choice(CHANNELS),
        "timestamp": tx_time,
        "is_fraud": is_fraud
       })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    df = make_transactions(n=20000)
    out = "data/raw/transactions.csv"
    df.to_csv(out, index=False)
    print(f"Gerado: {out} -> {len(df)} linhas")
