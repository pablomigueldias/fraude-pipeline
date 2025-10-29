from prefect import flow, task #type: ignore
import pandas as pd
from sqlalchemy import text #type: ignore
from utils import ENGINE

@task
def extract_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["timestamp"])


@task
def load_raw(df: pd.DataFrame):
    df.to_sql("raw_transactions", ENGINE, if_exists="append", index=False)


@flow(name="etl_raw")
def etl_raw_flow(csv_path: str = "data/raw/transactions.csv"):
    df = extract_csv(csv_path)
    load_raw(df)


if __name__ == "__main__":
    etl_raw_flow()