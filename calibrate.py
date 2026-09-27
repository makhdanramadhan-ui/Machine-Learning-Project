"""Kalibrasi peluang model churn (Opsi 1: model inti TIDAK diubah).

- Base model (model_churn.pkl) tetap beku: keputusan CHURN/TETAP + semua
  metrik laporan tidak berubah.
- CalibratedClassifierCV(method='sigmoid', cv=5) di-fit HANYA di data train
  (split identik train.py: 80/20, stratify, random_state=42) -> jujur, tidak
  menyentuh test.
- Output: calibrator.pkl + calib_info.json (reliabilitas per band + Brier).
- Rollback: hapus pakai calibrator.pkl / checkout branch backup-sebelum-kalibrasi.
"""
import json
import warnings
import joblib
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import brier_score_loss
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")

CSV = "Telco-Customer-Churn.csv"

df = pd.read_csv(CSV)
df = df.drop(columns=["customerID"], errors="ignore")
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna().reset_index(drop=True).drop(columns=["TotalCharges"])

X = df.drop(columns=["Churn"])
y = (df["Churn"] == "Yes").astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

base = joblib.load("model_churn.pkl")  # template beku, akan di-clone + refit per fold
cal = CalibratedClassifierCV(estimator=base, method="sigmoid", cv=5)
cal.fit(X_train, y_train)

p_base = base.predict_proba(X_test)[:, 1]
p_cal = cal.predict_proba(X_test)[:, 1]

print("Brier (makin kecil makin jujur): base=%.4f cal=%.4f"
      % (brier_score_loss(y_test, p_base), brier_score_loss(y_test, p_cal)))

bands = [(0.00, 0.30, "LOW"), (0.30, 0.60, "MID"), (0.60, 1.01, "HIGH")]
rel = []
for lo, hi, lbl in bands:
    m = (p_cal >= lo) & (p_cal < hi)
    rel.append({"band": lbl, "n": int(m.sum()),
                "mean_pred": round(float(p_cal[m].mean()), 4),
                "empirical": round(float(y_test[m].mean()), 4)})
    print(rel[-1])

joblib.dump(cal, "calibrator.pkl", protocol=4)
with open("calib_info.json", "w") as f:
    json.dump({"method": "sigmoid", "cv": 5, "fit_on": "train-only",
               "base_model": type(base.named_steps["clf"]).__name__,
               "brier_base": round(float(brier_score_loss(y_test, p_base)), 4),
               "brier_cal": round(float(brier_score_loss(y_test, p_cal)), 4),
               "reliability_test": rel,
               "n_train": len(X_train), "n_test": len(X_test)}, f, indent=2)
print("OK -> calibrator.pkl + calib_info.json")
