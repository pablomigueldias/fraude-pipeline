from pydantic import BaseModel #type: ignore
from typing import List


class TxInput(BaseModel):
    amount: float
    hour: int
    is_high_amount: int
    country_risk: float
    rolling_1h_tx: int
    amount_zscore: float


class TxBatch(BaseModel):
    items: List[TxInput]