"""Aplikasi Prediksi Customer Churn - Telco
Pipeline: preprocessing + model dalam 1 file model_churn.pkl (no leakage, no manual scaling)
"""
import joblib
import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- Load artefak ---
pipe = joblib.load("model_churn.pkl")  # Pipeline ColumnTransformer + Classifier
try:
    with open("model_info.json") as f:
        INFO = json.load(f)
except FileNotFoundError:
    INFO = {}
try:
    CMP = pd.read_csv("hasil_perbandingan.csv")
except FileNotFoundError:
    CMP = None

st.set_page_config(page_title="Prediksi Customer Churn", page_icon="📡", layout="wide")
st.title("📡 Aplikasi Prediksi Customer Churn - Telco")

# Sidebar info model
st.sidebar.header("Info Model")
if INFO:
    st.sidebar.write(f"**Model terbaik:** {INFO.get('best_model')}")
    m = INFO.get("metrics", {})
    st.sidebar.write(f"Akurasi: {m.get('Accuracy')} | F1: {m.get('F1')}")
    st.sidebar.write(f"Recall: {m.get('Recall')} | AUC: {m.get('ROC_AUC')}")
    st.sidebar.caption("Dipilih berdasarkan CV-F1 tertinggi.")
st.sidebar.caption("Dataset: Telco-Customer-Churn (7032 bersih, 18 fitur)")

tab1, tab2, tab3 = st.tabs(["🔮 Prediksi Single", "📁 Prediksi Batch (CSV)", "📊 Dashboard & Model"])

# ---------- TAB 1 ----------
with tab1:
    st.subheader("Form Data Pelanggan")
    c1, c2, c3 = st.columns(3)
    with c1:
        gender = st.selectbox("Jenis Kelamin", ["Female", "Male"])
        SeniorCitizen = st.selectbox("Lansia (SeniorCitizen)", ["No", "Ya"], index=0)
        Partner = st.selectbox("Punya Pasangan", ["Yes", "No"], index=1)
        Dependents = st.selectbox("Punya Tanggungan", ["Yes", "No"], index=1)
        tenure = st.number_input("Tenure (bulan)", 0, 72, 12)
        PhoneService = st.selectbox("Layanan Telepon", ["Yes", "No"])
        MultipleLines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
    with c2:
        InternetService = st.selectbox("Internet", ["Fiber optic", "DSL", "No"])
        OnlineSecurity = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
        OnlineBackup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
        DeviceProtection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
        TechSupport = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
        StreamingTV = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
        StreamingMovies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
    with c3:
        Contract = st.selectbox("Kontrak", ["Month-to-month", "One year", "Two year"])
        PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
        PaymentMethod = st.selectbox("Metode Bayar", ["Electronic check", "Mailed check",
            "Bank transfer (automatic)", "Credit card (automatic)"])
        MonthlyCharges = st.number_input("Monthly Charges ($)", 0.0, 200.0, 70.0)

    if st.button("🚀 Prediksi Sekarang", type="primary"):
        # DataFrame 1 baris sesuai kolom mentah training
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

        # Output + kategori risiko
        if prob < 0.30:
            lvl, fn = "🟢 RISIKO RENDAH", st.success
        elif prob < 0.60:
            lvl, fn = "🟡 RISIKO SEDANG", st.warning
        else:
            lvl, fn = "🔴 RISIKO TINGGI", st.error
        fn(f"**{lvl}** — Probabilitas Churn: **{prob*100:.2f}%** "
           f"({'CHURN' if pred == 1 else 'TETAP'})")
        st.progress(prob)

        # Rekomendasi bisnis rule-based
        st.subheader("💡 Rekomendasi Retensi")
        recs = []
        if Contract == "Month-to-month":
            recs.append("Tawarkan upgrade kontrak 1/2 tahun + diskon.")
        if InternetService == "Fiber optic" and MonthlyCharges > 75:
            recs.append("Tagihan fiber tinggi — tawarkan bundling / cashback.")
        if PaymentMethod == "Electronic check":
            recs.append("Migrasi ke auto-pay (transfer/kartu) — terbukti churn lebih rendah.")
        if TechSupport in ("No", "No internet service") and InternetService != "No":
            recs.append("Tawarkan paket TechSupport gratis 3 bulan.")
        if tenure < 6:
            recs.append("Pelanggan baru — onboarding intensif & cek kepuasan minggu ke-4.")
        if not recs:
            recs.append("Pertahankan kualitas layanan + loyalty reward.")
        for r in recs:
            st.write("- " + r)

# ---------- TAB 2 ----------
with tab2:
    st.subheader("Upload CSV untuk prediksi massal")
    st.caption("Format kolom sama seperti Telco-Customer-Churn.csv (tanpa kolom Churn juga bisa).")
    f = st.file_uploader("Pilih file CSV", type="csv")
    if f:
        df = pd.read_csv(f)
        df_clean = df.drop(columns=["customerID", "Churn", "TotalCharges"], errors="ignore").copy()
        probs = pipe.predict_proba(df_clean)[:, 1]
        preds = pipe.predict(df_clean)
        out = df.copy().loc[df_clean.index]
        out["Prob_Churn"] = (probs * 100).round(2)
        out["Prediksi"] = ["CHURN" if p == 1 else "TETAP" for p in preds]
        st.write(f"Hasil: {len(out)} baris | Churn: {(out['Prediksi']=='CHURN').sum()} "
                 f"| Rate: {(out['Prediksi']=='CHURN').mean()*100:.1f}%")
        st.dataframe(out.head(20))
        st.bar_chart(out["Prediksi"].value_counts())
        st.download_button("⬇️ Download Hasil (CSV)",
                           out.to_csv(index=False).encode(), "hasil_prediksi.csv", "text/csv")

