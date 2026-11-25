from pathlib import Path
import csv
import hashlib
import io
import joblib
import json
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

import ui
from prediction import (
    InputValidationError, example_customers, input_schema, input_notes,
    predict_customers, risk_levels, high_risk_boundary, validate_input,
)
from training_data import load_training_split

BASE = Path(__file__).parent

st.set_page_config(
    page_title="Prediksi Customer Churn - Telco",
    page_icon=BASE / "assets" / "brand-mark.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.session_state.setdefault("tema", "Terang")

with st.container(key="topbar"):
    head_left, head_right = st.columns([7, 2], gap="medium", vertical_alignment="center")
    with head_left:
        header_slot = st.empty()
    with head_right:
        st.segmented_control("Tema", ["Terang", "Gelap"], key="tema",
                             label_visibility="collapsed", width="stretch")

TEMA = st.session_state.get("tema") or "Terang"
TOK = ui.THEMES[TEMA]
SERIES = (["#1E3A8A", "#1D4ED8", "#60A5FA", "#A9C6FA"] if TEMA == "Terang"
          else ["#DBEAFE", "#93C5FD", "#60A5FA", "#2563EB"])
st.markdown(ui.font_face_css(), unsafe_allow_html=True)
st.markdown(ui.build_css(TEMA), unsafe_allow_html=True)


@st.cache_resource
def load_models(model_stamp, calibration_stamp, metadata_stamp):
    with open(BASE / "deployment_info.json", encoding="utf-8") as f:
        deployment = json.load(f)
    for filename, key in [("model_churn.pkl", "model_sha256"),
                          ("calibrator.pkl", "calibrator_sha256")]:
        digest = hashlib.sha256((BASE / filename).read_bytes()).hexdigest()
        if digest != deployment[key]:
            raise ValueError(f"{filename} tidak cocok dengan metadata evaluasi. "
                             "Jalankan notebook 02_Training_Model dan 03_Kalibrasi_dan_Threshold.")
    base = joblib.load(BASE / "model_churn.pkl")
    calibrated = joblib.load(BASE / "calibrator.pkl")
    return base, calibrated, deployment


try:
    stamps = [(BASE / name).stat().st_mtime_ns for name in
              ["model_churn.pkl", "calibrator.pkl", "deployment_info.json"]]
    pipe, CAL, DEPLOY = load_models(*stamps)
    with open(BASE / "model_info.json", encoding="utf-8") as f:
        INFO = json.load(f)
    with open(BASE / "calib_info.json", encoding="utf-8") as f:
        CALINFO = json.load(f)
    CMP = pd.read_csv(BASE / "hasil_perbandingan.csv")
    CVDET = pd.read_csv(BASE / "cv_detail.csv")
except (OSError, ValueError, KeyError) as exc:
    st.error(f"Model belum bisa dimuat: {exc}")
    st.info("Jalankan notebook `02_Training_Model.ipynb` dan `03_Kalibrasi_dan_Threshold.ipynb`, "
            "lalu unggah model dan file hasil evaluasinya bersama-sama.")
    st.stop()

SCHEMA = input_schema(pipe)
THRESHOLD = float(DEPLOY["threshold"])
HIGH_BOUNDARY = high_risk_boundary(THRESHOLD)


@st.cache_data
def load_charge_reference(dataset_stamp):
    train_data, _, _, _ = load_training_split()
    reference = {}
    for service, group in train_data.groupby("InternetService"):
        charges = group["MonthlyCharges"]
        reference[service] = {
            "min": float(charges.min()), "max": float(charges.max()),
            "median": float(charges.median()),
            "q1": float(charges.quantile(0.25)), "q3": float(charges.quantile(0.75)),
        }
    return reference


BEST = INFO.get("best_model", "LogisticRegression") if INFO else "LogisticRegression"
MODEL_NAMES = {"LogisticRegression": "Logistic Regression", "DecisionTree": "Decision Tree",
               "RandomForest": "Random Forest"}
BEST_LABEL = MODEL_NAMES.get(BEST, BEST)
header_slot.markdown(
    ui.header_bar(
        "Prediksi Customer Churn Telco",
        "Estimasi risiko churn pelanggan dari 18 fitur layanan dan tagihan menggunakan model "
        f"{BEST_LABEL} terkalibrasi (threshold {ui.fmt_num(THRESHOLD)})."),
    unsafe_allow_html=True,
)
BASE_MET = INFO.get("metrics", {})
MET = DEPLOY["metrics"]
CVF1 = BASE_MET.get("CV_F1", "-")
ACC = MET.get("Accuracy", "-")
AUC = MET.get("ROC_AUC", "-")
REC = MET.get("Recall", "-")
N_TEST = DEPLOY["n_test"]
N_DATA = DEPLOY["n_train"] + N_TEST

FIELD_LABELS = {
    "gender": "Jenis kelamin", "SeniorCitizen": "Lansia", "Partner": "Pasangan",
    "Dependents": "Tanggungan", "tenure": "Lama berlangganan", "PhoneService": "Layanan telepon",
    "MultipleLines": "Jalur telepon ganda", "InternetService": "Layanan internet",
    "OnlineSecurity": "Keamanan online", "OnlineBackup": "Backup online",
    "DeviceProtection": "Perlindungan perangkat", "TechSupport": "Bantuan teknis",
    "StreamingTV": "Streaming TV", "StreamingMovies": "Streaming film", "Contract": "Kontrak",
    "PaperlessBilling": "Tagihan tanpa kertas", "PaymentMethod": "Metode pembayaran",
    "MonthlyCharges": "Tagihan bulanan",
}

FIGURE_TITLES = {
    "target_distribution": "Sebaran target churn",
    "numeric_histograms_train": "Histogram fitur angka",
    "numeric_boxplots_train": "Boxplot fitur angka",
    "correlation_train": "Korelasi fitur angka",
    "categorical_churn_train": "Persentase churn per kategori",
    "categorical_distribution_train": "Sebaran fitur kategori",
    "scatter_train": "Lama berlangganan dan tagihan",
}


def count_text(value):
    return ui.count(value)


def dollar_text(value):
    return r"\$" + f"{value:.2f}".replace(".", ",")


def usd_html(value):
    return "&#36;" + f"{value:.2f}".replace(".", ",")


def option_label(value):
    labels = {
        "Female": "Perempuan", "Male": "Laki-laki", "Yes": "Ya", "No": "Tidak",
        "No phone service": "Tidak memakai telepon", "No internet service": "Tidak memakai internet",
        "Fiber optic": "Fiber optik", "Month-to-month": "Bulanan", "One year": "Satu tahun",
        "Two year": "Dua tahun", "Electronic check": "Cek elektronik",
        "Mailed check": "Cek melalui pos", "Bank transfer (automatic)": "Transfer bank otomatis",
        "Credit card (automatic)": "Kartu kredit otomatis",
    }
    return labels.get(value, value)


def feature_parts(name):
    kind, rest = name.split("__", 1)
    if kind == "num":
        return rest, None
    field, value = rest.split("_", 1)
    return field, value


def feature_label(name, row=None):
    field, value = feature_parts(name)
    title = FIELD_LABELS.get(field, field)
    if value is not None:
        return f"{title}: {option_label(value)}"
    if row is None:
        return title
    current = row.iloc[0][field]
    if field == "tenure":
        return f"{title}: {int(current)} bulan"
    if field == "MonthlyCharges":
        return f"{title}: {usd_html(float(current))}"
    return f"{title}: {'Ya' if int(current) == 1 else 'Tidak'}"


def customer_drivers(row):
    clf = pipe.named_steps["clf"]
    if not hasattr(clf, "coef_"):
        return None
    pre = pipe.named_steps["pre"]
    clean = validate_input(row, SCHEMA)
    encoded = pre.transform(clean)
    encoded = encoded.toarray() if hasattr(encoded, "toarray") else np.asarray(encoded)
    values = encoded[0] * clf.coef_[0]
    names = list(pre.get_feature_names_out())
    return clean, names, values


def style_chart(chart):
    return ui.style_chart(chart, TOK)


def show_chart(chart):
    st.altair_chart(style_chart(chart), theme=None, width="stretch")


def risk_chart(out):
    order = ["RENDAH", "SEDANG", "TINGGI"]
    counts = out["Risiko"].value_counts().reindex(order).fillna(0).astype(int)
    data = pd.DataFrame({"Risiko": order, "Pelanggan": counts.values})
    base = alt.Chart(data).encode(
        y=alt.Y("Risiko:N", sort=order, title=None, axis=alt.Axis(labelFontWeight=600)),
        x=alt.X("Pelanggan:Q", title="Pelanggan", axis=alt.Axis(tickMinStep=1)),
        color=alt.Color("Risiko:N", legend=None,
                        scale=alt.Scale(domain=order, range=[TOK["safe"], TOK["mid"], TOK["high"]])),
        tooltip=["Risiko:N", "Pelanggan:Q"])
    bars = base.mark_bar(cornerRadiusEnd=5, size=26)
    labels = base.mark_text(align="left", dx=6, color=TOK["ink"], fontWeight=600).encode(
        text="Pelanggan:Q")
    return (bars + labels).properties(height=170)


def histogram_chart(out):
    data = out[["Prob_Churn"]]
    bars = alt.Chart(data).mark_bar(color=TOK["accent"], cornerRadiusTopLeft=3,
                                    cornerRadiusTopRight=3, opacity=.9).encode(
        x=alt.X("Prob_Churn:Q", bin=alt.Bin(step=5, extent=[0, 100]),
                title="Probabilitas churn (%)"),
        y=alt.Y("count():Q", title="Pelanggan", axis=alt.Axis(tickMinStep=1)),
        tooltip=[alt.Tooltip("Prob_Churn:Q", bin=alt.Bin(step=5, extent=[0, 100]),
                             title="Rentang (%)"), alt.Tooltip("count():Q", title="Pelanggan")])
    rule_data = pd.DataFrame({"x": [THRESHOLD * 100], "label": [f"Threshold {THRESHOLD:.0%}"]})
    rule = alt.Chart(rule_data).mark_rule(color=TOK["high"], strokeWidth=2,
                                          strokeDash=[5, 4]).encode(x="x:Q")
    text = alt.Chart(rule_data).mark_text(align="left", dx=6, dy=-4, baseline="bottom",
                                          color=TOK["high"], fontWeight=600, fontSize=11).encode(
        x="x:Q", text="label:N", y=alt.value(12))
    return (bars + rule + text).properties(height=170)


def reliability_chart():
    labels = {"LOW": "Rendah", "MID": "Sedang", "HIGH": "Tinggi"}
    rows = []
    for item in CALINFO["reliability_test"]:
        band = labels.get(item["band"], item["band"])
        rows.append({"Kategori": band, "Ukuran": "Rata-rata probabilitas",
                     "Nilai": item["mean_pred"], "Pelanggan": item["n"]})
        rows.append({"Kategori": band, "Ukuran": "Proporsi churn aktual",
                     "Nilai": item["empirical"], "Pelanggan": item["n"]})
    data = pd.DataFrame(rows)
    return alt.Chart(data).mark_bar(cornerRadiusEnd=4).encode(
        x=alt.X("Kategori:N", sort=["Rendah", "Sedang", "Tinggi"], title="Kategori risiko",
                axis=alt.Axis(labelAngle=0)),
        xOffset=alt.XOffset("Ukuran:N"),
        y=alt.Y("Nilai:Q", title="Skala 0–1", scale=alt.Scale(domain=[0, 1])),
        color=alt.Color("Ukuran:N", scale=alt.Scale(
            domain=["Rata-rata probabilitas", "Proporsi churn aktual"],
            range=[TOK["accent"], TOK["neutral"]])),
        tooltip=["Kategori:N", "Ukuran:N", alt.Tooltip("Nilai:Q", format=".3f"),
                 "Pelanggan:Q"]).properties(height=240)


def metric_compare_chart():
    metrics = ["Accuracy", "Precision", "Recall", "F1"]
    data = CMP[["Model"] + metrics].copy()
    data["Model"] = data["Model"].replace(MODEL_NAMES)
    long = data.melt(id_vars="Model", var_name="Metrik", value_name="Skor")
    model_order = data["Model"].tolist()
    return alt.Chart(long).mark_bar(cornerRadiusEnd=3).encode(
        x=alt.X("Model:N", sort=model_order, title=None,
                axis=alt.Axis(labelAngle=0, labelFontWeight=600)),
        xOffset=alt.XOffset("Metrik:N", sort=metrics),
        y=alt.Y("Skor:Q", scale=alt.Scale(domain=[0, 1]), title="Skor"),
        color=alt.Color("Metrik:N", scale=alt.Scale(domain=metrics, range=SERIES)),
        tooltip=["Model:N", "Metrik:N", alt.Tooltip("Skor:Q", format=".4f")]).properties(height=260)


def cv_chart():
    data = CVDET.copy()
    data["Model"] = data["Model"].replace(MODEL_NAMES)
    names = [MODEL_NAMES.get(m, m) for m in CVDET["Model"].unique()]
    colors = [TOK["accent"] if name == BEST_LABEL else
              (TOK["ink2"] if i % 2 else TOK["neutral"]) for i, name in enumerate(names)]
    return alt.Chart(data).mark_line(point=alt.OverlayMarkDef(size=60, filled=True),
                                     strokeWidth=2.5).encode(
        x=alt.X("Fold:O", title="Sesi validasi", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("F1:Q", title="F1", scale=alt.Scale(zero=False)),
        color=alt.Color("Model:N", scale=alt.Scale(domain=names, range=colors)),
        strokeDash=alt.StrokeDash("Model:N", legend=None, scale=alt.Scale(
            domain=names, range=[[1, 0] if name == BEST_LABEL else [5, 4] for name in names])),
        tooltip=["Model:N", "Fold:O", alt.Tooltip("F1:Q", format=".4f")]).properties(height=260)


def coefficient_chart(top):
    data = top.copy()
    data["Arah"] = np.where(data["Bobot"] > 0, "Naikkan risiko churn", "Turunkan risiko churn")
    order = data.sort_values("Bobot")["Fitur"].tolist()
    bars = alt.Chart(data).mark_bar(cornerRadius=3, size=15).encode(
        y=alt.Y("Fitur:N", sort=order, title=None, axis=alt.Axis(labelLimit=220)),
        x=alt.X("Bobot:Q", title="Koefisien model (log-odds)"),
        color=alt.Color("Arah:N", scale=alt.Scale(
            domain=["Naikkan risiko churn", "Turunkan risiko churn"],
            range=[TOK["high"], TOK["safe"]])),
        tooltip=["Fitur:N", alt.Tooltip("Bobot:Q", format="+.3f"), "Arah:N"])
    zero = alt.Chart(pd.DataFrame({"x": [0]})).mark_rule(color=TOK["ink2"]).encode(x="x:Q")
    return (bars + zero).properties(height=420)


charge_default = load_charge_reference((BASE / "Telco-Customer-Churn.csv").stat().st_mtime_ns)

st.markdown(
    ui.model_ribbon(
        BEST_LABEL,
        [
            ("ROC-AUC", ui.fmt_num(AUC, 4), "Kemampuan membedakan pelanggan churn dan bertahan"),
            ("Recall Churn", ui.fmt_num(REC, 4),
             f"{count_text(MET['TP'])} dari {count_text(MET['TP'] + MET['FN'])} pelanggan churn "
             "di data uji terdeteksi"),
            ("F1-Score", ui.fmt_num(MET.get("F1", 0), 4),
             f"Keseimbangan precision ({ui.fmt_num(MET.get('Precision', 0), 4)}) dan recall"),
            ("Threshold", ui.fmt_num(THRESHOLD), f"CHURN jika probabilitas ≥ {THRESHOLD:.0%}"),
        ],
        [
            ("Data latih", count_text(DEPLOY["n_train"])),
            ("Data uji", count_text(N_TEST)),
            ("Fitur", f"{DEPLOY['n_features']}"),
            ("Kalibrasi", "Sigmoid 5-Fold"),
            ("Sklearn", DEPLOY["sklearn_version"]),
            ("SHA-256", DEPLOY["model_sha256"][:12] + "…"),
        ],
    ),
    unsafe_allow_html=True,
)

with st.expander("Tentang model dan cara membaca hasil", expanded=False):
    c_a, c_b = st.columns([1, 2])
    with c_a:
        st.markdown(f"**Model yang dipakai: {BEST_LABEL}**")
        st.caption("Dipilih berdasarkan rata-rata F1 tertinggi pada validasi silang lima fold "
                   "data latih (CV-F1). ROC-AUC, Recall, F1, dan metrik threshold dihitung "
                   f"setelah kalibrasi sigmoid pada {count_text(N_TEST)} data uji.")
        if MET:
            st.json(MET)
    with c_b:
        st.caption(f"Model memakai {DEPLOY['n_features']} informasi pelanggan. Angka dan kategori "
                   "diproses otomatis sebelum diprediksi.")
        st.write(f"**Aturan keputusan:** CHURN jika probabilitas ≥ {THRESHOLD:.0%}; "
                 "TETAP jika di bawah threshold tersebut.")
        st.caption("Threshold dipilih dari validasi data latih, bukan dari data uji. Label CHURN "
                   "menunjukkan risiko yang melewati threshold, bukan kepastian.")

tab1, tab2, tab3, tab4 = st.tabs([
    "Prediksi Single", "Prediksi Batch (CSV)", "Dashboard & Model", "EDA & Dokumentasi",
])

with tab1:
    left, right = st.columns([1.38, 1.0], gap="large")
    with left:
        with st.container(key="panel_form"):
            st.markdown(ui.section("Data Pelanggan", "user",
                                   "Isi data pelanggan di bawah, lalu klik Prediksi. Pilihan layanan "
                                   "tambahan menyesuaikan layanan telepon dan internet yang digunakan."),
                        unsafe_allow_html=True)
            st.markdown(ui.sub_head("Profil & Lama Berlangganan", "user", first=True),
                        unsafe_allow_html=True)
            f1, f2, f3 = st.columns(3)
            with f1:
                gender = st.selectbox("Jenis Kelamin", ["Female", "Male"], format_func=option_label)
            with f2:
                SeniorCitizen = st.selectbox("Lansia (SeniorCitizen)", ["No", "Ya"], index=0,
                                             format_func=option_label)
            with f3:
                Partner = st.selectbox("Punya Pasangan", ["Yes", "No"], index=1,
                                       format_func=option_label)
            f4, f5, _ = st.columns(3)
            with f4:
                Dependents = st.selectbox("Punya Tanggungan", ["Yes", "No"], index=1,
                                          format_func=option_label)
            with f5:
                tenure = st.number_input("Lama Berlangganan (bulan)", 0, 72, 12,
                                         help="Tenure: jumlah bulan pelanggan sudah berlangganan.")

            st.markdown(ui.sub_head("Layanan Telepon & Internet", "wifi"),
                        unsafe_allow_html=True)
            s1, s2, s3 = st.columns(3)
            with s1:
                PhoneService = st.selectbox("Layanan Telepon", ["Yes", "No"], format_func=option_label)
            _ml_lock = (PhoneService == "No")
            _ml_opts = ["No phone service"] if _ml_lock else ["Yes", "No"]
            with s2:
                MultipleLines = st.selectbox(
                    "Lebih dari Satu Jalur Telepon", _ml_opts, disabled=_ml_lock,
                    format_func=option_label,
                    help="MultipleLines: apakah pelanggan memakai lebih dari satu jalur telepon.")
            with s3:
                InternetService = st.selectbox("Layanan Internet", ["Fiber optic", "DSL", "No"],
                                               format_func=option_label)
            _lock = (InternetService == "No")
            _opts = ["No internet service"] if _lock else ["Yes", "No"]
            a1, a2, a3 = st.columns(3)
            with a1:
                OnlineSecurity = st.selectbox("Keamanan Online", _opts, disabled=_lock,
                                              format_func=option_label)
            with a2:
                OnlineBackup = st.selectbox("Backup Online", _opts, disabled=_lock,
                                            format_func=option_label)
            with a3:
                DeviceProtection = st.selectbox("Perlindungan Perangkat", _opts, disabled=_lock,
                                                format_func=option_label)
            a4, a5, a6 = st.columns(3)
            with a4:
                TechSupport = st.selectbox("Bantuan Teknis", _opts, disabled=_lock,
                                           format_func=option_label)
            with a5:
                StreamingTV = st.selectbox("Streaming TV", _opts, disabled=_lock,
                                           format_func=option_label)
            with a6:
                StreamingMovies = st.selectbox("Streaming Film", _opts, disabled=_lock,
                                               format_func=option_label)

            st.markdown(ui.sub_head("Kontrak & Tagihan", "receipt"),
                        unsafe_allow_html=True)
            k1, k2, k3 = st.columns(3)
            with k1:
                Contract = st.selectbox("Kontrak", ["Month-to-month", "One year", "Two year"],
                                        format_func=option_label)
            with k2:
                PaperlessBilling = st.selectbox("Tagihan Tanpa Kertas", ["Yes", "No"],
                                                format_func=option_label)
            with k3:
                PaymentMethod = st.selectbox("Metode Pembayaran", [
                    "Electronic check", "Mailed check", "Bank transfer (automatic)",
                    "Credit card (automatic)"], format_func=option_label)
            m1, m2 = st.columns([1, 1.6], gap="medium")
            charge_reference = charge_default[InternetService]
            service_label = "tanpa internet" if InternetService == "No" else option_label(InternetService)
            with m1:
                MonthlyCharges = st.number_input(
                    "Tagihan Bulanan ($)", 0.0, 120.0, 70.0, step=1.0, format="%.2f",
                    help="Batas input $0–$120; rentang data latih $18,25–$118,75. "
                         "Isi tagihan aktual.")
            with m2:
                st.markdown(f"**Acuan tagihan {service_label}**")
                st.caption(f"Rentang umum: {dollar_text(charge_reference['q1'])}–"
                           f"{dollar_text(charge_reference['q3'])}/bulan (50% data training). "
                           f"Median: {dollar_text(charge_reference['median'])}.")
                st.caption(f"Rentang yang tercatat: {dollar_text(charge_reference['min'])}–"
                           f"{dollar_text(charge_reference['max'])}. Ini total tagihan termasuk "
                           "telepon dan layanan tambahan yang dipakai, bukan tarif internet saja.")
            out_of_range = (MonthlyCharges < charge_reference["min"]
                            or MonthlyCharges > charge_reference["max"])
            if out_of_range:
                direction = "lebih rendah" if MonthlyCharges < charge_reference["min"] else "lebih tinggi"
                st.warning(f"Tagihan {dollar_text(MonthlyCharges)} {direction} dari rentang {service_label} "
                           "pada data training. Periksa lagi nominal dan layanan yang dipilih. "
                           "Prediksi tetap bisa dijalankan; acuan ini bukan daftar harga resmi.")

    row = pd.DataFrame([{
        "gender": gender, "SeniorCitizen": 1 if SeniorCitizen == "Ya" else 0,
        "Partner": Partner, "Dependents": Dependents, "tenure": tenure,
        "PhoneService": PhoneService, "MultipleLines": MultipleLines,
        "InternetService": InternetService, "OnlineSecurity": OnlineSecurity,
        "OnlineBackup": OnlineBackup, "DeviceProtection": DeviceProtection,
        "TechSupport": TechSupport, "StreamingTV": StreamingTV,
        "StreamingMovies": StreamingMovies, "Contract": Contract,
        "PaperlessBilling": PaperlessBilling, "PaymentMethod": PaymentMethod,
        "MonthlyCharges": MonthlyCharges,
    }])
    fingerprint = json.dumps([row.to_json(orient="records"), THRESHOLD, DEPLOY["calibrator_sha256"]])

    if MonthlyCharges < charge_reference["min"] or MonthlyCharges > charge_reference["max"]:
        charge_status = "Di luar rentang yang tercatat pada data latih untuk layanan ini."
    elif MonthlyCharges < charge_reference["q1"]:
        charge_status = "Di bawah rentang umum (Q1–Q3) untuk layanan ini."
    elif MonthlyCharges > charge_reference["q3"]:
        charge_status = "Di atas rentang umum (Q1–Q3) untuk layanan ini."
    else:
        charge_status = "Dalam rentang umum (Q1–Q3) untuk layanan ini."

    with right:
        st.markdown(
            ui.snapshot(
                option_label(Contract),
                "Tanpa internet" if InternetService == "No" else option_label(InternetService),
                f"{int(tenure)} bulan", MonthlyCharges, charge_reference,
                usd_html(MonthlyCharges), charge_status, out_of_range,
                usd_html(charge_reference["min"]), usd_html(charge_reference["max"]),
                usd_html(charge_reference["median"])),
            unsafe_allow_html=True)
        predict = st.button("Prediksi", type="primary", width="stretch")

        if predict:
            try:
                probabilities, predictions = predict_customers(row, CAL, SCHEMA, THRESHOLD)
                st.session_state["single_result"] = {
                    "input": fingerprint, "prob": float(probabilities[0]), "pred": int(predictions[0]),
                }
            except InputValidationError as exc:
                st.session_state.pop("single_result", None)
                st.error(str(exc))

        result = st.session_state.get("single_result")
        if result and result["input"] != fingerprint:
            st.info("Input telah berubah. Klik Prediksi untuk memperbarui hasil.")
        if not result:
            st.markdown(ui.ready_state(THRESHOLD, HIGH_BOUNDARY), unsafe_allow_html=True)
        if result and result["input"] == fingerprint:
            prob, pred = result["prob"], result["pred"]
            for note in input_notes(row):
                st.info(note)

            level = risk_levels([prob], THRESHOLD)[0]
            st.markdown(ui.verdict(prob, THRESHOLD, HIGH_BOUNDARY, level, pred),
                        unsafe_allow_html=True)
            st.markdown(ui.calibrated_scale(prob, THRESHOLD, HIGH_BOUNDARY), unsafe_allow_html=True)
            st.caption("TETAP berarti pelanggan diprediksi tidak churn. Detail pengujian "
                       "kalibrasi ada di Dashboard & Model.")

            drivers = customer_drivers(row)
            field_effect = {}
            if drivers is not None:
                clean_row, names, values = drivers
                for name, value in zip(names, values):
                    field = feature_parts(name)[0]
                    field_effect[field] = field_effect.get(field, 0.0) + float(value)
                ranked = sorted(((feature_label(n, clean_row), float(v)) for n, v in zip(names, values)
                                 if abs(v) > 1e-9), key=lambda item: -abs(item[1]))
                ups = [item for item in ranked if item[1] > 0][:4]
                downs = [item for item in ranked if item[1] < 0][:4]
                peak = max([abs(v) for _, v in ups + downs] or [1.0])
                st.markdown(
                    ui.contributions(
                        ups, downs, peak,
                        "Pengaruh lokal pada log-odds model dasar sebelum kalibrasi: nilai fitur "
                        "yang sudah diproses × koefisien. Fitur angka dibandingkan dengan rata-rata "
                        "data latih. Ini arah dan besar relatif pengaruh, bukan persentase risiko "
                        "dan bukan bukti sebab-akibat."),
                    unsafe_allow_html=True)

            st.markdown(ui.section("Saran untuk Mempertahankan Pelanggan", "target",
                                   "Diurutkan dari faktor yang paling mendorong risiko pelanggan ini. "
                                   "Efektivitasnya perlu diuji, karena model belum mengukur dampak "
                                   "penawaran terhadap churn."),
                        unsafe_allow_html=True)
            recs = []
            if Contract == "Month-to-month":
                recs.append((["Contract"], "Kontrak",
                             "Pertimbangkan penawaran kontrak satu atau dua tahun dengan diskon."))
            if InternetService == "Fiber optic" and MonthlyCharges > 75:
                recs.append((["MonthlyCharges", "InternetService"], "Tagihan",
                             "Tinjau paket fiber yang digunakan dan tawarkan paket yang lebih sesuai."))
            if PaymentMethod == "Electronic check":
                recs.append((["PaymentMethod"], "Pembayaran",
                             "Tawarkan pembayaran otomatis melalui transfer atau kartu."))
            if TechSupport in ("No", "No internet service") and InternetService != "No":
                recs.append((["TechSupport"], "Bantuan teknis",
                             "Pertimbangkan masa coba layanan bantuan teknis."))
            if tenure < 6:
                recs.append((["tenure"], "Pelanggan baru",
                             "Bantu pelanggan memahami layanan dan tanyakan pengalamannya "
                             "setelah bulan pertama."))
            if not recs:
                recs.append(([], "Layanan",
                             "Jaga kualitas layanan dan pertimbangkan penghargaan untuk pelanggan lama."))
            recs.sort(key=lambda item: -sum(field_effect.get(field, 0.0) for field in item[0]))
            st.markdown(ui.rec_list(ui.recommendation(i, label, text)
                                    for i, (_, label, text) in enumerate(recs, start=1)),
                        unsafe_allow_html=True)

with tab2:
    with st.container(key="panel_batch_input"):
        st.markdown(ui.section("Unggah CSV untuk Prediksi Massal", "upload",
                               "Gunakan template atau CSV dengan kolom yang sama. Kolom "
                               "`customerID`, `Churn`, dan `TotalCharges` boleh disertakan, "
                               "tetapi tidak dipakai untuk prediksi."),
                    unsafe_allow_html=True)
        b_left, b_right = st.columns([1, 1.5], gap="large", vertical_alignment="bottom")
        with b_left:
            st.download_button("Unduh template CSV", example_customers().to_csv(index=False).encode("utf-8"),
                               "template_pelanggan.csv", "text/csv", width="stretch")
        with b_right:
            f = st.file_uploader("Pilih file CSV", type="csv")
    out = None
    if f is not None:
        try:
            text = f.getvalue().decode("utf-8-sig")
            header = next(csv.reader(io.StringIO(text)), [])
            header = [col.strip() for col in header]
            if len(header) != len(set(header)):
                raise InputValidationError("Nama kolom CSV tidak boleh duplikat.")
            df = pd.read_csv(io.StringIO(text))
            df.columns = df.columns.str.strip()
            probs, preds = predict_customers(df, CAL, SCHEMA, THRESHOLD)
            for note in input_notes(df):
                st.info(note)
            extra = [col for col in df.columns if col not in SCHEMA["columns"]]
            if extra:
                st.caption("Kolom tidak digunakan oleh model: " + ", ".join(extra))
            out = df.copy()
            out["Prob_Churn"] = (probs * 100).round(2)
            out["Prediksi"] = ["CHURN" if p == 1 else "TETAP" for p in preds]
            out["Risiko"] = risk_levels(probs, THRESHOLD)
            out["Threshold_Churn"] = THRESHOLD
        except (InputValidationError, pd.errors.EmptyDataError, pd.errors.ParserError,
                UnicodeDecodeError, ValueError) as exc:
            st.error("CSV belum bisa diproses. Periksa bagian berikut, lalu unggah ulang:")
            st.text(str(exc))

    if out is not None:
        churn_n = int((out["Prediksi"] == "CHURN").sum())
        high_n = int((out["Risiko"] == "TINGGI").sum())
        rate = float((out["Prediksi"] == "CHURN").mean() * 100)

        st.markdown(ui.summary_strip([
            ("Total baris", count_text(len(out)), "", "Pelanggan pada file"),
            ("Prediksi churn", count_text(churn_n), "hot", f"Probabilitas ≥ {THRESHOLD:.0%}"),
            ("Persentase churn", ui.fmt_num(rate) + "%", "hot", "Dari seluruh baris"),
            ("Risiko tinggi", count_text(high_n), "hot", f"Probabilitas ≥ {HIGH_BOUNDARY:.0%}"),
        ]), unsafe_allow_html=True)

        with st.container(key="panel_batch_charts"):
            ch1, ch2 = st.columns(2, gap="large")
            with ch1:
                st.markdown(ui.chart_head("Segmen risiko"), unsafe_allow_html=True)
                show_chart(risk_chart(out))
            with ch2:
                st.markdown(ui.chart_head("Sebaran probabilitas churn",
                                          f"Garis putus-putus menandai threshold {THRESHOLD:.0%}."),
                            unsafe_allow_html=True)
                show_chart(histogram_chart(out))

        with st.container(key="panel_batch_table"):
            st.markdown(ui.section("Hasil Prediksi", "grid"), unsafe_allow_html=True)
            st.caption(f"Threshold: {THRESHOLD:.0%}. Kolom Prob_Churn berisi probabilitas dalam persen. "
                       f"Menampilkan {min(20, len(out))} dari {count_text(len(out))} pelanggan; "
                       "unduhan memuat semua hasil.")
            st.dataframe(
                out.head(20), width="stretch", hide_index=True,
                column_config={
                    "Prob_Churn": st.column_config.ProgressColumn(
                        "Prob_Churn", min_value=0, max_value=100, format="%.1f%%"),
                    "Threshold_Churn": st.column_config.NumberColumn(
                        "Threshold_Churn", format="%.2f"),
                })
            st.download_button("Unduh hasil (CSV)",
                               out.to_csv(index=False).encode(), "hasil_prediksi.csv", "text/csv",
                               width="stretch")

with tab3:
    with st.container(key="panel_app_model"):
        st.markdown(ui.section("Hasil Pengujian Model Aplikasi", "chart",
                               f"{BEST_LABEL} dengan kalibrasi sigmoid, diuji pada "
                               f"{count_text(N_TEST)} pelanggan yang tidak digunakan untuk "
                               "melatih model."),
                    unsafe_allow_html=True)
        d_left, d_right = st.columns([1.15, 1], gap="large")
        with d_left:
            st.dataframe(pd.DataFrame([
                {"Konfigurasi": f"Aplikasi (threshold {ui.fmt_num(THRESHOLD)})", **MET},
                {"Konfigurasi": "Pembanding (threshold 0,50)", **DEPLOY["metrics_at_0_5"]},
            ]), width="stretch", hide_index=True)
            st.caption(f"Dari {MET['TP'] + MET['FN']} pelanggan yang benar-benar churn, "
                       f"{MET['TP']} berhasil terdeteksi dan {MET['FN']} terlewat. "
                       f"{MET['FP']} pelanggan yang tidak churn juga ditandai CHURN. "
                       "Menurunkan threshold membantu mendeteksi lebih banyak churn, tetapi bisa menambah "
                       "prediksi yang keliru.")
        with d_right:
            st.markdown(ui.chart_head(f"Confusion matrix (threshold {ui.fmt_num(THRESHOLD)})",
                                      f"{count_text(N_TEST)} pelanggan data uji."),
                        unsafe_allow_html=True)
            st.markdown(ui.confusion_matrix(MET, N_TEST), unsafe_allow_html=True)
        with st.expander(f"Mengapa threshold {THRESHOLD:.0%}? Detail kalibrasi", expanded=False):
            st.write(f"Threshold dicoba dari 0,10 sampai 0,60 dengan selisih 0,01. "
                     f"Threshold {THRESHOLD:.2f} memberi F1 tertinggi pada validasi data training. "
                     "Artinya, model memberi label CHURN ketika probabilitas mencapai threshold ini, "
                     "meskipun masih di bawah 50%.")
            st.caption("Prediksi validasi dibuat dengan lima fold: setiap bagian diprediksi oleh "
                       "model yang dilatih pada bagian lainnya, dengan kalibrasi di dalam proses "
                       f"itu. F1 untuk memilih threshold: {DEPLOY['oof_tuning_f1']:.4f}. Skor ini dipakai "
                       "untuk memilih pengaturan, bukan hasil pengujian akhir.")
            st.write(f"Kalibrasi sigmoid menyesuaikan probabilitas model. Pada data testing, Brier "
                     f"score turun dari {CALINFO['brier_base']:.4f} menjadi {CALINFO['brier_cal']:.4f}. "
                     "Semakin kecil Brier, semakin kecil kesalahan probabilitasnya.")
            r_left, r_right = st.columns([1.2, 1], gap="large")
            with r_left:
                st.markdown(ui.chart_head("Reliabilitas kalibrasi",
                                          "Batang yang sama tinggi berarti probabilitas sesuai kenyataan."),
                            unsafe_allow_html=True)
                show_chart(reliability_chart())
            with r_right:
                st.dataframe(pd.DataFrame(CALINFO["reliability_test"]).rename(columns={
                    "band": "Kategori risiko", "n": "Pelanggan", "mean_pred": "Rata-rata probabilitas",
                    "empirical": "Proporsi churn aktual",
                }).replace({"Kategori risiko": {"LOW": "Rendah", "MID": "Sedang", "HIGH": "Tinggi"}}),
                             width="stretch", hide_index=True)

    with st.container(key="panel_compare"):
        st.markdown(ui.section("Perbandingan Tiga Model", "layers",
                               "Ketiga model ini diuji sebelum kalibrasi, dengan threshold 50%. Model "
                               "dipilih berdasarkan CV-F1 data training, bukan akurasi testing "
                               "tertinggi. Hasil setelah kalibrasi ada pada tabel aplikasi di atas."),
                    unsafe_allow_html=True)
        with st.expander("Cara membaca metrik"):
            st.markdown(
                "| Metrik | Rumus | Arti |\n"
                "|---|---|---|\n"
                "| TP | TP | Diprediksi churn dan memang churn |\n"
                "| TN | TN | Prediksi tidak churn (0), aktual tidak churn (0) |\n"
                "| FP | FP | Prediksi churn (1), aktual tidak churn (0): alarm keliru |\n"
                "| FN | FN | Prediksi tidak churn (0), aktual churn (1): churn terlewat |\n"
                "| Accuracy | (TP+TN)/total | Proporsi seluruh prediksi yang benar |\n"
                "| Precision | TP/(TP+FP) | Dari yang diprediksi churn, berapa yang benar-benar churn |\n"
                "| Recall | TP/(TP+FN) | Dari seluruh pelanggan churn, berapa yang terdeteksi |\n"
                "| F1 | 2×P×R/(P+R) | Rata-rata harmonik precision dan recall |\n"
                "| ROC-AUC | luas kurva ROC | 0,5 = acak, 1,0 = sempurna |")
            st.caption("F1 merangkum precision dan recall. Keduanya perlu diperhatikan karena "
                       "pelanggan churn lebih sedikit daripada pelanggan yang tidak churn. "
                       "Akurasi tinggi saja belum berarti model berhasil mendeteksi churn.")
            st.caption("**CV-F1** adalah rata-rata F1 dari validasi silang lima fold. Data training "
                       "dibagi menjadi lima bagian: model dilatih pada empat bagian lalu divalidasi "
                       "pada satu bagian, bergantian lima kali. Skor ini dipakai untuk memilih model.")
            st.caption("**ROC-AUC** menunjukkan kemampuan model membedakan churn dan tidak churn "
                       "pada berbagai threshold. Kurva ROC membandingkan recall dengan false positive "
                       "rate `FP/(FP+TN)`. Nilai 0,5 setara urutan acak.")

        if CMP is not None:
            st.markdown(ui.model_strip([
                (MODEL_NAMES.get(r["Model"], r["Model"]), r["Model"] == BEST, [
                    ("CV-F1", ui.fmt_num(r["CV_F1"], 4)), ("F1 uji", ui.fmt_num(r["F1"], 4)),
                    ("Recall", ui.fmt_num(r["Recall"], 4)), ("ROC-AUC", ui.fmt_num(r["ROC_AUC"], 4)),
                ]) for _, r in CMP.iterrows()
            ]), unsafe_allow_html=True)

            g1, g2 = st.columns(2, gap="large")
            with g1:
                st.markdown(ui.chart_head("Metrik uji per model", "Accuracy, Precision, Recall, dan F1 pada data uji."),
                            unsafe_allow_html=True)
                show_chart(metric_compare_chart())
            with g2:
                if CVDET is not None:
                    st.markdown(ui.chart_head("Stabilitas F1 lima fold",
                                              "Garis yang datar menandakan hasil validasi lebih stabil."),
                                unsafe_allow_html=True)
                    show_chart(cv_chart())

            _cmp_show = CMP.copy()
            _cmp_show["Model"] = _cmp_show["Model"].replace(MODEL_NAMES)
            _cmp_show.index = _cmp_show.index + 1
            st.dataframe(_cmp_show, width="stretch")

            cm_left, cm_right = st.columns([1, 1.3], gap="large")
            with cm_left:
                cm_model = st.selectbox("Pilih model untuk melihat confusion matrix",
                                        CMP["Model"].tolist(),
                                        format_func=lambda name: MODEL_NAMES.get(name, name))
            b = CMP[CMP["Model"] == cm_model].iloc[0]
            with cm_right:
                st.markdown(f"**Confusion matrix: {MODEL_NAMES.get(cm_model, cm_model)} "
                            f"({count_text(N_TEST)} pelanggan testing)**")
                st.markdown(ui.confusion_matrix(b, N_TEST), unsafe_allow_html=True)

            selected = CMP[CMP["Model"] == BEST].iloc[0]
            lowest_cv = CMP.loc[CMP["CV_F1"].idxmin()]
            top_recall = CMP.loc[CMP["Recall"].idxmax()]
            top_accuracy = CMP.loc[CMP["Accuracy"].idxmax()]
            st.info(
                f"**Mengapa {BEST_LABEL}?** Model ini mendapat CV-F1 tertinggi "
                f"({selected['CV_F1']:.4f}) pada data training, sedangkan "
                f"{MODEL_NAMES.get(lowest_cv['Model'], lowest_cv['Model'])} mencatat CV-F1 terendah "
                f"({lowest_cv['CV_F1']:.4f}) karena pohon tunggal lebih sensitif terhadap pembagian fold. "
                f"Saat diuji sebelum kalibrasi, "
                f"{MODEL_NAMES.get(top_recall['Model'], top_recall['Model'])} memiliki recall tertinggi "
                f"({top_recall['Recall']:.2%}), sedangkan "
                f"{MODEL_NAMES.get(top_accuracy['Model'], top_accuracy['Model'])} memiliki akurasi "
                f"tertinggi ({top_accuracy['Accuracy']:.2%}). Hasil testing ini dilaporkan tanpa "
                "mengganti model yang sudah dipilih.")
            if {"Train_F1", "CV_TRAIN_F1", "CV_F1_STD"}.issubset(CMP.columns):
                st.markdown("**Perbandingan F1 saat training, validasi, dan testing**")
                st.dataframe(CMP[["Model", "Train_F1", "CV_TRAIN_F1", "CV_F1", "CV_F1_STD", "F1"]].replace(
                    {"Model": MODEL_NAMES}),
                             width="stretch", hide_index=True)
                largest_gap = CMP.loc[(CMP["Train_F1"] - CMP["F1"]).idxmax()]
                st.caption(f"{MODEL_NAMES.get(largest_gap['Model'], largest_gap['Model'])} memiliki selisih "
                           f"F1 training dan testing terbesar: {largest_gap['Train_F1']:.4f} vs "
                           f"{largest_gap['F1']:.4f}. Model jauh lebih baik pada data yang sudah "
                           "dipelajari daripada data baru. Ini indikasi overfitting, dan terlihat "
                           "juga pada skor validasinya.")
            if CVDET is not None:
                st.markdown("**F1 pada setiap sesi validasi**")
                st.caption("Validasi dilakukan lima kali pada bagian data training yang berbeda. "
                           "Data testing 20% disimpan terpisah dan tidak masuk ke lima fold ini.")
                _cv_show = CVDET.rename(columns={"Fold": "Session"}).replace({"Model": MODEL_NAMES})
                _cv_pivot = _cv_show.pivot(index="Session", columns="Model", values="F1").reset_index()
                _cv_pivot = _cv_pivot.rename(
                    columns={c: f"Nilai F1 {c}" for c in _cv_pivot.columns if c != "Session"})
                _fold_map = {
                    1: ("2, 3, 4, 5", "1"),
                    2: ("1, 3, 4, 5", "2"),
                    3: ("1, 2, 4, 5", "3"),
                    4: ("1, 2, 3, 5", "4"),
                    5: ("1, 2, 3, 4", "5"),
                }
                _cv_pivot["Train Fold"] = _cv_pivot["Session"].map(lambda s: _fold_map.get(s, ("-", "-"))[0])
                _cv_pivot["Validation Fold"] = _cv_pivot["Session"].map(lambda s: _fold_map.get(s, ("-", "-"))[1])
                _f1_cols = [c for c in _cv_pivot.columns if c.startswith("Nilai F1")]
                _cv_pivot = _cv_pivot[["Session", "Train Fold", "Validation Fold"] + _f1_cols]
                st.dataframe(_cv_pivot, width="stretch", hide_index=True)

    with st.container(key="panel_features"):
        st.markdown(ui.section("Hubungan Fitur dengan Prediksi", "linechart",
                               "Grafik ini menampilkan koefisien model sebelum kalibrasi. Batang "
                               "merah ke kanan menunjukkan hubungan positif dengan churn, batang "
                               "hijau ke kiri hubungan negatif, ketika fitur lain tetap. Hubungan "
                               "ini tidak membuktikan sebab-akibat."),
                    unsafe_allow_html=True)
        with st.expander("Catatan tentang koefisien"):
            st.write("Koefisien Logistic Regression bekerja pada skala log-odds. Angka dan kategori "
                     "diproses dengan cara berbeda, sehingga besar bobotnya tidak bisa langsung "
                     "dipakai sebagai peringkat pengaruh. Fitur yang saling berkaitan juga "
                     "dapat memengaruhi arah koefisien.")
        try:
            pre = pipe.named_steps["pre"]
            feats = pre.get_feature_names_out()
            readable = [feature_label(f) for f in feats]
            clf = pipe.named_steps["clf"]
            if hasattr(clf, "coef_"):
                imp = pd.DataFrame({"Fitur": readable, "Bobot": clf.coef_[0]})
                imp["Abs"] = imp["Bobot"].abs()
                top = imp.sort_values("Abs", ascending=False).head(15).sort_values("Bobot")
                e_left, e_right = st.columns([1.4, 1], gap="large")
                with e_left:
                    show_chart(coefficient_chart(top.drop(columns="Abs")))
                with e_right:
                    st.markdown("**15 fitur dengan koefisien terbesar**")
                    st.dataframe(top.drop(columns="Abs").sort_values("Bobot", ascending=False),
                                 width="stretch", hide_index=True, height=420,
                                 column_config={"Bobot": st.column_config.NumberColumn(
                                     "Bobot", format="%+.3f")})
            else:
                imp = pd.DataFrame({"Fitur": readable, "Importance": clf.feature_importances_})
                top = imp.sort_values("Importance", ascending=False).head(15)
                e_left, e_right = st.columns([1.4, 1], gap="large")
                with e_left:
                    show_chart(alt.Chart(top).mark_bar(color=TOK["accent"], cornerRadiusEnd=3).encode(
                        y=alt.Y("Fitur:N", sort="-x", title=None),
                        x=alt.X("Importance:Q", title="Importance"),
                        tooltip=["Fitur:N", alt.Tooltip("Importance:Q", format=".4f")]).properties(height=420))
                with e_right:
                    st.dataframe(top, width="stretch", hide_index=True, height=420)
        except Exception as e:
            st.caption(f"Grafik fitur belum bisa ditampilkan: {e}")

    with st.expander("Sumber data dan keterbatasan model"):
        st.markdown("Sumber: [IBM Telco Customer Churn di Kaggle]"
                    "(https://www.kaggle.com/datasets/blastchar/telco-customer-churn). "
                    "Data awal berisi 7.043 pelanggan. Setelah 11 baris dengan TotalCharges kosong "
                    "dihapus, tersisa 7.032 pelanggan untuk training dan testing.")
        st.write("customerID hanya digunakan sebagai identitas. TotalCharges tidak diminta agar "
                 "form lebih sederhana. Total tagihan berkaitan dengan lama berlangganan, tetapi "
                 "tidak selalu sama dengan tagihan bulanan dikali jumlah bulan. Kami belum "
                 "membandingkan hasil model dengan dan tanpa fitur ini.")
        st.write("Hasil model berasal dari satu dataset dan belum diuji pada operator lain. "
                 "TETAP berarti diprediksi tidak churn, bukan jaminan pelanggan akan terus "
                 "berlangganan. Saran penawaran juga belum diuji efektivitasnya.")

with tab4:
    st.markdown(ui.section("Mengenal Data Pelanggan", "search",
                           "Pemeriksaan awal untuk memahami isi dan pola data sebelum pemodelan. "
                           "Grafik hubungan dengan churn hanya memakai data latih; data uji "
                           "disimpan untuk evaluasi akhir."),
                unsafe_allow_html=True)
    eda_dir = BASE / "docs" / "eda(explaratory data analysis)"
    if (eda_dir / "summary.json").exists():
        summary = json.loads((eda_dir / "summary.json").read_text(encoding="utf-8"))
        st.markdown(
            f"Dari **{count_text(summary['raw_rows'])} data**, tersisa "
            f"**{count_text(summary['clean_rows'])} data setelah dibersihkan**. "
            f"Model menggunakan {summary['input_features']} fitur. "
            "Churn Yes berarti berhenti berlangganan, sedangkan No berarti tidak churn.")
        with st.expander("Isi dataset dan hasil pemeriksaan data"):
            st.markdown("**Arti setiap variabel**")
            st.dataframe(pd.read_csv(eda_dir / "data_dictionary.csv"), width="stretch", hide_index=True)
            st.markdown("**Mengapa TotalCharges dihapus?**")
            st.write("TotalCharges (total tagihan selama berlangganan) tidak dipakai sebagai fitur. "
                     "Nilainya berkorelasi erat dengan tenure dan tidak selalu sama dengan "
                     "MonthlyCharges × tenure, sehingga form cukup meminta tenure dan tagihan "
                     "bulanan. Performa model dengan dan tanpa fitur ini belum dibandingkan.")
            st.caption("Pada tahap cleaning, 11 baris dengan TotalCharges kosong dihapus lebih dulu "
                       "agar data pemodelan sama dengan eksperimen awal, lalu kolomnya dibuang.")
            st.markdown("**Ringkasan statistik**")
            st.dataframe(pd.read_csv(eda_dir / "descriptive_statistics.csv"), width="stretch", hide_index=True)
            st.markdown("**Data yang kosong (missing value)**")
            st.dataframe(pd.read_csv(eda_dir / "missing_values.csv"), width="stretch", hide_index=True)
            st.markdown("**Data yang berulang (duplikat)**")
            duplicate_labels = {
                "raw_full_rows": "Baris yang sama persis pada data awal",
                "customerID": "customerID yang berulang",
                "raw_without_id": "Baris yang sama setelah customerID dihapus",
                "clean_without_id_total_including_target": "Baris yang sama tanpa ID dan TotalCharges, termasuk label churn",
                "clean_features_only": "Pelanggan dengan nilai fitur yang sama",
                "test_features_matching_train": "Pelanggan testing dengan profil fitur yang sama seperti training",
            }
            st.dataframe(pd.DataFrame([(duplicate_labels.get(key, key), value)
                                       for key, value in summary["duplicates"].items()],
                                      columns=["Pemeriksaan", "Jumlah"]),
                         width="stretch", hide_index=True)
            st.markdown("**Nilai yang jauh dari pola umum (outlier)**")
            st.dataframe(pd.read_csv(eda_dir / "outliers_iqr.csv"), width="stretch", hide_index=True)
            st.caption("Sebelas baris yang dihapus adalah pelanggan dengan lama berlangganan 0 bulan "
                       "dan label tidak churn. Karena itu, hasil untuk pelanggan baru perlu dibaca "
                       "dengan hati-hati. Pelanggan dengan fitur yang sama tetap disimpan jika ID-nya "
                       "berbeda. Pemeriksaan IQR tidak menemukan outlier secara keseluruhan, tetapi "
                       "itu belum berarti setiap catatan pasti benar.")
        figures = summary["figures"]
        for start in range(0, len(figures), 2):
            gallery = st.columns(2, gap="large")
            for offset, figure in enumerate(figures[start:start + 2]):
                stem = Path(figure["file"]).stem.split("_", 1)[-1]
                with gallery[offset]:
                    with st.container(key=f"panel_fig_{start + offset}"):
                        st.markdown(f"**{start + offset + 1}. {FIGURE_TITLES.get(stem, stem)}**")
                        st.image(str(eda_dir / figure["file"]), width="stretch")
                        st.markdown(ui.note_card(figure["interpretation"]), unsafe_allow_html=True)
    else:
        st.info("Grafik EDA belum tersedia. Jalankan notebook `01_EDA.ipynb` untuk membuatnya.")

    st.markdown(ui.section("Dokumentasi Kelompok 12", "doc"), unsafe_allow_html=True)
    repo_docs = "https://github.com/makhdanramadhan-ui/Machine-Learning-Project/blob/main/docs/"
    st.markdown(ui.doc_links([
        ("Laporan EDA", f"{repo_docs}eda%28explaratory%20data%20analysis%29/EDA.md"),
        ("Lima jurnal dan tabel studi literatur", f"{repo_docs}STUDI_LITERATUR.md"),
    ]), unsafe_allow_html=True)

st.markdown(
    '<div class="sheet-foot">Kelompok 12 · B2 · Muhamad Akhdan Ramadhan (J0404241102) · '
    'Thevan Erlangga (J0404241073) · Fachri Abyasa Tarid (J0404241136)</div>',
    unsafe_allow_html=True,
)
