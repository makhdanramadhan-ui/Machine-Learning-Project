"""Aplikasi Prediksi Customer Churn - Telco (UI Modern)
Pipeline: preprocessing + model dalam 1 file model_churn.pkl
"""
from pathlib import Path
import csv
import hashlib
import io
import joblib
import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from prediction import (
    InputValidationError, example_customers, input_schema, input_notes,
    predict_customers, risk_levels, high_risk_boundary,
)

BASE = Path(__file__).parent

st.set_page_config(
    page_title="Prediksi Customer Churn - Telco",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_resource
def load_models(model_stamp, calibration_stamp, metadata_stamp):
    """Muat sekali per versi artefak; metadata diverifikasi sebelum prediksi."""
    with open(BASE / "deployment_info.json", encoding="utf-8") as f:
        deployment = json.load(f)
    for filename, key in [("model_churn.pkl", "model_sha256"),
                          ("calibrator.pkl", "calibrator_sha256")]:
        digest = hashlib.sha256((BASE / filename).read_bytes()).hexdigest()
        if digest != deployment[key]:
            raise ValueError(f"{filename} tidak cocok dengan metadata evaluasi. Jalankan train.py.")
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
    st.info("Jalankan `python train.py`, lalu unggah model dan file hasil evaluasinya bersama-sama.")
    st.stop()

SCHEMA = input_schema(pipe)
THRESHOLD = float(DEPLOY["threshold"])
HIGH_BOUNDARY = high_risk_boundary(THRESHOLD)

# ---------- Theme: dark permanen ----------
DARK = True

# ---------- Top bar: brand ----------
st.markdown(
    "<div style='font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;opacity:.6;"
    "font-weight:700'>Telco &nbsp;•&nbsp; Customer Churn &nbsp;•&nbsp; ML Project</div>",
    unsafe_allow_html=True,
)

# ---------- CSS ----------
BG = "#0B0F19" if DARK else "#F4F6FB"
CARD = "#141B2E" if DARK else "#FFFFFF"
CARD2 = "#1A2340" if DARK else "#F8FAFF"
BORDER = "rgba(255,255,255,.09)" if DARK else "#E5E9F2"
TEXT = "#E9EDF5" if DARK else "#111827"
MUTED = "#9AA4B8" if DARK else "#6B7280"
INPUT_BG = "#1D2540" if DARK else "#FFFFFF"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
[data-testid="stAppViewContainer"] {{
    background: {BG};
    color: {TEXT};
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
}}
[data-testid="stHeader"] {{ background: transparent; }}
[data-testid="stToolbar"] {{ opacity: .7; }}
section[data-testid="stSidebar"] {{ display: none; }}

/* Hero */
.hero {{
    background: linear-gradient(135deg, #7C3AED 0%, #2563EB 55%, #06B6D4 100%);
    border-radius: 22px;
    padding: 28px 30px;
    color: white;
    box-shadow: 0 12px 40px rgba(37,99,235,.35);
    margin: 6px 0 18px 0;
    position: relative;
    overflow: hidden;
}}
.hero::after {{
    content: '';
    position: absolute; right: -60px; top: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(255,255,255,.28), transparent 65%);
}}
.hero h1 {{ margin: 0; font-size: 1.9rem; font-weight: 800; letter-spacing: -.02em; }}
.hero p {{ margin: 8px 0 14px 0; opacity: .92; font-size: .98rem; }}
.pill {{
    display: inline-block; padding: 6px 12px; border-radius: 999px;
    background: rgba(255,255,255,.16); border: 1px solid rgba(255,255,255,.25);
    font-size: .78rem; font-weight: 600; margin-right: 8px; margin-top: 6px;
    backdrop-filter: blur(6px);
}}

/* KPI cards */
.kpi {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 18px;
    padding: 16px 18px;
    box-shadow: 0 6px 22px rgba(0,0,0,{'0.28' if DARK else '0.06'});
}}
.kpi .label {{ font-size: .75rem; text-transform: uppercase; letter-spacing: .08em;
    color: {MUTED}; font-weight: 700; margin-bottom: 6px; }}
.kpi .value {{ font-size: 1.35rem; font-weight: 800; }}
.kpi .sub {{ font-size: .82rem; color: {MUTED}; margin-top: 4px; }}

/* Cards / containers */
div[data-testid="stContainer"] {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 18px;
}}
div[data-testid="stExpander"] {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 16px;
}}

/* Inputs */
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {{
    background: {INPUT_BG} !important;
    color: {TEXT} !important;
    border-radius: 12px !important;
}}
label p {{ font-weight: 600 !important; font-size: .86rem !important; }}