# ---------- TAB 3 ----------
with tab3:
    st.subheader("Perbandingan Model (Test Set)")
    with st.expander("Rumus metrik", expanded=True):
        st.markdown(
            "| Metrik | Rumus | Arti (Prediksi vs Realita) |\n"
            "|---|---|---|\n"
            "| TP (True Positive) | TP | Prediksi = churn, Realita = churn (ketangkap, benar) |\n"
            "| TN (True Negative) | TN | Prediksi = setia, Realita = setia (benar dibiarin) |\n"
            "| FP (False Positive) | FP | Prediksi = churn, Realita = setia (salah tuduh) |\n"
            "| FN (False Negative) | FN | Prediksi = setia, Realita = churn (lolos, paling rugi) |\n"
            "| Accuracy | (TP+TN) / total | Tebakan benar / total |\n"
            "| Precision | TP / (TP+FP) | Dari yang dibilang churn, berapa yang benar |\n"
            "| Recall | TP / (TP+FN) | Dari churn asli, berapa yang ketangkap |\n"
            "| Specificity | TN / (TN+FP) | Dari yang setia, berapa yang benar |\n"
            "| F1 | 2×P×R / (P+R) | Rata-rata adil Precision + Recall |\n"
            "| ROC_AUC | luas kurva ROC (FPR vs TPR, semua threshold) | 0.5 = tebak acak, 1.0 = sempurna |")
    if CMP is not None:
        st.dataframe(CMP)
        # Nilai mentah TN/FP/FN/TP model terbaik biar gampang dibaca
        try:
            best_name = INFO.get("best_model", "LogisticRegression")
            b = CMP[CMP["Model"] == best_name].iloc[0]
            st.markdown(f"**Confusion matrix — {best_name} (test 1407 data):**")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("TP: prediksi churn, realita churn", int(b["TP"]))
            k2.metric("TN: prediksi setia, realita setia", int(b["TN"]))
            k3.metric("FP: prediksi churn, realita setia", int(b["FP"]))
            k4.metric("FN: prediksi setia, realita churn", int(b["FN"]))
        except Exception:
            pass
        # Grafik horizontal biar label lurus terbaca
        fig, ax = plt.subplots(figsize=(8, 3))
        plot_df = CMP.set_index("Model")[["Accuracy", "Precision", "Recall", "F1"]]
        plot_df.plot(kind="barh", ax=ax)
        ax.set_xlabel("Skor")
        plt.tight_layout()
        st.pyplot(fig)
        # Teks alasan dibuat dinamis dari CSV biar tidak basi
        try:
            lr = CMP[CMP["Model"] == "LogisticRegression"].iloc[0]
            rf = CMP[CMP["Model"] == "RandomForest"].iloc[0]
            st.markdown(
                f"**Kenapa {INFO.get('best_model', 'LogisticRegression')} dipilih?** "
                f"CV-F1 tertinggi ({lr['CV_F1']}), Recall {lr['Recall']} (miss {int(lr['FN'])} dari "
                f"{int(lr['FN'] + lr['TP'])} churn), AUC {lr['ROC_AUC']}. "
                f"RandomForest akurasi tertinggi ({rf['Accuracy']}) tapi miss {int(rf['FN'])} churn — "
                "dalam bisnis, kehilangan pelanggan (FN) lebih mahal dari promo salah sasaran (FP).")
        except Exception:
            pass
    # Feature insight: koefisien (LogReg) atau importance (Tree)
    st.subheader("Fitur Paling Berpengaruh")
    try:
        pre = pipe.named_steps["pre"]
        feats = pre.get_feature_names_out()
        # Bersihkan prefix num__/cat__ biar gampang dibaca
        clean = [f.split("__", 1)[-1] for f in feats]
        clf = pipe.named_steps["clf"]
        if hasattr(clf, "coef_"):
            imp = pd.DataFrame({"Fitur": clean, "Bobot": clf.coef_[0]})
            imp["Abs"] = imp["Bobot"].abs()
            top = imp.sort_values("Abs", ascending=False).head(15).sort_values("Bobot")
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            colors = ["tab:red" if v > 0 else "tab:green" for v in top["Bobot"]]
            ax2.barh(top["Fitur"], top["Bobot"], color=colors)
            ax2.set_xlabel("Bobot (+ pendorong churn, - penahan)")
            plt.tight_layout()
            st.pyplot(fig2)
            st.dataframe(top.drop(columns="Abs"))
        else:
            imp = pd.DataFrame({"Fitur": clean, "Importance": clf.feature_importances_})
            top = imp.sort_values("Importance", ascending=False).head(15).sort_values("Importance")
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            ax2.barh(top["Fitur"], top["Importance"])
            ax2.set_xlabel("Importance")
            plt.tight_layout()
            st.pyplot(fig2)
            st.dataframe(top)
    except Exception as e:
        st.caption(f"Tidak bisa tampilkan importance: {e}")
