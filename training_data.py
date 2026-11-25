from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, brier_score_loss,
)
from sklearn.model_selection import train_test_split

BASE = Path(__file__).resolve().parent


def load_training_split():
    df = pd.read_csv(BASE / "Telco-Customer-Churn.csv")
    df = df.drop(columns=["customerID"], errors="ignore")
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df = df.dropna().reset_index(drop=True).drop(columns=["TotalCharges"])
    X = df.drop(columns=["Churn"])
    y = (df["Churn"] == "Yes").astype(int)
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


def classification_metrics(y, probabilities, threshold):
    pred = (probabilities >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return {
        "Accuracy": round(float(accuracy_score(y, pred)), 4),
        "Precision": round(float(precision_score(y, pred, zero_division=0)), 4),
        "Recall": round(float(recall_score(y, pred, zero_division=0)), 4),
        "F1": round(float(f1_score(y, pred, zero_division=0)), 4),
        "ROC_AUC": round(float(roc_auc_score(y, probabilities)), 4),
        "Brier": round(float(brier_score_loss(y, probabilities)), 4),
        "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp),
    }
