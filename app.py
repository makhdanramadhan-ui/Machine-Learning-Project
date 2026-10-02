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
    st.error(f"Artefak aplikasi belum lengkap atau tidak konsisten: {exc}")
    st.info("Jalankan `python train.py`, lalu deploy seluruh artefak hasil training bersamaan.")
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


def show_confusion_matrix(metrics):
    st.markdown(
        f"""<div class="cm-grid">
        <div class="cm-cell cm-tp"><span>TP • churn terdeteksi</span><b>{int(metrics['TP'])}</b>
        <span style="opacity:.7;font-size:.8rem">pred 1, real 1</span></div>
        <div class="cm-cell cm-tn"><span>TN • tidak churn benar</span><b>{int(metrics['TN'])}</b>
        <span style="opacity:.7;font-size:.8rem">pred 0, real 0</span></div>
        <div class="cm-cell cm-fp"><span>FP • alarm keliru</span><b>{int(metrics['FP'])}</b>
        <span style="opacity:.7;font-size:.8rem">pred 1, real 0</span></div>
        <div class="cm-cell cm-fn"><span>FN • churn terlewat</span><b>{int(metrics['FN'])}</b>
        <span style="opacity:.7;font-size:.8rem">pred 0, real 1</span></div>
        </div>""", unsafe_allow_html=True,
    )

# ---------- HERO ----------
st.markdown(
    f"""<div class="hero">
    <h1>📡 Prediksi Customer Churn — Telco</h1>
    <p>Prediksi pelanggan <b>churn</b> atau <b>tidak churn</b>, lengkap dengan probabilitas
    terkalibrasi, rekomendasi retensi, prediksi massal CSV, dan transparansi model.</p>
    <span class="pill">🏆 Model: {BEST}</span>
    <span class="pill">🎯 CV-F1 model inti: {fmt(CVF1)}</span>
    <span class="pill">📈 ROC-AUC: {fmt(AUC)}</span>
    <span class="pill">🗂️ {N_DATA} data • {DEPLOY['n_features']} fitur</span>
    </div>""",
    unsafe_allow_html=True,
)

# ---------- KPI ROW (pengganti sidebar) ----------
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"<div class='kpi'><div class='label'>🏆 Model Terbaik</div>"
                f"<div class='value'>{BEST}</div>"
                f"<div class='sub'>Dipilih via CV-F1 tertinggi</div></div>", unsafe_allow_html=True)
with k2:
    st.markdown(f"<div class='kpi'><div class='label'>🎯 Akurasi & Recall</div>"
                f"<div class='value'>{fmt(ACC)} / {fmt(REC)}</div>"
                f"<div class='sub'>Model aplikasi • test {N_TEST} data</div></div>", unsafe_allow_html=True)
with k3:
    st.markdown(f"<div class='kpi'><div class='label'>📈 ROC-AUC</div>"
                f"<div class='value'>{fmt(AUC)}</div>"
                f"<div class='sub'>0.5 = acak, 1.0 = sempurna</div></div>", unsafe_allow_html=True)
with k4:
    st.markdown("<div class='kpi'><div class='label'>🗂️ Dataset</div>"
                f"<div class='value'>{N_DATA}</div>"
                "<div class='sub'>Telco-Customer-Churn • bersih</div></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Detail Info Model", expanded=False):
    c_a, c_b = st.columns([1, 2])
    with c_a:
        st.write(f"**Model terbaik:** `{BEST}`")
        st.caption("Model inti dipilih berdasarkan CV-F1 tertinggi (5-fold). "
                   "Angka KPI di atas adalah evaluasi model aplikasi setelah kalibrasi.")
        if MET:
            st.json(MET)
    with c_b:
        st.caption(f"Dataset: {N_DATA} pelanggan, {DEPLOY['n_features']} fitur mentah. "
                   "Preprocessing dilakukan otomatis di dalam pipeline. "
                   "Kalibrasi sigmoid dilatih hanya pada data train.")
        st.write(f"**Aturan keputusan:** CHURN jika probabilitas ≥ {THRESHOLD:.0%}; "
                 "TETAP jika di bawah ambang tersebut.")
        st.caption("Ambang dipilih dengan F1 maksimum dari prediksi out-of-fold pada data train. "
                   "Data test hanya digunakan untuk evaluasi akhir. CHURN adalah prediksi, bukan kepastian.")

tab1, tab2, tab3 = st.tabs(["🔮 Prediksi Single", "📁 Prediksi Batch (CSV)", "📊 Dashboard & Model"])

