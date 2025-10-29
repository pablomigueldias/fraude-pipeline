
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) 

import numpy as np
import pandas as pd
import streamlit as st #type: ignore
from joblib import load #type: ignore
from sqlalchemy import text #type: ignore
from etl.utils import ENGINE


st.set_page_config(
    page_title="Fraude - Monitor",
    page_icon="🕵️",
    layout="wide"
)

@st.cache_resource(show_spinner=False)
def load_artifacts():
    art = load("model/model.joblib")
    model = art["model"]
    features = art["features"]
    thr = float(art.get("threshold", 0.5))
    return model, features, thr

@st.cache_data(ttl=120, show_spinner=False)
def load_data():

    df = pd.read_sql("SELECT * FROM features_transactions", ENGINE)
    if "amount" in df:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    if "hour" in df:
        df["hour"] = pd.to_numeric(df["hour"], errors="coerce").astype("Int64")

    if "is_fraud" in df:
        df["is_fraud"] = pd.to_numeric(df["is_fraud"], errors="coerce").fillna(0).astype(int)

    if not {"country","channel","timestamp"}.issubset(df.columns):
        try:
            raw = pd.read_sql(
                "SELECT transaction_id, country, channel, timestamp FROM raw_transactions",
                ENGINE
            )
            df = df.merge(raw, on="transaction_id", how="left", suffixes=("","_raw"))
        except Exception:
            pass
    if "timestamp" in df:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df

def apply_filters(df: pd.DataFrame):
    left, right = st.sidebar.columns(2)

    if "timestamp" in df:
        min_dt = pd.to_datetime(df["timestamp"].min()) if not df["timestamp"].isna().all() else None
        max_dt = pd.to_datetime(df["timestamp"].max()) if not df["timestamp"].isna().all() else None
    else:
        min_dt = max_dt = None

    st.sidebar.markdown("### Filtros")
    if min_dt and max_dt:
        dstart, dend = st.sidebar.date_input(
            "Período",
            value=(min_dt.date(), max_dt.date()),
            min_value=min_dt.date(),
            max_value=max_dt.date()
        )
        mask_dt = (df["timestamp"].dt.date >= dstart) & (df["timestamp"].dt.date <= dend)
        df = df[mask_dt]

    if "country" in df:
        countries = sorted([c for c in df["country"].dropna().unique()])
        sel_countries = st.sidebar.multiselect("País", countries, default=countries[:5] if countries else [])
        if sel_countries:
            df = df[df["country"].isin(sel_countries)]

    if "channel" in df:
        channels = sorted([c for c in df["channel"].dropna().unique()])
        sel_channels = st.sidebar.multiselect("Canal", channels, default=channels)
        if sel_channels:
            df = df[df["channel"].isin(sel_channels)]

    if "amount" in df:
        min_amount = float(np.nanmin(df["amount"])) if len(df) else 0.0
        max_amount = float(np.nanmax(df["amount"])) if len(df) else 10000.0
        val_min = st.sidebar.slider("Valor mínimo (amount)", min_amount, max_amount, min_amount)
        df = df[df["amount"] >= val_min]

    return df

def predict(model, features, df_feats: pd.DataFrame):
    missing = [c for c in features if c not in df_feats.columns]
    for m in missing:
        df_feats[m] = 0
    X = df_feats[features].astype(float).to_numpy()
    proba = model.predict_proba(X)[:, 1]
    return proba


st.title("Monitor de Fraudes")
st.caption("Pipeline de engenharia de dados + IA • Demo")

model, FEATURES, THRESH_SAVED = load_artifacts()
df = load_data()

if df.empty:
    st.warning("Nenhum dado encontrado em `features_transactions`.")
    st.stop()

df_f = apply_filters(df)

st.sidebar.markdown("### Threshold de Alerta")
thr_mode = st.sidebar.selectbox("Modo", ["Usar do modelo", "Definir manualmente", "Top-K% alertas"])
if thr_mode == "Usar do modelo":
    threshold = THRESH_SAVED
elif thr_mode == "Definir manualmente":
    threshold = st.sidebar.slider("Threshold (0-1)", 0.0, 1.0, float(THRESH_SAVED), 0.01)
else:
    k = st.sidebar.slider("Percentual de alertas (K%)", 0.1, 10.0, 1.0, 0.1)
    threshold = None  


with st.spinner("Calculando probabilidades..."):
    df_f = df_f.copy()
    df_f["proba"] = predict(model, FEATURES, df_f)

    if thr_mode == "Top-K% alertas":
        thr_q = np.quantile(df_f["proba"], 1 - (k / 100.0)) if len(df_f) else 1.0
        df_f["alert"] = (df_f["proba"] >= thr_q).astype(int)
        threshold_display = thr_q
    else:
        df_f["alert"] = (df_f["proba"] >= threshold).astype(int)
        threshold_display = threshold


col1, col2, col3, col4 = st.columns(4)
col1.metric("Transações (filtro)", f"{len(df_f):,}".replace(",", "."))
if "is_fraud" in df_f:
    col2.metric("Fraudes (rotuladas)", int(df_f["is_fraud"].sum()))
else:
    col2.metric("Fraudes (rotuladas)", "—")
col3.metric("Alertas", int(df_f["alert"].sum()))
col4.metric("Threshold atual", f"{threshold_display:.3f}")

st.divider()

st.subheader("Top suspeitas")
topn = st.slider("Quantidade a listar", 10, 500, 50, 10)
cols_show = ["transaction_id", "customer_id", "amount", "country", "channel", "proba", "alert"]
cols_exist = [c for c in cols_show if c in df_f.columns]
st.dataframe(
    df_f.sort_values("proba", ascending=False)[cols_exist].head(topn),
    use_container_width=True,
    hide_index=True
)

st.subheader("Distribuição dos scores (proba)")
st.caption("Ajuda a escolher threshold/percentual de alertas.")
hist_vals, bins = np.histogram(df_f["proba"], bins=30, range=(0,1))
hist_df = pd.DataFrame({"bin_center": (bins[:-1] + bins[1:]) / 2, "freq": hist_vals})
st.bar_chart(hist_df.set_index("bin_center"))

st.subheader("Importância das features")
if hasattr(model, "feature_importances_"):
    fi = pd.DataFrame({"feature": FEATURES, "importance": model.feature_importances_})
    fi = fi.sort_values("importance", ascending=False).head(15)
    st.bar_chart(fi.set_index("feature"))
else:
    st.info("O modelo atual não expõe `feature_importances_` (tente RandomForest/GradientBoosting).")


if "is_fraud" in df_f:
    st.subheader("Métricas no recorte filtrado (se rótulo existir)")
    from sklearn.metrics import classification_report, average_precision_score, roc_auc_score #type: ignore
    y_true = df_f["is_fraud"].astype(int)
    y_prob = df_f["proba"].astype(float)
    y_pred = df_f["alert"].astype(int)

    ap = average_precision_score(y_true, y_prob) if y_true.sum() > 0 else 0.0
    auc = roc_auc_score(y_true, y_prob) if y_true.nunique() > 1 else 0.5
    st.write(f"**AUC-PR (AP):** {ap:.4f} • **AUC-ROC:** {auc:.4f}")
    st.text(classification_report(y_true, y_pred, digits=4))
else:
    st.info("Sem rótulo `is_fraud` neste recorte — mostrando apenas scores/alertas.")


