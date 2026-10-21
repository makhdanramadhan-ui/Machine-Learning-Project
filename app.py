"""Aplikasi Prediksi Customer Churn - Telco
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

import ui
from prediction import (
    InputValidationError, example_customers, input_schema, input_notes,
    predict_customers, risk_levels, high_risk_boundary,
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

# ---------- Kepala lembar ----------
head_left, head_right = st.columns([8, 2], gap="medium", vertical_alignment="bottom")
with head_left:
    st.markdown(
        '<div class="app-title">Prediksi Customer Churn — Telco</div>'
        '<p class="app-sub">Perkirakan churn pelanggan telco dari 18 fitur pelanggan, '
        'dengan ambang keputusan 0,32 yang dipilih dari F1 out-of-fold data latih.</p>',
        unsafe_allow_html=True,
    )
with head_right:
    st.segmented_control("Tema", ["Terang", "Gelap"], key="tema",
                         label_visibility="collapsed", width="stretch")

TEMA = st.session_state.get("tema", "Terang")
TOK = ui.THEMES[TEMA]
st.markdown(ui.build_css(TEMA), unsafe_allow_html=True)


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


@st.cache_data
def load_charge_reference(dataset_stamp):
    """Acuan tagihan dari training set, bukan tarif pasar atau aturan model."""
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
BASE_MET = INFO.get("metrics", {})
MET = DEPLOY["metrics"]
CVF1 = BASE_MET.get("CV_F1", "-")
ACC = MET.get("Accuracy", "-")
AUC = MET.get("ROC_AUC", "-")
REC = MET.get("Recall", "-")
N_TEST = DEPLOY["n_test"]
N_DATA = DEPLOY["n_train"] + N_TEST


def count_text(value):
    return f"{int(value):,}".replace(",", ".")


def dollar_text(value):
    return r"\$" + f"{value:.2f}".replace(".", ",")


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


# ---------- Grafik matplotlib ----------
def style_fig(fig, ax_or_axes, tok=None):
    """Sumbu mengikuti palet lembar: hairline, tanpa bingkai atas-kanan."""
    tok = tok or TOK
    axes = ax_or_axes if isinstance(ax_or_axes, (list, tuple)) else [ax_or_axes]
    for ax in axes:
        ax.set_facecolor("none")
        ax.tick_params(colors=tok["muted"], labelsize=8, length=3, color=tok["rule"])
        ax.yaxis.label.set_color(tok["ink"])
        ax.xaxis.label.set_color(tok["ink"])
        ax.title.set_color(tok["ink"])
        for spine in ax.spines.values():
            spine.set_color(tok["rule"])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.patch.set_facecolor("none")


# ---------- Title block: identitas model ----------
st.markdown(
    ui.title_block(
        [
            ("Model", BEST_LABEL, "sm"),
            ("Ambang", ui.fmt_num(THRESHOLD)),
            ("CV-F1", ui.fmt_num(CVF1, 4)),
            ("Akurasi", ui.fmt_num(ACC, 4)),
            ("Precision", ui.fmt_num(MET.get("Precision", 0), 4)),
            ("Recall", ui.fmt_num(REC, 4)),
            ("F1", ui.fmt_num(MET.get("F1", 0), 4)),
            ("ROC-AUC", ui.fmt_num(AUC, 4)),
            ("Brier", ui.fmt_num(MET.get("Brier", 0), 4)),
        ],
        strip=[
            ("Data latih", count_text(DEPLOY["n_train"])),
            ("Data uji", count_text(N_TEST)),
            ("Fitur", str(DEPLOY["n_features"])),
            ("Kalibrasi", "Sigmoid, 5 fold"),
            ("Sklearn", DEPLOY["sklearn_version"]),
            ("SHA-256 model", DEPLOY["model_sha256"][:12] + "…"),
        ],
    ),
    unsafe_allow_html=True,
)

with st.expander("Tentang model dan cara membaca hasil", expanded=False):
    c_a, c_b = st.columns([1, 2])
    with c_a:
        st.markdown(f"**Model yang dipakai: {BEST_LABEL}**")
        st.caption("Model ini mendapat rata-rata F1 tertinggi pada validasi silang lima fold. "
                   "Akurasi, recall, dan AUC di atas dihitung setelah kalibrasi, sesuai model "
                   "yang dipakai aplikasi.")
        if MET:
            st.json(MET)
    with c_b:
        st.caption(f"Model memakai {DEPLOY['n_features']} informasi pelanggan. Angka dan kategori "
                   "diproses otomatis sebelum diprediksi. Kalibrasi sigmoid menyesuaikan "
                   "probabilitas dan dilatih hanya dengan data training.")
        st.write(f"**Aturan keputusan:** CHURN jika probabilitas ≥ {THRESHOLD:.0%}; "
                 "TETAP jika di bawah ambang tersebut.")
        st.caption("Ambang dipilih dari hasil validasi data training. Data testing dipakai untuk "
                   "mengukur hasil akhirnya. Label CHURN menunjukkan risiko yang melewati ambang, "
                   "bukan kepastian.")

tab1, tab2, tab3, tab4 = st.tabs([
    "Prediksi Single", "Prediksi Batch (CSV)", "Dashboard & Model", "EDA & Dokumentasi",
])

# ---------- TAB 1: Prediksi single ----------
with tab1:
    with st.container(border=True):
        st.markdown(ui.section("Data Pelanggan", "user",
                               "Isi data pelanggan, lalu klik Prediksi. Pilihan layanan tambahan "
                               "menyesuaikan layanan telepon dan internet yang digunakan."),
                    unsafe_allow_html=True)
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
            charge_reference = load_charge_reference(
                (BASE / "Telco-Customer-Churn.csv").stat().st_mtime_ns)[InternetService]
            service_label = "tanpa internet" if InternetService == "No" else option_label(InternetService)
            st.markdown(f"**Acuan tagihan {service_label}**")
            st.caption(f"Rentang umum: {dollar_text(charge_reference['q1'])}–"
                       f"{dollar_text(charge_reference['q3'])}/bulan (50% data training). "
                       f"Median: {dollar_text(charge_reference['median'])}.")
            st.caption(f"Rentang yang tercatat: {dollar_text(charge_reference['min'])}–"
                       f"{dollar_text(charge_reference['max'])}. Ini total tagihan termasuk "
                       "telepon dan layanan tambahan yang dipakai, bukan tarif internet saja.")
            if MonthlyCharges < charge_reference["min"] or MonthlyCharges > charge_reference["max"]:
                direction = "lebih rendah" if MonthlyCharges < charge_reference["min"] else "lebih tinggi"
                st.warning(f"Tagihan {dollar_text(MonthlyCharges)} {direction} dari rentang {service_label} "
                           "pada data training. Periksa lagi nominal dan layanan yang dipilih. "
                           "Prediksi tetap bisa dijalankan; acuan ini bukan daftar harga resmi.")

        b1, b2, b3 = st.columns([1, 2, 1])
        with b2:
            predict = st.button("Prediksi", type="primary", width="stretch")

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
        st.info("Input telah berubah. Klik Prediksi untuk memperbarui hasil.")
    if result and result["input"] == fingerprint:
        prob, pred = result["prob"], result["pred"]
        for note in input_notes(row):
            st.info(note)

        level = risk_levels([prob], THRESHOLD)[0]
        st.markdown(
            '<div class="verdict">'
            f'<div class="verdict-head">{ui.risk_chip(level)}'
            '<span class="verdict-decision">Keputusan model: '
            f'<b>{"CHURN" if pred == 1 else "TETAP"}</b></span></div>'
            f'<div class="verdict-figure">{ui.fmt_num(prob * 100)}<span class="unit">%</span></div>'
            '<div class="verdict-sub">Probabilitas churn terkalibrasi</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(ui.calibrated_scale(prob, THRESHOLD, HIGH_BOUNDARY), unsafe_allow_html=True)
        st.caption(f"Ambang keputusan {THRESHOLD:.0%}. Risiko rendah: < {THRESHOLD:.0%}; "
                   f"sedang: {THRESHOLD:.0%}–< {HIGH_BOUNDARY:.0%}; tinggi: ≥ {HIGH_BOUNDARY:.0%}. "
                   "Kategori risiko membantu membaca hasil; model tetap memprediksi churn atau tidak churn.")
        st.caption("TETAP berarti pelanggan diprediksi tidak churn. Probabilitas sudah disesuaikan "
                   "dengan kalibrasi sigmoid; detail pengujiannya ada di Dashboard & Model.")

        st.markdown(ui.section("Saran untuk Mempertahankan Pelanggan", "target",
                               "Saran berikut disesuaikan dengan data yang diisi. Efektivitasnya "
                               "perlu diuji, karena model belum mengukur dampak penawaran terhadap churn."),
                    unsafe_allow_html=True)
        recs = []
        if Contract == "Month-to-month":
            recs.append(("doc", "Kontrak", "Pertimbangkan penawaran kontrak satu atau dua tahun dengan diskon."))
        if InternetService == "Fiber optic" and MonthlyCharges > 75:
            recs.append(("layers", "Tagihan", "Tinjau paket fiber yang digunakan dan tawarkan paket yang lebih sesuai."))
        if PaymentMethod == "Electronic check":
            recs.append(("check", "Pembayaran", "Tawarkan pembayaran otomatis melalui transfer atau kartu."))
        if TechSupport in ("No", "No internet service") and InternetService != "No":
            recs.append(("flag", "Bantuan teknis", "Pertimbangkan masa coba layanan bantuan teknis."))
        if tenure < 6:
            recs.append(("user", "Pelanggan baru", "Bantu pelanggan memahami layanan dan tanyakan pengalamannya setelah bulan pertama."))
        if not recs:
            recs.append(("target", "Layanan", "Jaga kualitas layanan dan pertimbangkan penghargaan untuk pelanggan lama."))
        st.markdown("".join(ui.recommendation(n, label, t) for n, label, t in recs),
                    unsafe_allow_html=True)

# ---------- TAB 2: Prediksi batch ----------
with tab2:
    with st.container(border=True):
        st.markdown(ui.section("Unggah CSV untuk Prediksi Massal", "upload",
                               "Gunakan template di bawah atau CSV dengan kolom yang sama. Kolom "
                               "`customerID`, `Churn`, dan `TotalCharges` boleh disertakan, "
                               "tetapi tidak dipakai untuk prediksi."),
                    unsafe_allow_html=True)
        st.download_button("Unduh template CSV", example_customers().to_csv(index=False).encode("utf-8"),
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

        st.markdown(ui.summary_strip([
            ("Total baris", count_text(len(out))),
            ("Prediksi churn", count_text(churn_n)),
            ("Persentase churn", ui.fmt_num(rate) + "%"),
        ]), unsafe_allow_html=True)
        st.caption(f"Ambang: {THRESHOLD:.0%}. Kolom Prob_Churn berisi probabilitas dalam persen. "
                   f"Menampilkan {min(20, len(out))} dari {count_text(len(out))} pelanggan; "
                   "unduhan memuat semua hasil.")
        st.dataframe(out.head(20), width="stretch", hide_index=True)

        fig_dist, ax_dist = plt.subplots(figsize=(6.5, 2.1))
        counts = out["Prediksi"].value_counts().reindex(["TETAP", "CHURN"]).fillna(0)
        ax_dist.barh(counts.index, counts.values,
                     color=[TOK["ramp6"], TOK["accent"]], height=.55, edgecolor="none")
        ax_dist.set_xlabel("Pelanggan", fontsize=9)
        ax_dist.set_xlim(0, max(counts.values.max(), 1) * 1.18)
        for i, value in enumerate(counts.values):
            ax_dist.text(value + max(counts.values.max(), 1) * 0.02, i, f"{int(value):,}".replace(",", "."),
                         va="center", fontsize=8, color=TOK["muted"])
        style_fig(fig_dist, ax_dist)
        plt.tight_layout()
        st.pyplot(fig_dist, width="stretch")
        plt.close(fig_dist)

        st.download_button("Unduh hasil (CSV)",
                           out.to_csv(index=False).encode(), "hasil_prediksi.csv", "text/csv",
                           width="stretch")

# ---------- TAB 3: Dashboard & model ----------
with tab3:
    with st.container(border=True):
        st.markdown(ui.section("Hasil Pengujian Model Aplikasi", "chart",
                               f"{BEST_LABEL} dengan kalibrasi sigmoid, diuji pada "
                               f"{count_text(N_TEST)} pelanggan yang tidak digunakan untuk "
                               "melatih model."),
                    unsafe_allow_html=True)
        st.dataframe(pd.DataFrame([
            {"Konfigurasi": f"Aplikasi — ambang {THRESHOLD:.2f}", **MET},
            {"Konfigurasi": "Pembanding — ambang 0,50", **DEPLOY["metrics_at_0_5"]},
        ]), width="stretch", hide_index=True)
        st.markdown(ui.confusion_matrix(MET), unsafe_allow_html=True)
        st.caption(f"Dari {MET['TP'] + MET['FN']} pelanggan yang benar-benar churn, "
                   f"{MET['TP']} berhasil terdeteksi dan {MET['FN']} terlewat. "
                   f"{MET['FP']} pelanggan yang tidak churn juga ditandai CHURN. "
                   "Menurunkan ambang membantu mendeteksi lebih banyak churn, tetapi bisa menambah "
                   "prediksi yang keliru.")
        with st.expander(f"Mengapa ambangnya {THRESHOLD:.0%}?", expanded=False):
            st.write(f"Ambang dicoba dari 0,10 sampai 0,60 dengan selisih 0,01. "
                     f"Ambang {THRESHOLD:.2f} memberi F1 tertinggi pada validasi data training. "
                     "Artinya, model memberi label CHURN ketika probabilitas mencapai ambang ini, "
                     "meskipun masih di bawah 50%.")
            st.caption("Prediksi validasi dibuat dengan lima fold: setiap bagian diprediksi oleh "
                       "model yang dilatih pada bagian lainnya, dengan kalibrasi di dalam proses "
                       f"itu. F1 untuk memilih ambang: {DEPLOY['oof_tuning_f1']:.4f}. Skor ini dipakai "
                       "untuk memilih pengaturan, bukan hasil pengujian akhir.")
            st.write(f"Kalibrasi sigmoid menyesuaikan probabilitas model. Pada data testing, Brier "
                     f"score turun dari {CALINFO['brier_base']:.4f} menjadi {CALINFO['brier_cal']:.4f}. "
                     "Semakin kecil Brier, semakin kecil kesalahan probabilitasnya.")
            st.dataframe(pd.DataFrame(CALINFO["reliability_test"]).rename(columns={
                "band": "Kategori risiko", "n": "Pelanggan", "mean_pred": "Rata-rata probabilitas",
                "empirical": "Proporsi churn aktual",
            }).replace({"Kategori risiko": {"LOW": "Rendah", "MID": "Sedang", "HIGH": "Tinggi"}}),
                         width="stretch", hide_index=True)
            st.caption("Tabel membandingkan rata-rata probabilitas dengan proporsi pelanggan yang "
                       "benar-benar churn pada setiap kategori risiko. Kedua kolom memakai skala 0–1.")

    with st.container(border=True):
        st.markdown(ui.section("Perbandingan Tiga Model", "layers",
                               "Ketiga model ini diuji sebelum kalibrasi, dengan ambang 50%. Model "
                               "dipilih berdasarkan CV-F1 data training, bukan akurasi testing "
                               "tertinggi. Hasil setelah kalibrasi ada pada tabel aplikasi di atas."),
                    unsafe_allow_html=True)
        with st.expander("Cara membaca metrik"):
            st.markdown(
                "| Metrik | Rumus | Arti |\n"
                "|---|---|---|\n"
                "| TP | TP | Diprediksi churn dan memang churn |\n"
                "| TN | TN | Prediksi tidak churn (0), aktual tidak churn (0) |\n"
                "| FP | FP | Prediksi churn (1), aktual tidak churn (0) — alarm keliru |\n"
                "| FN | FN | Prediksi tidak churn (0), aktual churn (1) — churn terlewat |\n"
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
                       "pada berbagai ambang. Kurva ROC membandingkan recall dengan false positive "
                       "rate `FP/(FP+TN)`. Nilai 0,5 setara urutan acak.")

        if CMP is not None:
            _cmp_show = CMP.copy()
            _cmp_show["Model"] = _cmp_show["Model"].replace(MODEL_NAMES)
            _cmp_show.index = _cmp_show.index + 1
            st.dataframe(_cmp_show, width="stretch")
            cm_model = st.selectbox("Pilih model untuk melihat confusion matrix", CMP["Model"].tolist(),
                                    format_func=lambda name: MODEL_NAMES.get(name, name))
            b = CMP[CMP["Model"] == cm_model].iloc[0]
            st.markdown(f"**Confusion matrix — {MODEL_NAMES.get(cm_model, cm_model)} "
                        f"({count_text(N_TEST)} pelanggan testing)**")
            st.markdown(ui.confusion_matrix(b), unsafe_allow_html=True)

            fig, ax = plt.subplots(figsize=(6.5, 2.6))
            plot_df = CMP.set_index("Model")[["Accuracy", "Precision", "Recall", "F1"]]
            plot_df = plot_df.rename(index=MODEL_NAMES)
            colors = [TOK["accent"] if name == BEST_LABEL else TOK["ramp6"]
                      for name in plot_df.index]
            plot_df.plot(kind="barh", ax=ax, color=colors)
            ax.set_xlabel("Skor", fontsize=9)
            ax.tick_params(labelsize=8)
            leg = ax.legend(fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.22),
                            ncol=4, frameon=False, handlelength=1.2, handletextpad=0.4,
                            columnspacing=1.0)
            for text in leg.get_texts():
                text.set_color(TOK["muted"])
            style_fig(fig, ax)
            plt.tight_layout()
            st.pyplot(fig, width="stretch")
            plt.close(fig)

            selected = CMP[CMP["Model"] == BEST].iloc[0]
            top_recall = CMP.loc[CMP["Recall"].idxmax()]
            top_accuracy = CMP.loc[CMP["Accuracy"].idxmax()]
            st.info(
                f"**Mengapa {BEST_LABEL}?** Model ini mendapat CV-F1 tertinggi "
                f"({selected['CV_F1']:.4f}) pada data training. Saat diuji sebelum kalibrasi, "
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

                fig0, ax0 = plt.subplots(figsize=(6.5, 2.6))
                for m in CVDET["Model"].unique():
                    d = CVDET[CVDET["Model"] == m].sort_values("Fold")
                    ax0.plot(d["Fold"], d["F1"], marker="o", label=MODEL_NAMES.get(m, m),
                             linewidth=2, markersize=4,
                             color=TOK["accent"] if m == BEST else TOK["ramp6"])
                ax0.set_xticks([1, 2, 3, 4, 5])
                ax0.set_xlabel("Sesi validasi", fontsize=9)
                ax0.set_ylabel("F1", fontsize=9)
                ax0.tick_params(labelsize=8)
                ax0.legend(fontsize=8, frameon=False, loc="best")
                for text in ax0.get_legend().get_texts():
                    text.set_color(TOK["muted"])
                ax0.grid(axis="y", alpha=.25, color=TOK["rule"])
                style_fig(fig0, ax0)
                plt.tight_layout()
                st.pyplot(fig0, width="stretch")
                plt.close(fig0)

    with st.container(border=True):
        st.markdown(ui.section("Hubungan Fitur dengan Prediksi", "linechart",
                               "Grafik ini menampilkan koefisien model sebelum kalibrasi. Panjang "
                               "batang ke kanan menunjukkan hubungan positif dengan churn, ke kiri "
                               "hubungan negatif, ketika fitur lain tetap. Hubungan ini tidak "
                               "membuktikan sebab-akibat."),
                    unsafe_allow_html=True)
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
                colors = [TOK["accent"] if v > 0 else TOK["ramp6"] for v in top["Bobot"]]
                ax2.barh(top["Fitur"], top["Bobot"], color=colors, edgecolor="none", height=.6)
                ax2.axvline(0, color=TOK["rule"], linewidth=1)
                ax2.set_xlabel("Koefisien model (log-odds)")
                ax2.grid(axis="x", alpha=.25, color=TOK["rule"])
                style_fig(fig2, ax2)
                plt.tight_layout()
                st.pyplot(fig2, width="stretch")
                plt.close(fig2)
                st.dataframe(top.drop(columns="Abs"), width="stretch", hide_index=True)
            else:
                imp = pd.DataFrame({"Fitur": clean, "Importance": clf.feature_importances_})
                top = imp.sort_values("Importance", ascending=False).head(15).sort_values("Importance")
                fig2, ax2 = plt.subplots(figsize=(8, 5))
                ax2.barh(top["Fitur"], top["Importance"], color=TOK["accent"], height=.6)
                ax2.set_xlabel("Importance")
                style_fig(fig2, ax2)
                plt.tight_layout()
                st.pyplot(fig2, width="stretch")
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

# ---------- TAB 4: EDA & dokumentasi ----------
with tab4:
    st.markdown(ui.section("Mengenal Data Pelanggan", "search",
                           "EDA adalah pemeriksaan awal untuk memahami isi dan pola data sebelum "
                           "membuat model. Grafik hubungan dengan churn memakai data training "
                           "saja; data testing disimpan untuk pengujian akhir."),
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
            st.write("TotalCharges adalah total tagihan selama berlangganan. Kolom ini tidak "
                     "digunakan sebagai fitur agar pengguna cukup mengisi lama berlangganan "
                     "(tenure) dan tagihan bulanan (MonthlyCharges), tanpa perlu mencari total "
                     "tagihan dari seluruh riwayat pembayaran.")
            st.write("TotalCharges juga berkaitan erat dengan tenure, sehingga sebagian "
                     "informasinya beririsan dengan fitur yang tetap digunakan. Namun, nilainya "
                     "tidak selalu sama dengan MonthlyCharges × tenure. Penghapusan ini merupakan "
                     "pilihan untuk menyederhanakan input; kami belum membandingkan performa model "
                     "dengan dan tanpa TotalCharges.")
            st.caption("Menghapus kolom berbeda dengan menghapus baris: pada tahap cleaning, 11 baris "
                       "dengan TotalCharges kosong lebih dulu dihapus untuk mempertahankan data "
                       "pemodelan yang sama dengan eksperimen awal. Setelah itu, kolom TotalCharges "
                       "dibuang. Jika kolom tersebut sejak awal tidak dipakai, nilai kosongnya saja "
                       "tidak mengharuskan baris data ikut dihapus.")
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

    st.markdown(ui.section("Dokumentasi Kelompok 12", "doc"), unsafe_allow_html=True)
    repo_docs = "https://github.com/makhdanramadhan-ui/Machine-Learning-Project/blob/main/docs/"
    st.markdown(f"- [Laporan EDA]({repo_docs}eda%28explaratory%20data%20analysis%29/EDA.md)\n"
                f"- [Lima jurnal dan tabel studi literatur]({repo_docs}STUDI_LITERATUR.md)\n"
                f"- [PPT laporan]({repo_docs}ML2026_B2_Kelompok12_PrediksiCustomerChurn.pptx)")

st.markdown(
    '<div class="sheet-foot">Kelompok 12 · B2 · Muhamad Akhdan Ramadhan (J0404241102) · '
    'Thevan Erlangga (J0404241073) · Fachri Abyasa Tarid (J0404241136)</div>',
    unsafe_allow_html=True,
)
