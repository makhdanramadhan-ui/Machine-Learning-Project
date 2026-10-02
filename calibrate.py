"""Kalibrasi train-only + threshold F1 dari out-of-fold training, lalu evaluasi test.

Jalankan setelah train.py. Test tidak dipakai untuk memilih threshold.
Model inti tetap tersedia untuk perbandingan; aplikasi memakai model terkalibrasi.
"""
import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, brier_score_loss,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from prediction import high_risk_boundary
from training_data import load_training_split

BASE = Path(__file__).resolve().parent


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


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


def calibrate():
    X_train, X_test, y_train, y_test = load_training_split()
    base = joblib.load(BASE / "model_churn.pkl")
    inner_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=43)
    outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cal = CalibratedClassifierCV(estimator=base, method="sigmoid", cv=inner_cv)

    # Setiap outer fold kalibrasi/fit hanya pada training fold-nya.
    # Hyperparameter model inti sudah dipilih di train-CV; ini bukan nested-CV
    # untuk estimasi generalisasi. Holdout test tetap menjadi evaluasi akhir.
    oof = cross_val_predict(cal, X_train, y_train, cv=outer_cv,
                           method="predict_proba", n_jobs=-1)[:, 1]
    thresholds = np.round(np.arange(0.10, 0.601, 0.01), 2)
    scores = [f1_score(y_train, oof >= t, zero_division=0) for t in thresholds]
    # Jika sama, pilih ambang lebih rendah (lebih sensitif untuk churn).
    threshold = float(thresholds[int(np.argmax(scores))])
    pd.DataFrame({"Threshold": thresholds, "OOF_F1": scores}).to_csv(
        BASE / "threshold_selection.csv", index=False)

    cal.fit(X_train, y_train)
    joblib.dump(cal, BASE / "calibrator.pkl", protocol=4)
    p_base = base.predict_proba(X_test)[:, 1]
    p_cal = cal.predict_proba(X_test)[:, 1]
    high = high_risk_boundary(threshold)
    bands = [(0.0, threshold, "LOW"), (threshold, high, "MID"), (high, 1.01, "HIGH")]
    reliability = []
    for lo, hi, label in bands:
        mask = (p_cal >= lo) & (p_cal < hi)
        reliability.append({
            "band": label, "n": int(mask.sum()),
            "mean_pred": round(float(p_cal[mask].mean()), 4) if mask.any() else None,
            "empirical": round(float(y_test[mask].mean()), 4) if mask.any() else None,
        })
    clf_name = type(base.named_steps["clf"]).__name__
    metadata = {
        "method": "sigmoid", "cv": 5, "fit_on": "train-only", "base_model": clf_name,
        "brier_base": round(float(brier_score_loss(y_test, p_base)), 4),
        "brier_cal": round(float(brier_score_loss(y_test, p_cal)), 4),
        "reliability_test": reliability, "n_train": len(X_train), "n_test": len(X_test),
    }
    (BASE / "calib_info.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    deployment = {
        "base_model": clf_name, "probability_model": "sigmoid calibrated ensemble (5-fold)",
        "threshold": threshold, "threshold_selection": "max F1 on 5-fold OOF train probabilities",
        "threshold_selection_data": "train-only", "oof_tuning_f1": round(float(max(scores)), 4),
        "risk_high_boundary": high, "n_train": len(X_train), "n_test": len(X_test),
        "n_features": X_train.shape[1], "sklearn_version": sklearn.__version__,
        "metrics": classification_metrics(y_test, p_cal, threshold),
        "metrics_at_0_5": classification_metrics(y_test, p_cal, 0.5),
        "model_sha256": file_hash(BASE / "model_churn.pkl"),
        "calibrator_sha256": file_hash(BASE / "calibrator.pkl"),
    }
    (BASE / "deployment_info.json").write_text(json.dumps(deployment, indent=2), encoding="utf-8")
    print(f"Threshold OOF-train: {threshold:.2f} | OOF tuning F1: {max(scores):.4f}")
    print("Evaluasi model aplikasi:", deployment["metrics"])
    return deployment


if __name__ == "__main__":
    calibrate()
