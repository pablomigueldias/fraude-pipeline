import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split #type: ignore
from sklearn.metrics import ( #type: ignore
    classification_report,
    roc_auc_score,
    precision_recall_curve,
    average_precision_score,
    confusion_matrix
)
from sklearn.ensemble import RandomForestClassifier #type: ignore
from joblib import dump #type: ignore
from etl.utils import ENGINE

FEATURES = ["amount","hour","is_high_amount","country_risk","rolling_1h_tx","amount_zscore"]
TARGET = "is_fraud"

if __name__ == "__main__":
    
    df = pd.read_sql("SELECT * FROM features_transactions", ENGINE)
    X = df[FEATURES]
    y = df[TARGET].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=400,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced_subsample",
        max_depth=None,
        min_samples_leaf=2
    )
    clf.fit(X_train, y_train)

    prob = clf.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, prob)
    ap  = average_precision_score(y_test, prob)  
    print(f"AUC-ROC: {auc:.4f}")
    print(f"AUC-PR (AP): {ap:.4f}")

    precision, recall, thresholds = precision_recall_curve(y_test, prob)
    f1s = 2 * (precision * recall) / (precision + recall + 1e-12)
    best_idx = np.nanargmax(f1s)
    best_thr = thresholds[max(best_idx-1, 0)] if best_idx < len(thresholds) else 0.5

    print(f"Threshold escolhido (max F1): {best_thr:.4f}")

    pred = (prob >= best_thr).astype(int)

    print(classification_report(y_test, pred, digits=4))
    cm = confusion_matrix(y_test, pred)
    print("Confusion matrix:\n", cm)


    dump({"model": clf, "features": FEATURES, "threshold": float(best_thr)}, "model/model.joblib")
    print("✅ Modelo salvo em model/model.joblib (com threshold recomendado)")
