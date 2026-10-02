"""Split acuan agar kalibrasi memakai data training yang sama dengan training model."""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

BASE = Path(__file__).resolve().parent


def load_training_split():
    df = pd.read_csv(BASE / "Telco-Customer-Churn.csv")
    df = df.drop(columns=["customerID"], errors="ignore")
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    # Pertahankan cohort evaluasi awal (7032 pelanggan dengan catatan lengkap).
    # TotalCharges tidak dibutuhkan aplikasi; bukan berarti nilainya persis Monthly x tenure.
    df = df.dropna().reset_index(drop=True).drop(columns=["TotalCharges"])
    X = df.drop(columns=["Churn"])
    y = (df["Churn"] == "Yes").astype(int)
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
