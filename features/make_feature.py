import pandas as pd
from etl.utils import ENGINE

COUNTRY_RISK = {"BR":0.4,"US":0.2,"GB":0.25,"DE":0.2,"FR":0.22,"CN":0.5,"IN":0.35,"RU":0.45,"ZA":0.38,"MX":0.33}

def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # garantir datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # features básicas
    df["hour"] = df["timestamp"].dt.hour
    df["is_high_amount"] = (df["amount"] > 2000).astype(int)
    df["country_risk"] = df["country"].map(COUNTRY_RISK).fillna(0.3)

    # ordena por cliente e tempo e zera índice para alinhar tudo
    df = df.sort_values(["customer_id", "timestamp"]).reset_index(drop=True)

    # contagem de transações na última 1h por cliente (time-based rolling)
    rolling = (
        df.groupby("customer_id")
          .rolling("3600s", on="timestamp")["transaction_id"]
          .count()
          .reset_index(level=0, drop=True)
    )
    df["rolling_1h_tx"] = rolling.astype("int16").to_numpy()

    # z-score por cliente
    df["amount_mean_cust"] = df.groupby("customer_id")["amount"].transform("mean")
    df["amount_std_cust"]  = df.groupby("customer_id")["amount"].transform("std")
    df["amount_std_cust"]  = df["amount_std_cust"].fillna(1.0).replace(0, 1.0)
    df["amount_zscore"]    = (df["amount"] - df["amount_mean_cust"]) / df["amount_std_cust"]

    keep = [
        "transaction_id","customer_id","amount","hour","is_high_amount",
        "country_risk","rolling_1h_tx","amount_zscore","is_fraud"
    ]
    return df[keep]

if __name__ == "__main__":
    raw = pd.read_sql("SELECT * FROM raw_transactions", ENGINE)
    feats = compute_features(raw)
    feats.to_sql("features_transactions", ENGINE, if_exists="replace", index=False)
    print("✅ Features gravadas em features_transactions")