/* Tabs */
button[data-baseweb="tab"] {{
    border-radius: 12px 12px 0 0 !important;
    font-weight: 700 !important;
    padding: 10px 18px !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    background: linear-gradient(135deg, #7C3AED22, #2563EB22) !important;
    border-bottom: 3px solid #7C3AED !important;
}}

/* Primary button */
div.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, #7C3AED, #2563EB) !important;
    border: none !important;
    border-radius: 14px !important;
    padding: .7rem 1.2rem !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    box-shadow: 0 8px 24px rgba(124,58,237,.4);
    transition: transform .12s ease;
}}
div.stButton > button[kind="primary"]:hover {{ transform: translateY(-1px); }}
div.stButton > button:not([kind="primary"]) {{
    border-radius: 12px !important;
    font-weight: 600 !important;
}}

/* Result banner */
.result {{
    border-radius: 18px; padding: 20px 22px; margin: 14px 0;
    border: 1px solid {BORDER}; background: {CARD2};
}}
.result.low {{ border-left: 6px solid #10B981; }}
.result.mid {{ border-left: 6px solid #F59E0B; }}
.result.high {{ border-left: 6px solid #EF4444; }}
.badge {{
    display: inline-block; padding: 6px 14px; border-radius: 999px;
    font-weight: 800; font-size: .85rem; color: white; margin-bottom: 8px;
}}
.badge.low {{ background: linear-gradient(135deg,#10B981,#059669); }}
.badge.mid {{ background: linear-gradient(135deg,#F59E0B,#D97706); }}
.badge.high {{ background: linear-gradient(135deg,#EF4444,#DC2626); }}
.prob {{ font-size: 2rem; font-weight: 800; margin: 2px 0; }}

/* Rec card */
.rec {{
    background: {CARD2}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 12px 14px; margin-bottom: 8px;
}}

/* Confusion matrix grid */
.cm-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 10px 0; }}
.cm-cell {{ border-radius: 14px; padding: 16px; text-align: center; border: 1px solid {BORDER}; }}
.cm-cell b {{ font-size: 1.6rem; display: block; }}
.cm-tp {{ background: linear-gradient(135deg,#EF444433,#EF444422); }}
.cm-tn {{ background: linear-gradient(135deg,#10B98133,#10B98122); }}
.cm-fp {{ background: linear-gradient(135deg,#F59E0B33,#F59E0B22); }}
.cm-fn {{ background: linear-gradient(135deg,#8B5CF633,#8B5CF622); }}

.footer {{ text-align:center; color:{MUTED}; font-size:.8rem; margin: 28px 0 10px 0; }}
a {{ color: #60A5FA !important; }}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------- Helpers for matplotlib theming ----------
def style_fig(fig, ax_or_axes):
    axes = ax_or_axes if isinstance(ax_or_axes, (list, tuple)) else [ax_or_axes]
    fg = "#E5E7EB" if DARK else "#111827"
    for ax in axes:
        ax.set_facecolor("none")
        ax.tick_params(colors=fg)
        ax.yaxis.label.set_color(fg)
        ax.xaxis.label.set_color(fg)
        ax.title.set_color(fg)
        for s in ax.spines.values():
            s.set_color("#4B5563" if DARK else "#D1D5DB")
    fig.patch.set_facecolor("none")

BEST = INFO.get("best_model", "LogisticRegression") if INFO else "LogisticRegression"
MODEL_NAMES = {"LogisticRegression": "Logistic Regression", "DecisionTree": "Decision Tree",
               "RandomForest": "Random Forest"}
BEST_LABEL = MODEL_NAMES.get(BEST, BEST)
BASE_MET = INFO.get("metrics", {})
MET = DEPLOY["metrics"]
CVF1 = BASE_MET.get("CV_F1", "-")
ACC = MET.get("Accuracy", "-")
AUC = MET.get("ROC_AUC", "-")
REC = MET.get("Recall", "-")
N_TEST = DEPLOY["n_test"]
N_DATA = DEPLOY["n_train"] + N_TEST

def fmt(x):
    return f"{x:.4f}" if isinstance(x, float) else str(x)


def count_text(value):
    return f"{int(value):,}".replace(",", ".")


def option_label(value):
    """Terjemahkan tampilan pilihan; nilai yang diterima model tetap sama."""
    labels = {
        "Female": "Perempuan", "Male": "Laki-laki", "Yes": "Ya", "No": "Tidak",
        "No phone service": "Tidak memakai telepon", "No internet service": "Tidak memakai internet",
        "Fiber optic": "Fiber optik", "Month-to-month": "Bulanan", "One year": "Satu tahun",
        "Two year": "Dua tahun", "Electronic check": "Cek elektronik",
        "Mailed check": "Cek melalui pos", "Bank transfer (automatic)": "Transfer bank otomatis",
        "Credit card (automatic)": "Kartu kredit otomatis",
    }
    return labels.get(value, value)


def show_confusion_matrix(metrics):
    st.markdown(
        f"""<div class="cm-grid">
        <div class="cm-cell cm-tp"><span>TP • churn terdeteksi</span><b>{int(metrics['TP'])}</b>
        <span style="opacity:.7;font-size:.8rem">Diprediksi churn, memang churn</span></div>
        <div class="cm-cell cm-tn"><span>TN • tidak churn benar</span><b>{int(metrics['TN'])}</b>
        <span style="opacity:.7;font-size:.8rem">Diprediksi tetap, memang tidak churn</span></div>
        <div class="cm-cell cm-fp"><span>FP • alarm keliru</span><b>{int(metrics['FP'])}</b>
        <span style="opacity:.7;font-size:.8rem">Diprediksi churn, ternyata tidak churn</span></div>
        <div class="cm-cell cm-fn"><span>FN • churn terlewat</span><b>{int(metrics['FN'])}</b>
        <span style="opacity:.7;font-size:.8rem">Diprediksi tetap, ternyata churn</span></div>
        </div>""", unsafe_allow_html=True,
    )

# ---------- HERO ----------
st.markdown(
    f"""<div class="hero">
    <h1>📡 Prediksi Customer Churn — Telco</h1>
    <p>Perkirakan apakah pelanggan akan <b>berhenti berlangganan (churn)</b>.
    Coba satu pelanggan atau unggah CSV untuk melihat hasil beberapa pelanggan sekaligus.</p>
    <span class="pill">🏆 Model: {BEST_LABEL}</span>
    <span class="pill">🎯 CV-F1: {fmt(CVF1)}</span>
    <span class="pill">📈 ROC-AUC: {fmt(AUC)}</span>
    <span class="pill">🗂️ {count_text(N_DATA)} pelanggan • {DEPLOY['n_features']} fitur</span>
    </div>""",
    unsafe_allow_html=True,
)

# ---------- KPI ROW (pengganti sidebar) ----------
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"<div class='kpi'><div class='label'>🏆 Model Terbaik</div>"
                f"<div class='value'>{BEST_LABEL}</div>"
                f"<div class='sub'>CV-F1 tertinggi dari tiga model</div></div>", unsafe_allow_html=True)
with k2:
    st.markdown(f"<div class='kpi'><div class='label'>🎯 Akurasi & Recall</div>"
                f"<div class='value'>{ACC:.2%} / {REC:.2%}</div>"
                f"<div class='sub'>Diuji pada {count_text(N_TEST)} pelanggan</div></div>", unsafe_allow_html=True)
with k3:
    st.markdown(f"<div class='kpi'><div class='label'>📈 ROC-AUC</div>"
                f"<div class='value'>{fmt(AUC)}</div>"
                f"<div class='sub'>0.5 = acak, 1.0 = sempurna</div></div>", unsafe_allow_html=True)
with k4:
    st.markdown("<div class='kpi'><div class='label'>🗂️ Dataset</div>"
                f"<div class='value'>{count_text(N_DATA)}</div>"
                "<div class='sub'>Data pelanggan setelah dibersihkan</div></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Tentang model dan cara membaca hasil", expanded=False):
    c_a, c_b = st.columns([1, 2])
    with c_a:
        st.write(f"**Model yang dipilih:** {BEST_LABEL}")
        st.caption("Model ini mendapat rata-rata F1 tertinggi pada validasi silang lima fold. "
                   "Akurasi, recall, dan AUC di atas dihitung setelah kalibrasi, sesuai model yang dipakai aplikasi.")
        if MET:
            st.json(MET)
    with c_b:
        st.caption(f"Model menggunakan {DEPLOY['n_features']} informasi pelanggan. "
                   "Data angka dan kategori diproses otomatis sebelum diprediksi. "
                   "Kalibrasi sigmoid membantu menyesuaikan probabilitas dan dilatih hanya dengan data training.")
        st.write(f"**Aturan keputusan:** CHURN jika probabilitas ≥ {THRESHOLD:.0%}; "
                 "TETAP jika di bawah threshold tersebut.")
        st.caption("Threshold dipilih dari hasil validasi data training. Data testing dipakai untuk "
                   "mengukur hasil akhirnya. Label CHURN menunjukkan risiko yang melewati threshold, bukan kepastian.")

tab1, tab2, tab3, tab4 = st.tabs([
    "🔮 Prediksi Single", "📁 Prediksi Batch (CSV)", "📊 Dashboard & Model", "🔎 EDA & Dokumentasi",
])

# ---------- TAB 1 ----------
with tab1:
    with st.container(border=True):
        st.markdown("### 🧾 Data Pelanggan")
        st.caption("Isi data pelanggan, lalu klik Prediksi Sekarang. Pilihan layanan tambahan "
                   "akan menyesuaikan layanan telepon dan internet yang digunakan.")
        c1, c2, c3 = st.columns(3)
        with c1:
            gender = st.selectbox("Jenis Kelamin", ["Female", "Male"], format_func=option_label)
            SeniorCitizen = st.selectbox("Lansia (SeniorCitizen)", ["No", "Ya"], index=0, format_func=option_label)
            Partner = st.selectbox("Punya Pasangan", ["Yes", "No"], index=1, format_func=option_label)
            Dependents = st.selectbox("Punya Tanggungan", ["Yes", "No"], index=1, format_func=option_label)
            tenure = st.number_input("Lama Berlangganan (bulan)", 0, 72, 12,
                                     help="Tenure: jumlah bulan pelanggan sudah berlangganan.")
            PhoneService = st.selectbox("Layanan Telepon", ["Yes", "No"], format_func=option_label)
            _ml_lock = (PhoneService == "No")
            _ml_opts = ["No phone service"] if _ml_lock else ["Yes", "No"]
            MultipleLines = st.selectbox("Lebih dari Satu Jalur Telepon", _ml_opts,
                disabled=_ml_lock, format_func=option_label,
                help="MultipleLines: apakah pelanggan memakai lebih dari satu jalur telepon.")
        with c2:
            InternetService = st.selectbox("Layanan Internet", ["Fiber optic", "DSL", "No"], format_func=option_label)
            _lock = (InternetService == "No")
            _opts = ["No internet service"] if _lock else ["Yes", "No"]
            OnlineSecurity = st.selectbox("Keamanan Online", _opts, disabled=_lock, format_func=option_label)
            OnlineBackup = st.selectbox("Backup Online", _opts, disabled=_lock, format_func=option_label)
            DeviceProtection = st.selectbox("Perlindungan Perangkat", _opts, disabled=_lock, format_func=option_label)
            TechSupport = st.selectbox("Bantuan Teknis", _opts, disabled=_lock, format_func=option_label)
            StreamingTV = st.selectbox("Streaming TV", _opts, disabled=_lock, format_func=option_label)
            StreamingMovies = st.selectbox("Streaming Film", _opts, disabled=_lock, format_func=option_label)
        with c3:
            Contract = st.selectbox("Kontrak", ["Month-to-month", "One year", "Two year"], format_func=option_label)
            PaperlessBilling = st.selectbox("Tagihan Tanpa Kertas", ["Yes", "No"], format_func=option_label)
            PaymentMethod = st.selectbox("Metode Pembayaran", ["Electronic check", "Mailed check",
                "Bank transfer (automatic)", "Credit card (automatic)"], format_func=option_label)
            MonthlyCharges = st.number_input("Tagihan Bulanan ($)", 0.0, 120.0, 70.0, step=1.0,
                format="%.2f",
                help="Batas input $0–$120; rentang data latih $18,25–$118,75. Isi tagihan aktual.")

        b1, b2, b3 = st.columns([1, 2, 1])
        with b2:
            predict = st.button("🚀 Prediksi Sekarang", type="primary", width="stretch")

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
        st.info("Input telah berubah. Klik Prediksi Sekarang untuk memperbarui hasil.")
    if result and result["input"] == fingerprint:
        prob, pred = result["prob"], result["pred"]
        for note in input_notes(row):
            st.info(note)

        if prob < THRESHOLD:
            lvl, cls = "🟢 RISIKO RENDAH", "low"
        elif prob < HIGH_BOUNDARY:
            lvl, cls = "🟡 RISIKO SEDANG", "mid"
        else:
            lvl, cls = "🔴 RISIKO TINGGI", "high"

        st.markdown(
            f"""<div class="result {cls}">
            <span class="badge {cls}">{lvl}</span>
            <div class="prob">{prob*100:.2f}%</div>
            <div style="opacity:.85">Keputusan model: <b>{'CHURN' if pred == 1 else 'TETAP'}</b>
            • Probabilitas churn terkalibrasi</div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.progress(prob)
        st.caption(f"Threshold keputusan: {THRESHOLD:.0%}. Risiko rendah: < {THRESHOLD:.0%}; "
                   f"sedang: {THRESHOLD:.0%}–< {HIGH_BOUNDARY:.0%}; tinggi: ≥ {HIGH_BOUNDARY:.0%}. "
                   "Kategori risiko membantu membaca hasil; model tetap memprediksi churn atau tidak churn.")
        st.caption("TETAP berarti pelanggan diprediksi tidak churn. Probabilitas sudah disesuaikan "
                   "dengan kalibrasi sigmoid; detail pengujiannya ada di Dashboard & Model.")

        st.markdown("### 💡 Saran untuk Mempertahankan Pelanggan")
        st.caption("Saran berikut disesuaikan dengan data yang diisi. Efektivitasnya perlu diuji, "
                   "karena model belum mengukur dampak penawaran terhadap churn.")
        recs = []
        if Contract == "Month-to-month":
            recs.append(("📝 Kontrak", "Pertimbangkan penawaran kontrak satu atau dua tahun dengan diskon."))
        if InternetService == "Fiber optic" and MonthlyCharges > 75:
            recs.append(("💸 Tagihan", "Tinjau paket fiber yang digunakan dan tawarkan paket yang lebih sesuai."))
        if PaymentMethod == "Electronic check":
            recs.append(("💳 Pembayaran", "Tawarkan pembayaran otomatis melalui transfer atau kartu."))
        if TechSupport in ("No", "No internet service") and InternetService != "No":
            recs.append(("🛠️ Bantuan teknis", "Pertimbangkan masa coba layanan bantuan teknis."))
        if tenure < 6:
            recs.append(("🌱 Pelanggan baru", "Bantu pelanggan memahami layanan dan tanyakan pengalamannya setelah bulan pertama."))
        if not recs:
            recs.append(("💎 Layanan", "Jaga kualitas layanan dan pertimbangkan penghargaan untuk pelanggan lama."))
        for title, desc in recs:
            st.markdown(f"<div class='rec'><b>{title}</b> — {desc}</div>", unsafe_allow_html=True)

# ---------- TAB 2 ----------
with tab2:
    with st.container(border=True):
        st.markdown("### 📤 Upload CSV untuk Prediksi Massal")
        st.caption("Gunakan template di bawah atau CSV dengan kolom yang sama. Kolom `customerID`, "
                   "`Churn`, dan `TotalCharges` boleh disertakan, tetapi tidak dipakai untuk prediksi.")
        st.download_button("⬇️ Download Template CSV", example_customers().to_csv(index=False).encode("utf-8"),
                           "template_pelanggan.csv", "text/csv", width="stretch")
        with st.expander("Panduan mengisi CSV"):
            st.write("Kolom wajib: " + ", ".join(SCHEMA["columns"]))
            st.caption("Simpan CSV sebagai UTF-8 dengan pemisah koma. SeniorCitizen diisi 0 atau 1, "
                       "tenure dengan bulan bulat 0–72, dan MonthlyCharges dengan angka 0–120. "
                       "Pilihan layanan tambahan harus sesuai dengan layanan telepon dan internet. "
                       "Jika ada data yang salah, perbaiki dulu agar seluruh pelanggan bisa diproses.")
            st.json(SCHEMA["categories"])
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
        rate = float((out["Prediksi"] == "CHURN").mean() * 100)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"<div class='kpi'><div class='label'>Total Baris</div>"
                        f"<div class='value'>{len(out)}</div></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div class='kpi'><div class='label'>Prediksi Churn</div>"
                        f"<div class='value'>{churn_n}</div></div>", unsafe_allow_html=True)
        with m3:
            st.markdown(f"<div class='kpi'><div class='label'>Persentase Prediksi Churn</div>"
                        f"<div class='value'>{rate:.1f}%</div></div>", unsafe_allow_html=True)

        st.caption(f"Threshold: {THRESHOLD:.0%}. Kolom Prob_Churn berisi probabilitas dalam persen. "
                   f"Menampilkan {min(20, len(out))} dari {count_text(len(out))} pelanggan; unduhan memuat semua hasil.")
        st.dataframe(out.head(20), width="stretch", hide_index=True)
        st.bar_chart(out["Prediksi"].value_counts())
        st.download_button("⬇️ Download Hasil (CSV)",
                           out.to_csv(index=False).encode(), "hasil_prediksi.csv", "text/csv",
                           width="stretch")

# ---------- TAB 3 ----------
with tab3:
    with st.container(border=True):
        st.markdown("### 🎯 Hasil Pengujian Model Aplikasi")
        st.caption(f"{BEST_LABEL} dengan kalibrasi sigmoid. Diuji pada {count_text(N_TEST)} pelanggan "
                   "yang tidak digunakan untuk melatih model.")
        st.dataframe(pd.DataFrame([
            {"Konfigurasi": f"Aplikasi — threshold {THRESHOLD:.2f}", **MET},
            {"Konfigurasi": "Pembanding — threshold 0.50", **DEPLOY["metrics_at_0_5"]},
        ]), width="stretch", hide_index=True)
        show_confusion_matrix(MET)
        st.info(f"Dari {MET['TP'] + MET['FN']} pelanggan yang benar-benar churn, "
                f"{MET['TP']} berhasil terdeteksi dan {MET['FN']} terlewat. "
                f"Sebanyak {MET['FP']} pelanggan yang tidak churn juga ditandai CHURN. "
                "Menurunkan threshold membantu mendeteksi lebih banyak churn, tetapi bisa menambah prediksi yang keliru.")
        with st.expander(f"Mengapa threshold-nya {THRESHOLD:.0%}?", expanded=False):
            st.write(f"Kami mencoba threshold 0,10 sampai 0,60 dengan selisih 0,01. "
                     f"Threshold {THRESHOLD:.2f} memberi F1 tertinggi pada validasi data training. "
                     "Artinya, model memberi label CHURN ketika probabilitas mencapai threshold ini, "
                     "meskipun masih di bawah 50%.")
            st.caption("Prediksi validasi dibuat dengan lima fold: setiap bagian diprediksi oleh model "
                       "yang dilatih pada bagian lainnya, dengan kalibrasi di dalam proses itu. "
                       f"F1 untuk memilih threshold: {DEPLOY['oof_tuning_f1']:.4f}. "
                       "Skor ini dipakai untuk memilih pengaturan, bukan hasil pengujian akhir. "
                       "Parameter model juga sudah dipilih dari data training.")
            st.write(f"Kalibrasi sigmoid menyesuaikan probabilitas model. Pada data testing, Brier score "
                     f"turun dari {CALINFO['brier_base']:.4f} menjadi {CALINFO['brier_cal']:.4f}. "
                     "Semakin kecil Brier, semakin kecil kesalahan probabilitasnya.")
            st.dataframe(pd.DataFrame(CALINFO["reliability_test"]).rename(columns={
                "band": "Kategori risiko", "n": "Pelanggan", "mean_pred": "Rata-rata probabilitas",
                "empirical": "Proporsi churn aktual",
            }).replace({"Kategori risiko": {"LOW": "Rendah", "MID": "Sedang", "HIGH": "Tinggi"}}),
                         width="stretch", hide_index=True)
            st.caption("Tabel membandingkan rata-rata probabilitas dengan proporsi pelanggan yang benar-benar "
                       "churn pada setiap kategori risiko. Kedua kolom memakai skala 0–1.")

    with st.container(border=True):
        st.markdown("### 🏆 Perbandingan Tiga Model")
        st.caption("Ketiga model ini diuji sebelum kalibrasi, dengan threshold 50%. Model dipilih "
                   "berdasarkan CV-F1 data training, bukan akurasi testing tertinggi. "
                   "Hasil model setelah kalibrasi ditampilkan pada tabel aplikasi di atas.")
        with st.expander("📖 Cara membaca metrik", expanded=False):
            st.markdown("Label: churn = 1, tidak churn = 0. Nilai metrik pada tabel memakai skala 0–1.")
            st.markdown(
                "| Metrik | Rumus | Arti |\n"
                "|---|---|---|\n"
                "| TP | TP | Diprediksi churn dan memang churn |\n"
                "| TN | TN | Prediksi tidak churn (0), aktual tidak churn (0) ✅ |\n"
                "| FP | FP | Prediksi churn (1), aktual tidak churn (0) — alarm keliru |\n"
                "| FN | FN | Prediksi tidak churn (0), aktual churn (1) — churn terlewat |\n"
                "| Accuracy | (TP+TN)/total | Proporsi seluruh prediksi yang benar |\n"
                "| Precision | TP/(TP+FP) | Dari yang diprediksi churn, berapa yang benar-benar churn |\n"
                "| Recall | TP/(TP+FN) | Dari seluruh pelanggan churn, berapa yang terdeteksi |\n"
                "| F1 | 2×P×R/(P+R) | Rata-rata harmonik precision dan recall |\n"
                "| ROC-AUC | luas kurva ROC | 0.5 = acak, 1.0 = sempurna |")
            st.divider()
            st.markdown("**F1** merangkum precision dan recall. Keduanya perlu diperhatikan karena "
                        "pelanggan churn lebih sedikit daripada pelanggan yang tidak churn. "
                        "Akurasi tinggi saja belum berarti model berhasil mendeteksi churn.")
            st.markdown("**CV-F1** adalah rata-rata F1 dari validasi silang lima fold. Data training "
                        "dibagi menjadi lima bagian: model dilatih pada empat bagian lalu divalidasi "
                        "pada satu bagian, bergantian lima kali. Skor ini dipakai untuk memilih model.")
            st.markdown("**ROC-AUC** menunjukkan kemampuan model membedakan churn dan tidak churn "
                        "pada berbagai threshold. Kurva ROC membandingkan recall dengan "
                        "false positive rate `FP/(FP+TN)`. Nilai 0,5 setara urutan acak; "
                        "semakin mendekati 1, semakin baik pemisahannya.")
        if CMP is not None:
            _cmp_show = CMP.copy()
            _cmp_show["Model"] = _cmp_show["Model"].replace(MODEL_NAMES)
            _cmp_show.index = _cmp_show.index + 1
            st.dataframe(_cmp_show, width="stretch")
            cm_model = st.selectbox("Pilih model untuk melihat confusion matrix", CMP["Model"].tolist(),
                                    format_func=lambda name: MODEL_NAMES.get(name, name))
            b = CMP[CMP["Model"] == cm_model].iloc[0]
            st.markdown(f"**Confusion matrix — {MODEL_NAMES.get(cm_model, cm_model)} "
                        f"({count_text(N_TEST)} pelanggan testing):**")
            show_confusion_matrix(b)
            fig, ax = plt.subplots(figsize=(6.5, 2.6))
            plot_df = CMP.set_index("Model")[["Accuracy", "Precision", "Recall", "F1"]]
            plot_df = plot_df.rename(index=MODEL_NAMES)
            plot_df.plot(kind="barh", ax=ax, color=["#7C3AED", "#2563EB", "#06B6D4", "#10B981"])
            ax.set_xlabel("Skor", fontsize=9)
            ax.tick_params(labelsize=8)
            leg = ax.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.22),
                            ncol=4, frameon=True, handlelength=1.2, handletextpad=0.4,
                            columnspacing=1.0)
            leg.get_frame().set_alpha(0.95)
            style_fig(fig, ax)
            plt.tight_layout()
            st.pyplot(fig, width="content")
            plt.close(fig)
            selected = CMP[CMP["Model"] == BEST].iloc[0]
            top_recall = CMP.loc[CMP["Recall"].idxmax()]
            top_accuracy = CMP.loc[CMP["Accuracy"].idxmax()]
            st.info(
                f"**Mengapa {BEST_LABEL}?** Model ini mendapat CV-F1 tertinggi "
                f"({selected['CV_F1']:.4f}) pada data training. Saat diuji sebelum kalibrasi, "
                f"{MODEL_NAMES.get(top_recall['Model'], top_recall['Model'])} memiliki recall tertinggi "
                f"({top_recall['Recall']:.2%}), sedangkan "
                f"{MODEL_NAMES.get(top_accuracy['Model'], top_accuracy['Model'])} memiliki akurasi tertinggi "
                f"({top_accuracy['Accuracy']:.2%}). Hasil testing ini dilaporkan tanpa mengganti model yang sudah dipilih.")
            if {"Train_F1", "CV_TRAIN_F1", "CV_F1_STD"}.issubset(CMP.columns):
                st.markdown("**Perbandingan F1 saat training, validasi, dan testing:**")
                st.dataframe(CMP[["Model", "Train_F1", "CV_TRAIN_F1", "CV_F1", "CV_F1_STD", "F1"]].replace(
                    {"Model": MODEL_NAMES}),
                             width="stretch", hide_index=True)
                largest_gap = CMP.loc[(CMP["Train_F1"] - CMP["F1"]).idxmax()]
                st.caption(f"{MODEL_NAMES.get(largest_gap['Model'], largest_gap['Model'])} memiliki selisih "
                           f"F1 training dan testing terbesar: {largest_gap['Train_F1']:.4f} vs "
                           f"{largest_gap['F1']:.4f}. Model jauh lebih baik pada data yang sudah dipelajari "
                           "daripada data baru. Ini indikasi overfitting, dan terlihat juga pada skor validasinya.")
            if CVDET is not None:
                st.markdown("**F1 pada setiap sesi validasi:**")
                st.caption("Validasi dilakukan lima kali pada bagian data training yang berbeda. "
                           "Data testing 20% disimpan terpisah dan tidak masuk ke lima fold ini.")
                _cv_show = CVDET.rename(columns={"Fold": "Session"}).replace({"Model": MODEL_NAMES})
                _cv_pivot = _cv_show.pivot(index="Session", columns="Model", values="F1").reset_index()
                _cv_pivot = _cv_pivot.rename(
                    columns={c: f"Nilai F1 {c}" for c in _cv_pivot.columns if c != "Session"})
                # Mapping fold standar sklearn: session k -> test fold k, train = sisanya
                _fold_map = {
                    1: ("2, 3, 4, 5", "1"),
                    2: ("1, 3, 4, 5", "2"),
                    3: ("1, 2, 4, 5", "3"),
                    4: ("1, 2, 3, 5", "4"),
                    5: ("1, 2, 3, 4", "5"),
                }
                _cv_pivot["Train Fold"] = _cv_pivot["Session"].map(lambda s: _fold_map.get(s, ("-", "-"))[0])
                _cv_pivot["Validation Fold"] = _cv_pivot["Session"].map(lambda s: _fold_map.get(s, ("-", "-"))[1])
                # Urutan kolom: Session, Train, Test, baru nilai F1
                _f1_cols = [c for c in _cv_pivot.columns if c.startswith("Nilai F1")]
                _cv_pivot = _cv_pivot[["Session", "Train Fold", "Validation Fold"] + _f1_cols]
                st.dataframe(_cv_pivot, width="stretch", hide_index=True)
                fig0, ax0 = plt.subplots(figsize=(6.5, 2.6))
                for m in CVDET["Model"].unique():
                    d = CVDET[CVDET["Model"] == m].sort_values("Fold")
                    ax0.plot(d["Fold"], d["F1"], marker="o", label=MODEL_NAMES.get(m, m), linewidth=2.2, markersize=4)
                ax0.set_xticks([1, 2, 3, 4, 5])
                ax0.set_xlabel("Sesi validasi", fontsize=9)
                ax0.set_ylabel("F1", fontsize=9)
                ax0.tick_params(labelsize=8)
                _leg0 = ax0.legend(fontsize=8, frameon=False, loc="best", labelcolor="white")
                for _t in _leg0.get_texts():
                    _t.set_color("white")
                ax0.grid(alpha=.2)
                style_fig(fig0, ax0)
                plt.tight_layout()
                st.pyplot(fig0)
                plt.close(fig0)

    with st.container(border=True):
        st.markdown("### ⭐ Hubungan Fitur dengan Prediksi")
        st.caption("Grafik ini menampilkan koefisien model sebelum kalibrasi. Merah menunjukkan "
                   "hubungan positif dengan churn, hijau hubungan negatif, ketika fitur lain tetap. "
                   "Hubungan ini tidak membuktikan sebab-akibat.")
        with st.expander("Catatan tentang koefisien"):
            st.write("Koefisien Logistic Regression bekerja pada skala log-odds. Angka dan kategori "
                     "diproses dengan cara berbeda, sehingga besar bobotnya tidak bisa langsung "
                     "dipakai sebagai peringkat pengaruh. Fitur yang saling berkaitan juga "
                     "dapat memengaruhi arah koefisien.")
        try:
            pre = pipe.named_steps["pre"]
            feats = pre.get_feature_names_out()
            clean = [f.split("__", 1)[-1] for f in feats]
            clf = pipe.named_steps["clf"]
            if hasattr(clf, "coef_"):
                imp = pd.DataFrame({"Fitur": clean, "Bobot": clf.coef_[0]})
                imp["Abs"] = imp["Bobot"].abs()
                top = imp.sort_values("Abs", ascending=False).head(15).sort_values("Bobot")
                fig2, ax2 = plt.subplots(figsize=(8, 5))
                colors = ["#EF4444" if v > 0 else "#10B981" for v in top["Bobot"]]
                ax2.barh(top["Fitur"], top["Bobot"], color=colors, edgecolor="none", height=.6)
                ax2.set_xlabel("Koefisien model (log-odds)")
                ax2.grid(axis="x", alpha=.2)
                style_fig(fig2, ax2)
                plt.tight_layout()
                st.pyplot(fig2)
                plt.close(fig2)
                st.dataframe(top.drop(columns="Abs"), width="stretch", hide_index=True)
            else:
                imp = pd.DataFrame({"Fitur": clean, "Importance": clf.feature_importances_})
                top = imp.sort_values("Importance", ascending=False).head(15).sort_values("Importance")
                fig2, ax2 = plt.subplots(figsize=(8, 5))
                ax2.barh(top["Fitur"], top["Importance"], color="#7C3AED", height=.6)
                ax2.set_xlabel("Importance")
                style_fig(fig2, ax2)
                plt.tight_layout()
                st.pyplot(fig2)
                plt.close(fig2)
                st.dataframe(top, width="stretch", hide_index=True)
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
    st.markdown("### 🔎 Mengenal Data Pelanggan (EDA)")
    eda_dir = BASE / "docs" / "eda(explaratory data analysis)"
    if (eda_dir / "summary.json").exists():
        summary = json.loads((eda_dir / "summary.json").read_text(encoding="utf-8"))
        st.caption("EDA adalah pemeriksaan awal untuk memahami isi dan pola data sebelum membuat model. "
                   "Grafik hubungan dengan churn menggunakan data training saja; data testing disimpan "
                   "untuk pengujian akhir.")
        st.write(f"Dari **{count_text(summary['raw_rows'])} data**, tersisa "
                 f"**{count_text(summary['clean_rows'])} data setelah dibersihkan**. "
                 f"Model menggunakan {summary['input_features']} fitur. "
                 "Churn Yes berarti berhenti berlangganan, sedangkan No berarti tidak churn.")
        with st.expander("Isi dataset dan hasil pemeriksaan data"):
            st.markdown("**Arti setiap variabel**")
            st.dataframe(pd.read_csv(eda_dir / "data_dictionary.csv"), width="stretch", hide_index=True)
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
        for figure in summary["figures"]:
            st.image(str(eda_dir / figure["file"]), width="stretch")
            st.caption(figure["interpretation"])
    else:
        st.info("Grafik EDA belum tersedia. Jalankan `python eda.py` untuk membuatnya.")
    st.markdown("### 📚 Laporan Kelompok 12 — Kelas B2")
    repo_docs = "https://github.com/makhdanramadhan-ui/Machine-Learning-Project/blob/main/docs/"
    st.markdown(f"- [Laporan EDA]({repo_docs}eda%28explaratory%20data%20analysis%29/EDA.md)\n"
                f"- [Lima jurnal dan tabel studi literatur]({repo_docs}STUDI_LITERATUR.md)\n"
                f"- [PPT laporan]({repo_docs}ML2026_B2_Kelompok12_PrediksiCustomerChurn.pptx)")

st.markdown("<div class='footer'>Kelompok 12 • B2 • Muhamad Akhdan Ramadhan (J0404241102) • "
            "Thevan Erlangga (J0404241073) • Fachri Abyasa Tarid (J0404241136)</div>",
            unsafe_allow_html=True)
