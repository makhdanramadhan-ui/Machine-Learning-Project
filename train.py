"""Training pipeline Telco Churn - fixed version.
- No leakage: scaler/encoder fit hanya di train (via Pipeline)
- Stratified split 80/20 + Stratified 5-Fold GridSearch
- 3 algoritma: LogisticRegression, DecisionTree, RandomForest (tuned)
- Pemilihan best by F1 (imbalanced 73:27, FN lebih mahal)
- Save 1 file pipeline: model_churn.pkl (preprocessing + model)
"""
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, confusion_matrix,
                             classification_report)

CSV = "Telco-Customer-Churn.csv"

# 1. Load
df = pd.read_csv(CSV)
print(f"Raw shape: {df.shape}")
df = df.drop(columns=["customerID"], errors="ignore")

# 2. Cleaning TotalCharges (11 blank ' ') + DROP TotalCharges:
# Total = Monthly x tenure (turunan, korelasi 0.83 dengan tenure).
# Kalau dipakai bareng Monthly, model bingung (multikolinear) dan
# koef Monthly jadi negatif (tidak masuk akal). Jadi dibuang.
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
n_before = len(df)
df = df.dropna().reset_index(drop=True)
df = df.drop(columns=["TotalCharges"])
print(f"Drop {n_before - len(df)} baris kosong -> shape {df.shape}")
print(df["Churn"].value_counts())
print(df["Churn"].value_counts(normalize=True).round(4))

X = df.drop(columns=["Churn"])
y = (df["Churn"] == "Yes").astype(int)

NUM = ["SeniorCitizen", "tenure", "MonthlyCharges"]
CAT = [c for c in X.columns if c not in NUM]
print("NUM:", NUM)
print("CAT:", CAT)

pre = ColumnTransformer([
    ("num", StandardScaler(), NUM),
    ("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Train {len(X_train)} | Test {len(X_test)}")

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

models = {
    "LogisticRegression": (
        LogisticRegression(max_iter=1000),
        {"clf__C": [0.1, 1.0, 10.0], "clf__class_weight": [None, "balanced"]},
    ),
    "DecisionTree": (
        DecisionTreeClassifier(random_state=42),
        {"clf__max_depth": [5, 10, None], "clf__min_samples_split": [2, 5],
         "clf__class_weight": [None, "balanced"]},
    ),
    "RandomForest": (
        RandomForestClassifier(random_state=42, n_jobs=-1),
        {"clf__n_estimators": [200], "clf__max_depth": [12, None],
         "clf__min_samples_split": [2, 5], "clf__class_weight": ["balanced", "balanced_subsample"]},
    ),
}

rows, pipes = [], {}
best = {"f1": -1}
cv_details = []  # Rincian F1 tiap fold buat transparansi di dashboard
for name, (clf, grid) in models.items():
    gs = GridSearchCV(Pipeline([("pre", pre), ("clf", clf)]), grid, cv=cv, scoring="f1", n_jobs=-1)
    gs.fit(X_train, y_train)
    pred = gs.predict(X_test)
    prob = gs.predict_proba(X_test)[:, 1]
    m = {
        "Model": name,
        "BestParams": gs.best_params_,
        "CV_F1": round(gs.best_score_, 4),
        "Accuracy": round(accuracy_score(y_test, pred), 4),
        "Precision": round(precision_score(y_test, pred), 4),
        "Recall": round(recall_score(y_test, pred), 4),
        "F1": round(f1_score(y_test, pred), 4),
        "ROC_AUC": round(roc_auc_score(y_test, prob), 4),
        "TN": int(confusion_matrix(y_test, pred)[0, 0]),
        "FP": int(confusion_matrix(y_test, pred)[0, 1]),
        "FN": int(confusion_matrix(y_test, pred)[1, 0]),
        "TP": int(confusion_matrix(y_test, pred)[1, 1]),
    }
    rows.append(m)
    pipes[name] = gs.best_estimator_
    # Simpan F1 tiap fold dari setting terbaik (bukti tryout 5x)
    bi = gs.best_index_
    for f in range(5):
        cv_details.append({"Model": name, "Fold": f + 1,
                           "F1": round(float(gs.cv_results_[f"split{f}_test_score"][bi]), 4)})
    print(f"\n== {name} ==\n{m}\n{classification_report(y_test, pred)}")
    # Pilih best by CV_F1 (metodologis benar: seleksi di train-CV, bukan test)
    if gs.best_score_ > best["f1"]:
        best = {"f1": float(gs.best_score_), "name": name,
                "pipe": gs.best_estimator_, "row": m}

res = pd.DataFrame(rows).sort_values("F1", ascending=False)
res.to_csv("hasil_perbandingan.csv", index=False)
pd.DataFrame(cv_details).to_csv("cv_detail.csv", index=False)
print("\n=== PERBANDINGAN (sort F1) ===")
print(res.to_string(index=False))

# Save best pipeline SATU file (preprocessing + model)
joblib.dump(best["pipe"], "model_churn.pkl", protocol=4)
with open("model_info.json", "w") as f:
    json.dump({"best_model": best["name"], "metrics": best["row"],
               "n_train": len(X_train), "n_test": len(X_test)}, f, indent=2)
# Simpan daftar kolom mentah untuk validasi app
joblib.dump({"num": NUM, "cat": CAT}, "model_meta.pkl")
print(f"\nBEST: {best['name']} F1={best['f1']:.4f} -> model_churn.pkl (pipeline)")