# ---------- TAB 1 ----------
with tab1:
    with st.container(border=True):
        st.markdown("### 🧾 Form Data Pelanggan")
        st.caption("Isi sesuai kondisi pelanggan saat ini, lalu klik Prediksi. "
                   "Field add-on terkunci otomatis jika tidak relevan.")
        c1, c2, c3 = st.columns(3)
        with c1:
            gender = st.selectbox("Jenis Kelamin", ["Female", "Male"])
            SeniorCitizen = st.selectbox("Lansia (SeniorCitizen)", ["No", "Ya"], index=0)
            Partner = st.selectbox("Punya Pasangan", ["Yes", "No"], index=1)
            Dependents = st.selectbox("Punya Tanggungan", ["Yes", "No"], index=1)
            tenure = st.number_input("Tenure (bulan)", 0, 72, 12)
            PhoneService = st.selectbox("Layanan Telepon", ["Yes", "No"])
            _ml_lock = (PhoneService == "No")
            _ml_opts = ["No phone service"] if _ml_lock else ["Yes", "No"]
            MultipleLines = st.selectbox("Multiple Lines", _ml_opts,
                disabled=_ml_lock)
        with c2:
            InternetService = st.selectbox("Internet", ["Fiber optic", "DSL", "No"])
            _lock = (InternetService == "No")
            _opts = ["No internet service"] if _lock else ["Yes", "No"]
            OnlineSecurity = st.selectbox("Online Security", _opts, disabled=_lock)
            OnlineBackup = st.selectbox("Online Backup", _opts, disabled=_lock)
            DeviceProtection = st.selectbox("Device Protection", _opts, disabled=_lock)
            TechSupport = st.selectbox("Tech Support", _opts, disabled=_lock)
            StreamingTV = st.selectbox("Streaming TV", _opts, disabled=_lock)
            StreamingMovies = st.selectbox("Streaming Movies", _opts, disabled=_lock)
        with c3:
            Contract = st.selectbox("Kontrak", ["Month-to-month", "One year", "Two year"])
            PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
            PaymentMethod = st.selectbox("Metode Bayar", ["Electronic check", "Mailed check",
                "Bank transfer (automatic)", "Credit card (automatic)"])
            MonthlyCharges = st.number_input("Monthly Charges ($)", 0.0, 120.0, 70.0, step=1.0,
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
        st.caption(f"CHURN jika probabilitas ≥ {THRESHOLD:.0%}. Risiko rendah: < {THRESHOLD:.0%}; "
                   f"sedang: {THRESHOLD:.0%}–< {HIGH_BOUNDARY:.0%}; tinggi: ≥ {HIGH_BOUNDARY:.0%}. "
                   "Batas risiko adalah kategori tampilan, bukan kelas baru yang dilatih.")
        st.caption(f"Kalibrasi sigmoid, 5-fold, train-only. Brier pada test: "
                   f"{CALINFO['brier_base']:.4f} → {CALINFO['brier_cal']:.4f} (lebih kecil lebih baik).")

        st.markdown("### 💡 Rekomendasi Retensi")
        st.caption("Saran berbasis aturan profil pelanggan; bukan bukti sebab-akibat "
                   "atau jaminan bahwa tindakan tersebut akan mengurangi churn.")
        recs = []
        if Contract == "Month-to-month":
            recs.append(("📝 Kontrak", "Tawarkan upgrade kontrak 1/2 tahun + diskon."))
        if InternetService == "Fiber optic" and MonthlyCharges > 75:
            recs.append(("💸 Tagihan", "Tagihan fiber tinggi — tawarkan bundling / cashback."))
        if PaymentMethod == "Electronic check":
            recs.append(("💳 Pembayaran", "Pertimbangkan opsi auto-pay (transfer/kartu)."))
        if TechSupport in ("No", "No internet service") and InternetService != "No":
            recs.append(("🛠️ Support", "Tawarkan paket TechSupport gratis 3 bulan."))
        if tenure < 6:
            recs.append(("🌱 Baru", "Pelanggan baru — onboarding intensif & cek kepuasan minggu ke-4."))
        if not recs:
            recs.append(("💎 Loyal", "Pertahankan kualitas layanan + loyalty reward."))
        for title, desc in recs:
            st.markdown(f"<div class='rec'><b>{title}</b> — {desc}</div>", unsafe_allow_html=True)

# ---------- TAB 2 ----------
with tab2:
    with st.container(border=True):
        st.markdown("### 📤 Upload CSV untuk Prediksi Massal")
        st.caption("Format kolom sama seperti Telco-Customer-Churn.csv (tanpa kolom Churn juga bisa). "
                   "Kolom `customerID`, `Churn`, `TotalCharges` otomatis diabaikan.")
        st.download_button("⬇️ Download Template CSV", example_customers().to_csv(index=False).encode("utf-8"),
                           "template_pelanggan.csv", "text/csv", width="stretch")
        with st.expander("Format dan validasi CSV"):
            st.write("Kolom wajib: " + ", ".join(SCHEMA["columns"]))
            st.caption("Gunakan CSV UTF-8 dengan pemisah koma. Semua baris harus valid; "
                       "baris bermasalah tidak dibuang otomatis. SeniorCitizen: 0/1, "
                       "tenure: bulan bulat 0–72, MonthlyCharges: angka 0–120. "
                       "Add-on harus konsisten dengan layanan telepon/internet.")
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
            out["Ambang_Churn"] = THRESHOLD
        except (InputValidationError, pd.errors.EmptyDataError, pd.errors.ParserError,
                UnicodeDecodeError, ValueError) as exc:
            st.error("CSV belum bisa diproses. Perbaiki input berikut:")
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
            st.markdown(f"<div class='kpi'><div class='label'>Churn Rate</div>"
                        f"<div class='value'>{rate:.1f}%</div></div>", unsafe_allow_html=True)

        st.caption(f"Keputusan dari probabilitas terkalibrasi dengan ambang {THRESHOLD:.0%}. "
                   f"Prob_Churn ditampilkan dalam persen. Pratinjau 20 dari {len(out)} baris.")
        st.dataframe(out.head(20), width="stretch", hide_index=True)
        st.bar_chart(out["Prediksi"].value_counts())
        st.download_button("⬇️ Download Hasil (CSV)",
                           out.to_csv(index=False).encode(), "hasil_prediksi.csv", "text/csv",
                           width="stretch")

# ---------- TAB 3 ----------
with tab3:
    with st.container(border=True):
        st.markdown("### 🎯 Evaluasi Model yang Digunakan Aplikasi")
        st.caption(f"{BEST} + kalibrasi sigmoid • probabilitas dan keputusan dari model yang sama • "
                   f"test holdout {N_TEST} pelanggan.")
        st.dataframe(pd.DataFrame([
            {"Konfigurasi": f"Aplikasi (ambang {THRESHOLD:.2f}, dipilih di train)", **MET},
            {"Konfigurasi": "Kalibrasi (ambang default 0.50)", **DEPLOY["metrics_at_0_5"]},
        ]), width="stretch", hide_index=True)
        show_confusion_matrix(MET)
        st.info(f"Dengan ambang {THRESHOLD:.0%}, aplikasi menangkap {MET['TP']} dari "
                f"{MET['TP'] + MET['FN']} pelanggan churn dan melewatkan {MET['FN']}. "
                f"Ada {MET['FP']} alarm keliru. Precision {MET['Precision']:.2%} dan "
                f"recall {MET['Recall']:.2%} menunjukkan trade-off penawaran retensi.")
        with st.expander("Kalibrasi dan pemilihan ambang"):
            st.write("Kalibrasi sigmoid menyesuaikan probabilitas model inti. "
                     "Ambang keputusan dipilih dari grid 0,10–0,60 (langkah 0,01) "
                     "berdasarkan F1 maksimum prediksi out-of-fold data training, "
                     "dengan kalibrasi 5-fold di dalam setiap training fold.")
            st.caption(f"OOF-F1 untuk tuning ambang: {DEPLOY['oof_tuning_f1']:.4f}. "
                       "Angka ini adalah skor tuning, bukan estimasi generalisasi yang independen; "
                       "hyperparameter model inti juga telah dipilih pada data train. "
                       "Semua keputusan tuning tidak memakai label test.")
            st.write(f"Brier test sebelum/sesudah kalibrasi: {CALINFO['brier_base']:.4f} / "
                     f"{CALINFO['brier_cal']:.4f}. Lebih kecil berarti kesalahan probabilitas lebih rendah.")
            st.dataframe(pd.DataFrame(CALINFO["reliability_test"]).rename(columns={
                "band": "Band risiko", "n": "Pelanggan", "mean_pred": "Rata-rata probabilitas",
                "empirical": "Proporsi churn aktual",
            }), width="stretch", hide_index=True)

    with st.container(border=True):
        st.markdown("### 🏆 Perbandingan Tiga Model Inti (Test Set)")
        st.caption("Model inti dievaluasi tanpa kalibrasi, dengan ambang default 0,50. "
                   "Tabel diurutkan berdasarkan CV-F1 untuk seleksi pada data train; "
                   "angka ini berbeda dari konfigurasi aplikasi terkalibrasi di atas.")
        with st.expander("📖 Rumus metrik", expanded=False):
            st.markdown("Label Confusion Matrix: churn = 1, tidak churn = 0.")
            st.markdown(
                "| Metrik | Rumus | Arti |\n"
                "|---|---|---|\n"
                "| TP | TP | Prediksi churn (1), realita churn (1) ✅ |\n"
                "| TN | TN | Prediksi tidak churn (0), aktual tidak churn (0) ✅ |\n"
                "| FP | FP | Prediksi churn (1), aktual tidak churn (0) — alarm keliru |\n"
                "| FN | FN | Prediksi tidak churn (0), aktual churn (1) — churn terlewat |\n"
                "| Accuracy | (TP+TN)/total | Tebakan benar / total |\n"
                "| Precision | TP/(TP+FP) | Dari yang dibilang churn, berapa yang benar |\n"
                "| Recall | TP/(TP+FN) | Dari churn asli, berapa yang ketangkap |\n"
                "| F1 | 2×P×R/(P+R) | Rata-rata adil Precision + Recall |\n"
                "| ROC-AUC | luas kurva ROC | 0.5 = acak, 1.0 = sempurna |")
            st.divider()
            st.markdown("**📘 F1-Score**")
            st.markdown(
                "**Kepanjangan:** F1 = *F-Measure / F-Score* (rata-rata harmonik Precision dan Recall).\n\n"
                "**Rumus:** `F1 = 2 × (Precision × Recall) / (Precision + Recall)`.\n\n"
                "**Definisi:** F1 mengukur keseimbangan antara Precision (ketepatan saat memprediksi churn) "
                "dan Recall (kemampuan menangkap semua churn asli). Nilainya 0–1: makin dekat 1 makin bagus. "
                "F1 penting karena dataset churn itu tidak seimbang (yang churn lebih sedikit) — "
                "akurasi saja bisa menipu, sedangkan F1 menghukum model yang hanya bagus di satu sisi. "
                "Contoh di proyek ini: model dengan Recall tinggi tapi Precision rendah tetap butuh F1 "
                "untuk memastikan promo retensi tidak terlalu banyak salah sasaran."
            )
            st.markdown("**📗 CV-F1**")
            st.markdown(
                "**Kepanjangan:** CV-F1 = *Cross-Validated F1* (rata-rata F1 dari validasi silang).\n\n"
                "**Cara hitung:** data latih dibagi 5 fold (lipatan). Model dilatih di 4 fold, diuji di 1 fold, "
                "diulang 5 kali sampai semua fold pernah jadi data uji. CV-F1 = rata-rata F1 dari kelima fold.\n\n"
                "**Definisi:** CV-F1 merangkum performa pada lima validation fold data training. "
                "Model inti dipilih berdasarkan CV-F1 tertinggi. Variasi antar-fold membantu membaca "
                "stabilitas hasil, tetapi tidak menjamin performa pada seluruh pelanggan baru."
            )
            st.markdown("**📙 ROC-AUC**")
            st.markdown(
                "**Kepanjangan:** ROC-AUC = *Receiver Operating Characteristic – Area Under the Curve* "
                "(luas area di bawah kurva ROC).\n\n"
                "**Cara baca:** kurva ROC memetakan *True Positive Rate* (Recall) vs *False Positive Rate* "
                "(FP / (FP+TN)) di semua threshold probabilitas. AUC = luas di bawah kurva itu, nilainya 0–1.\n\n"
                "**Definisi:** ROC-AUC mengukur kemampuan model membedakan pelanggan churn vs tidak churn "
                "di semua level threshold, bukan cuma di threshold 0.5. Nilai 0.5 = tebakan acak, "
                "0.7–0.8 = cukup baik, 0.8–0.9 = baik, 1.0 = sempurna. Di proyek ini ROC-AUC dipakai sebagai "
                "pembanding kualitas diskriminasi antar model: makin tinggi, makin andal model memilah "
                "pelanggan berisiko tanpa tergantung satu titik cutoff."
            )
        if CMP is not None:
            _cmp_show = CMP.copy()
            _cmp_show.index = _cmp_show.index + 1
            st.dataframe(_cmp_show, width="stretch")
            cm_model = st.selectbox("Confusion matrix model inti", CMP["Model"].tolist())
            b = CMP[CMP["Model"] == cm_model].iloc[0]
            st.markdown(f"**Confusion matrix — {cm_model} (test {N_TEST} data):**")
            show_confusion_matrix(b)
            fig, ax = plt.subplots(figsize=(6.5, 2.6))
            plot_df = CMP.set_index("Model")[["Accuracy", "Precision", "Recall", "F1"]]
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
                f"**Kenapa {BEST} dipilih?** CV-F1 tertinggi ({selected['CV_F1']:.4f}) "
                "pada data train. Pada test model inti, "
                f"{top_recall['Model']} memiliki recall tertinggi ({top_recall['Recall']:.2%}), "
                f"sedangkan {top_accuracy['Model']} memiliki akurasi tertinggi "
                f"({top_accuracy['Accuracy']:.2%}). Pemilihan model tidak diubah berdasarkan test.")
            if {"Train_F1", "CV_TRAIN_F1", "CV_F1_STD"}.issubset(CMP.columns):
                st.markdown("**Analisis train–validation–test:**")
                st.dataframe(CMP[["Model", "Train_F1", "CV_TRAIN_F1", "CV_F1", "CV_F1_STD", "F1"]],
                             width="stretch", hide_index=True)
                largest_gap = CMP.loc[(CMP["Train_F1"] - CMP["F1"]).idxmax()]
                st.caption(f"Gap F1 train–test terbesar: {largest_gap['Model']} "
                           f"({largest_gap['Train_F1']:.4f} vs {largest_gap['F1']:.4f}). "
                           "Gap besar merupakan indikasi overfitting; bandingkan juga skor validation.")
            if CVDET is not None:
                st.markdown("**Hasil validasi tiap session (F1):**")
                st.caption("Lima session hanya membagi data train menjadi train fold dan validation fold. "
                           "Holdout test 20% tidak termasuk dalam lima fold ini.")
                _cv_show = CVDET.rename(columns={"Fold": "Session"})
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
                    ax0.plot(d["Fold"], d["F1"], marker="o", label=m, linewidth=2.2, markersize=4)
                ax0.set_xticks([1, 2, 3, 4, 5])
                ax0.set_xlabel("Session", fontsize=9)
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
        st.markdown("### ⭐ Interpretasi Model Inti")
        st.caption("Bobot berikut berasal dari model inti sebelum kalibrasi. "
                   "Koefisien positif/negatif menunjukkan hubungan dengan log-odds churn "
                   "dengan fitur lain tetap; bukan bukti sebab-akibat. Besar koefisien "
                   "numerik terstandardisasi dan dummy kategori tidak langsung sebanding.")
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
                ax2.set_xlabel("Koefisien (+ / − hubungan dengan log-odds churn)")
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
            st.caption(f"Tidak bisa tampilkan importance: {e}")

    with st.expander("Dataset dan keterbatasan aplikasi"):
        st.markdown("Sumber: [IBM Telco Customer Churn di Kaggle]"
                    "(https://www.kaggle.com/datasets/blastchar/telco-customer-churn). "
                    "CSV mentah berisi 7.043 pelanggan. Cohort training menggunakan 7.032 "
                    "catatan lengkap setelah 11 TotalCharges kosong dihapus.")
        st.write("customerID tidak dipakai sebagai fitur. TotalCharges tidak diminta agar input aplikasi "
                 "lebih sederhana. Nilainya berkorelasi dengan tenure, tetapi bukan selalu sama "
                 "dengan tagihan bulanan dikali tenure. Keuntungan penghapusan fitur belum diuji "
                 "dengan eksperimen ablation.")
        st.write("Dataset ini tidak mencakup seluruh kondisi pelanggan/operator saat ini. "
                 "TETAP berarti diprediksi tidak churn, bukan jaminan loyalitas. "
                 "Rekomendasi retensi adalah aturan contoh yang perlu diuji efektivitasnya.")

st.markdown("<div class='footer'>Kelompok 12 • Muhamad Akhdan Ramadhan (J0404241102) • "
            "Thevan Erlangga (J0404241073) • Fachri Abyasa Tarid (J0404241136)</div>",
            unsafe_allow_html=True)
