"""Aplikasi Prediksi Customer Churn - Telco (UI Modern)
Pipeline: preprocessing + model dalam 1 file model_churn.pkl
"""
from pathlib import Path
import joblib
import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

BASE = Path(__file__).parent

# --- Load artefak ---
pipe = joblib.load(BASE / "model_churn.pkl")
try:
    with open(BASE / "model_info.json") as f:
        INFO = json.load(f)
except FileNotFoundError:
    INFO = {}
try:
    CMP = pd.read_csv(BASE / "hasil_perbandingan.csv")
except FileNotFoundError:
    CMP = None
try:
    CVDET = pd.read_csv(BASE / "cv_detail.csv")
except FileNotFoundError:
    CVDET = None

st.set_page_config(
    page_title="Prediksi Customer Churn - Telco",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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
MET = INFO.get("metrics", {}) if INFO else {}
CVF1 = MET.get("CV_F1", "-")
ACC = MET.get("Accuracy", "-")
AUC = MET.get("ROC_AUC", "-")
REC = MET.get("Recall", "-")

def fmt(x):
    return f"{x:.4f}" if isinstance(x, float) else str(x)

# ---------- HERO ----------
st.markdown(
    f"""<div class="hero">
    <h1>📡 Prediksi Customer Churn — Telco</h1>
    <p>Uji coba pelanggan akan <b>churn</b> atau <b>setia</b>, lengkap dengan probabilitas,
    rekomendasi retensi, prediksi massal CSV, dan transparansi model.</p>
    <span class="pill">🏆 Model: {BEST}</span>
    <span class="pill">🎯 CV-F1: {fmt(CVF1)}</span>
    <span class="pill">📈 ROC-AUC: {fmt(AUC)}</span>
    <span class="pill">🗂️ 7032 data • 18 fitur</span>
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
                f"<div class='sub'>Test set 1407 data</div></div>", unsafe_allow_html=True)
with k3:
    st.markdown(f"<div class='kpi'><div class='label'>📈 ROC-AUC</div>"
                f"<div class='value'>{fmt(AUC)}</div>"
                f"<div class='sub'>0.5 = acak, 1.0 = sempurna</div></div>", unsafe_allow_html=True)
with k4:
    st.markdown("<div class='kpi'><div class='label'>🗂️ Dataset</div>"
                "<div class='value'>7032</div>"
                "<div class='sub'>Telco-Customer-Churn • bersih</div></div>", unsafe_allow_html=True)

with st.expander("ℹ️ Detail Info Model", expanded=False):
    c_a, c_b = st.columns([1, 2])
    with c_a:
        st.write(f"**Model terbaik:** `{BEST}`")
        st.caption("Dipilih berdasarkan CV-F1 tertinggi (5-fold). Dalam bisnis, "
                   "kehilangan pelanggan (FN) lebih mahal dari promo salah sasaran (FP).")
        if MET:
            st.json(MET)
    with c_b:
        st.caption("Dataset: Telco-Customer-Churn — 7032 baris bersih, 18 fitur mentah. "
                   "Pipeline = ColumnTransformer + Classifier dalam 1 file `model_churn.pkl` "
                   "(tanpa leakage, tanpa scaling manual).")

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
            _ml_opts = ["Yes", "No", "No phone service"]
            _ml_lock = (PhoneService == "No")
            MultipleLines = st.selectbox("Multiple Lines", _ml_opts,
                index=2 if _ml_lock else 0, disabled=_ml_lock)
        with c2:
            InternetService = st.selectbox("Internet", ["Fiber optic", "DSL", "No"])
            _lock = (InternetService == "No")
            _opts = ["Yes", "No", "No internet service"]
            OnlineSecurity = st.selectbox("Online Security", _opts, index=2 if _lock else 0, disabled=_lock)
            OnlineBackup = st.selectbox("Online Backup", _opts, index=2 if _lock else 0, disabled=_lock)
            DeviceProtection = st.selectbox("Device Protection", _opts, index=2 if _lock else 0, disabled=_lock)
            TechSupport = st.selectbox("Tech Support", _opts, index=2 if _lock else 0, disabled=_lock)
            StreamingTV = st.selectbox("Streaming TV", _opts, index=2 if _lock else 0, disabled=_lock)
            StreamingMovies = st.selectbox("Streaming Movies", _opts, index=2 if _lock else 0, disabled=_lock)
        with c3:
            Contract = st.selectbox("Kontrak", ["Month-to-month", "One year", "Two year"])
            PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
            PaymentMethod = st.selectbox("Metode Bayar", ["Electronic check", "Mailed check",
                "Bank transfer (automatic)", "Credit card (automatic)"])
            MonthlyCharges = st.number_input("Monthly Charges ($)", 0.0, 120.0, 70.0, step=1.0,
                format="%.2f",
                help="Maks 120 mengikuti data latih (maks 118,75). Isi tagihan aktual dari billing.")
            if InternetService == "No" and MonthlyCharges > 35:
                st.warning("⚠️ Tidak wajar: tanpa internet tagihan normalnya ~20. Cek lagi input.")
            elif InternetService == "DSL" and MonthlyCharges > 85:
                st.warning("⚠️ Tidak wajar: DSL normalnya di bawah 85. Cek lagi input.")
            elif InternetService == "Fiber optic" and MonthlyCharges < 25:
                st.warning("⚠️ Tidak wajar: fiber normalnya di atas 25. Cek lagi input.")

        b1, b2, b3 = st.columns([1, 2, 1])
        with b2:
            predict = st.button("🚀 Prediksi Sekarang", type="primary", use_container_width=True)

    if predict:
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
        pred = pipe.predict(row)[0]
        prob = float(pipe.predict_proba(row)[0][1])

        if prob < 0.30:
            lvl, cls = "🟢 RISIKO RENDAH", "low"
        elif prob < 0.60:
            lvl, cls = "🟡 RISIKO SEDANG", "mid"
        else:
            lvl, cls = "🔴 RISIKO TINGGI", "high"

        st.markdown(
            f"""<div class="result {cls}">
            <span class="badge {cls}">{lvl}</span>
            <div class="prob">{prob*100:.2f}%</div>
            <div style="opacity:.85">Keputusan model: <b>{'CHURN' if pred == 1 else 'TETAP'}</b>
            • Probabilitas churn dari <code>predict_proba</code></div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.progress(prob)

        st.markdown("### 💡 Rekomendasi Retensi")
        recs = []
        if Contract == "Month-to-month":
            recs.append(("📝 Kontrak", "Tawarkan upgrade kontrak 1/2 tahun + diskon."))
        if InternetService == "Fiber optic" and MonthlyCharges > 75:
            recs.append(("💸 Tagihan", "Tagihan fiber tinggi — tawarkan bundling / cashback."))
        if PaymentMethod == "Electronic check":
            recs.append(("💳 Pembayaran", "Migrasi ke auto-pay (transfer/kartu) — churn lebih rendah."))
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
        f = st.file_uploader("Pilih file CSV", type="csv")
    if f:
        df = pd.read_csv(f)
        df_clean = df.drop(columns=["customerID", "Churn", "TotalCharges"], errors="ignore").copy()
        probs = pipe.predict_proba(df_clean)[:, 1]
        preds = pipe.predict(df_clean)
        out = df.copy().loc[df_clean.index]
        out["Prob_Churn"] = (probs * 100).round(2)
        out["Prediksi"] = ["CHURN" if p == 1 else "TETAP" for p in preds]
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

        st.dataframe(out.head(20), use_container_width=True)
        st.bar_chart(out["Prediksi"].value_counts())
        st.download_button("⬇️ Download Hasil (CSV)",
                           out.to_csv(index=False).encode(), "hasil_prediksi.csv", "text/csv",
                           use_container_width=True)

# ---------- TAB 3 ----------
with tab3:
    with st.container(border=True):
        st.markdown("### 🏆 Perbandingan Model (Test Set)")
        with st.expander("📖 Rumus metrik", expanded=False):
            st.markdown("Label Confusion Matrix: churn = 1, setia = 0.")
            st.markdown(
                "| Metrik | Rumus | Arti |\n"
                "|---|---|---|\n"
                "| TP | TP | Prediksi churn (1), realita churn (1) ✅ |\n"
                "| TN | TN | Prediksi setia (0), realita setia (0) ✅ |\n"
                "| FP | FP | Prediksi churn (1), realita setia (0) — salah tuduh |\n"
                "| FN | FN | Prediksi setia (0), realita churn (1) — lolos, paling rugi |\n"
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
                "**Definisi:** CV-F1 menunjukkan performa model yang stabil dan tidak kebetulan bagus di satu "
                "pembagian data saja. Inilah alasan model terbaik di proyek ini dipilih berdasarkan CV-F1 tertinggi, "
                "bukan sekadar akurasi test sekali jalan — supaya model terbukti konsisten di semua variasi data "
                "pelanggan."
            )
            st.markdown("**📙 ROC-AUC**")
            st.markdown(
                "**Kepanjangan:** ROC-AUC = *Receiver Operating Characteristic – Area Under the Curve* "
                "(luas area di bawah kurva ROC).\n\n"
                "**Cara baca:** kurva ROC memetakan *True Positive Rate* (Recall) vs *False Positive Rate* "
                "(FP / (FP+TN)) di semua threshold probabilitas. AUC = luas di bawah kurva itu, nilainya 0–1.\n\n"
                "**Definisi:** ROC-AUC mengukur kemampuan model membedakan pelanggan churn vs setia "
                "di semua level threshold, bukan cuma di threshold 0.5. Nilai 0.5 = tebakan acak, "
                "0.7–0.8 = cukup baik, 0.8–0.9 = baik, 1.0 = sempurna. Di proyek ini ROC-AUC dipakai sebagai "
                "pembanding kualitas diskriminasi antar model: makin tinggi, makin andal model memilah "
                "pelanggan berisiko tanpa tergantung satu titik cutoff."
            )
        if CMP is not None:
            _cmp_show = CMP.copy()
            _cmp_show.index = _cmp_show.index + 1
            st.dataframe(_cmp_show, use_container_width=True)
            try:
                b = CMP[CMP["Model"] == BEST].iloc[0]
                st.markdown(f"**Confusion matrix — {BEST} (test 1407 data):**")
                st.markdown(
                    f"""<div class="cm-grid">
                    <div class="cm-cell cm-tp"><span>TP • churn ketangkap</span><b>{int(b["TP"])}</b>
                    <span style="opacity:.7;font-size:.8rem">pred 1, real 1</span></div>
                    <div class="cm-cell cm-tn"><span>TN • setia benar</span><b>{int(b["TN"])}</b>
                    <span style="opacity:.7;font-size:.8rem">pred 0, real 0</span></div>
                    <div class="cm-cell cm-fp"><span>FP • salah tuduh</span><b>{int(b["FP"])}</b>
                    <span style="opacity:.7;font-size:.8rem">pred 1, real 0</span></div>
                    <div class="cm-cell cm-fn"><span>FN • lolos (rugi!)</span><b>{int(b["FN"])}</b>
                    <span style="opacity:.7;font-size:.8rem">pred 0, real 1</span></div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            except Exception:
                pass
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
            st.pyplot(fig, use_container_width=False)
            try:
                lr = CMP[CMP["Model"] == "LogisticRegression"].iloc[0]
                rf = CMP[CMP["Model"] == "RandomForest"].iloc[0]
                st.info(
                    f"**Kenapa {BEST} dipilih?** CV-F1 tertinggi ({lr['CV_F1']}), "
                    f"Recall {lr['Recall']} (miss {int(lr['FN'])} dari "
                    f"{int(lr['FN'] + lr['TP'])} churn), AUC {lr['ROC_AUC']}. "
                    f"RandomForest akurasi tertinggi ({rf['Accuracy']}) tapi miss {int(rf['FN'])} churn — "
                    "kehilangan pelanggan (FN) lebih mahal dari promo salah sasaran (FP).")
            except Exception:
                pass
            if CVDET is not None:
                st.markdown("**Hasil training tiap session (F1):**")
                _cv_show = CVDET.rename(columns={"Fold": "Session"})
                _cv_pivot = _cv_show.pivot(index="Session", columns="Model", values="F1").reset_index()
                _cv_pivot = _cv_pivot.rename(
                    columns={c: f"Nilai F1 {c}" for c in _cv_pivot.columns if c != "Session"})
                st.dataframe(_cv_pivot, use_container_width=True, hide_index=True)
                fig0, ax0 = plt.subplots(figsize=(6.5, 2.6))
                for m in CVDET["Model"].unique():
                    d = CVDET[CVDET["Model"] == m].sort_values("Fold")
                    ax0.plot(d["Fold"], d["F1"], marker="o", label=m, linewidth=2.2, markersize=4)
                ax0.set_xticks([1, 2, 3, 4, 5])
                ax0.set_xlabel("Session", fontsize=9)
                ax0.set_ylabel("F1", fontsize=9)
                ax0.tick_params(labelsize=8)
                ax0.legend(fontsize=7.5, frameon=False, loc="best")
                ax0.grid(alpha=.2)
                style_fig(fig0, ax0)
                plt.tight_layout()
                st.pyplot(fig0)

    with st.container(border=True):
        st.markdown("### ⭐ Fitur Paling Berpengaruh")
        st.caption("Merah = pendorong churn (+), hijau = penahan churn (−) untuk LogisticRegression.")
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
                ax2.set_xlabel("Bobot (+ pendorong churn, - penahan)")
                ax2.grid(axis="x", alpha=.2)
                style_fig(fig2, ax2)
                plt.tight_layout()
                st.pyplot(fig2)
                st.dataframe(top.drop(columns="Abs"), use_container_width=True)
            else:
                imp = pd.DataFrame({"Fitur": clean, "Importance": clf.feature_importances_})
                top = imp.sort_values("Importance", ascending=False).head(15).sort_values("Importance")
                fig2, ax2 = plt.subplots(figsize=(8, 5))
                ax2.barh(top["Fitur"], top["Importance"], color="#7C3AED", height=.6)
                ax2.set_xlabel("Importance")
                style_fig(fig2, ax2)
                plt.tight_layout()
                st.pyplot(fig2)
                st.dataframe(top, use_container_width=True)
        except Exception as e:
            st.caption(f"Tidak bisa tampilkan importance: {e}")
