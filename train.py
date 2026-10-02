"""Tiga model, seleksi CV-F1 train-only, evaluasi holdout, lalu model aplikasi."""
import json

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

from calibrate import calibrate, classification_metrics
from training_data import BASE, load_training_split


def train():
    X_train, X_test, y_train, y_test = load_training_split()
    num = ["SeniorCitizen", "tenure", "MonthlyCharges"]
    cat = [col for col in X_train.columns if col not in num]
    pre = ColumnTransformer([
        ("num", StandardScaler(), num),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat),
    ])
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
             "clf__min_samples_split": [2, 5],
             "clf__class_weight": ["balanced", "balanced_subsample"]},
        ),
    }
    rows, cv_details = [], []
    best = None
    for name, (clf, grid) in models.items():
        gs = GridSearchCV(Pipeline([("pre", pre), ("clf", clf)]), grid, cv=cv,
                          scoring="f1", n_jobs=-1, return_train_score=True)
        gs.fit(X_train, y_train)
        bi = gs.best_index_
        probabilities = gs.predict_proba(X_test)[:, 1]
        row = {
            "Model": name, "BestParams": gs.best_params_,
            "CV_F1": round(float(gs.best_score_), 4),
            "CV_F1_STD": round(float(gs.cv_results_["std_test_score"][bi]), 4),
            "CV_TRAIN_F1": round(float(gs.cv_results_["mean_train_score"][bi]), 4),
            "Train_F1": round(float(f1_score(y_train, gs.predict(X_train))), 4),
            **classification_metrics(y_test, probabilities, 0.5),
        }
        rows.append(row)
        for fold in range(5):
            cv_details.append({"Model": name, "Fold": fold + 1,
                               "F1": round(float(gs.cv_results_[f"split{fold}_test_score"][bi]), 4)})
        # Seleksi model hanya memakai validation score pada training set.
        if best is None or gs.best_score_ > best["score"]:
            best = {"score": float(gs.best_score_), "name": name,
                    "pipe": gs.best_estimator_, "row": row}
        print(name, row)

    pd.DataFrame(rows).sort_values("CV_F1", ascending=False).to_csv(
        BASE / "hasil_perbandingan.csv", index=False)
    pd.DataFrame(cv_details).to_csv(BASE / "cv_detail.csv", index=False)
    joblib.dump(best["pipe"], BASE / "model_churn.pkl", protocol=4)
    joblib.dump({"num": num, "cat": cat}, BASE / "model_meta.pkl")
    info = {"best_model": best["name"], "selection_metric": "CV_F1", "metrics": best["row"],
            "n_train": len(X_train), "n_test": len(X_test)}
    (BASE / "model_info.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    print(f"Model inti: {best['name']} | CV-F1: {best['score']:.4f}")
    calibrate()


if __name__ == "__main__":
    train()
