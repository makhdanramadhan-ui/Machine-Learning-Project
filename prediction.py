"""Kontrak input dan keputusan yang sama untuk form, CSV, dan evaluasi."""
import numpy as np
import pandas as pd

NUMERIC_COLUMNS = ["SeniorCitizen", "tenure", "MonthlyCharges"]
INTERNET_ADDONS = [
    "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
    "StreamingTV", "StreamingMovies",
]


class InputValidationError(ValueError):
    """Masalah input yang bisa ditampilkan tanpa traceback kepada pengguna."""


def input_schema(pipeline):
    """Kategori berasal dari encoder terlatih, bukan tebakan kategori baru."""
    pre = pipeline.named_steps["pre"]
    categorical = next(cols for name, _, cols in pre.transformers_ if name == "cat")
    encoder = pre.named_transformers_["cat"]
    return {
        "columns": list(pipeline.feature_names_in_),
        "categories": {col: list(values) for col, values in zip(categorical, encoder.categories_)},
    }


def validate_input(frame, schema):
    """Validasi seluruh batch; tidak membuang baris bermasalah secara diam-diam."""
    if frame.empty:
        raise InputValidationError("CSV belum berisi data pelanggan.")
    if frame.columns.duplicated().any():
        raise InputValidationError("Nama kolom CSV tidak boleh duplikat.")
    missing = [col for col in schema["columns"] if col not in frame.columns]
    if missing:
        raise InputValidationError("Kolom wajib belum tersedia: " + ", ".join(missing) + ".")

    clean = frame.loc[:, schema["columns"]].copy()
    errors = []

    def report(mask, message):
        positions = np.flatnonzero(pd.Series(mask).fillna(False).to_numpy(dtype=bool))
        if positions.size:
            # Nomor baris data (baris pertama setelah header = 1).
            rows = ", ".join(str(int(i) + 1) for i in positions[:5])
            extra = f", dan {positions.size - 5} baris lainnya" if positions.size > 5 else ""
            errors.append(f"{message} (baris data {rows}{extra}).")

    for col in NUMERIC_COLUMNS:
        values = pd.to_numeric(clean[col], errors="coerce")
        valid = values.notna() & np.isfinite(values)
        report(~valid, f"{col} harus berupa angka terisi dan berhingga")
        clean[col] = values
        if col == "SeniorCitizen":
            report(valid & ~values.isin([0, 1]), "SeniorCitizen hanya boleh 0 atau 1")
        elif col == "tenure":
            report(valid & ((values < 0) | (values > 72) | (values % 1 != 0)),
                   "tenure harus berupa bulan bulat antara 0 dan 72")
        else:
            report(valid & ((values < 0) | (values > 120)),
                   "MonthlyCharges harus antara 0 dan 120 dolar")

    for col, allowed in schema["categories"].items():
        values = clean[col].astype("string").str.strip()
        report(values.isna() | ~values.isin(allowed),
               f"{col} hanya menerima: {', '.join(str(v) for v in allowed)}")
        clean[col] = values

    no_phone = clean["PhoneService"].eq("No")
    report(no_phone & ~clean["MultipleLines"].eq("No phone service"),
           "PhoneService=No mengharuskan MultipleLines=No phone service")
    report(clean["PhoneService"].eq("Yes") & clean["MultipleLines"].eq("No phone service"),
           "PhoneService=Yes tidak boleh memakai MultipleLines=No phone service")
    no_internet = clean["InternetService"].eq("No")
    has_internet = clean["InternetService"].isin(["DSL", "Fiber optic"])
    for col in INTERNET_ADDONS:
        report(no_internet & ~clean[col].eq("No internet service"),
               f"InternetService=No mengharuskan {col}=No internet service")
        report(has_internet & clean[col].eq("No internet service"),
               f"Pelanggan DSL/Fiber optic tidak boleh memakai {col}=No internet service")

    if errors:
        raise InputValidationError("\n".join(errors))
    clean["SeniorCitizen"] = clean["SeniorCitizen"].astype(int)
    clean["tenure"] = clean["tenure"].astype(int)
    return clean


def predict_customers(frame, model, schema, threshold):
    clean = validate_input(frame, schema)
    churn_index = list(model.classes_).index(1)
    probabilities = model.predict_proba(clean)[:, churn_index]
    predictions = (probabilities >= threshold).astype(int)
    return probabilities, predictions


def high_risk_boundary(threshold):
    return min(0.95, max(0.60, threshold + 0.10))


def risk_levels(probabilities, threshold):
    """Risiko rendah selalu di bawah threshold keputusan CHURN."""
    return np.where(np.asarray(probabilities) < threshold, "RENDAH",
                    np.where(np.asarray(probabilities) < high_risk_boundary(threshold),
                             "SEDANG", "TINGGI"))


def input_notes(frame):
    """Kondisi di luar rentang latih tetap bisa diprediksi, tetapi dijelaskan."""
    notes = []
    if pd.to_numeric(frame["tenure"], errors="coerce").eq(0).any():
        notes.append("Ada tenure 0 bulan; data training bersih dimulai dari tenure 1 bulan.")
    if (~pd.to_numeric(frame["MonthlyCharges"], errors="coerce").between(18.25, 118.75)).any():
        notes.append("Ada tagihan di luar rentang dataset latih ($18,25–$118,75).")
    return notes


def example_customers():
    """Contoh konsisten untuk unduhan template dan demonstrasi."""
    return pd.DataFrame([
        {"gender": "Male", "SeniorCitizen": 0, "Partner": "No", "Dependents": "No",
         "tenure": 2, "PhoneService": "Yes", "MultipleLines": "No",
         "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "No",
         "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "Yes",
         "StreamingMovies": "Yes", "Contract": "Month-to-month", "PaperlessBilling": "Yes",
         "PaymentMethod": "Electronic check", "MonthlyCharges": 95.0},
        {"gender": "Female", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "Yes",
         "tenure": 60, "PhoneService": "Yes", "MultipleLines": "Yes",
         "InternetService": "DSL", "OnlineSecurity": "Yes", "OnlineBackup": "Yes",
         "DeviceProtection": "Yes", "TechSupport": "Yes", "StreamingTV": "No",
         "StreamingMovies": "No", "Contract": "Two year", "PaperlessBilling": "No",
         "PaymentMethod": "Bank transfer (automatic)", "MonthlyCharges": 65.0},
    ])
