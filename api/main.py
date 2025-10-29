import uvicorn #type: ignore
from fastapi import FastAPI #type: ignore
from joblib import load #type: ignore
from model.inference_schema import TxBatch
import numpy as np


app = FastAPI(title="Fraud Detector API")
artifacts = load("model/model.joblib")
model = artifacts["model"]
FEATURES = artifacts["features"]


@app.get("/")
async def root():
    return {"status": "ok", "features": FEATURES}


@app.post("/predict")
async def predict(batch: TxBatch):
    X = np.array([[
    it.amount, it.hour, it.is_high_amount, it.country_risk, it.rolling_1h_tx, it.amount_zscore
    ] for it in batch.items])
    prob = model.predict_proba(X)[:,1].tolist()
    pred = [1 if p>=0.5 else 0 for p in prob]
    return {"proba": prob, "pred": pred}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)