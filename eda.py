"""EDA reproduktif; grafik hubungan dengan target memakai data TRAIN saja."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

BASE = Path(__file__).resolve().parent
OUT = BASE / "docs" / "eda"
DATASET_URL = "https://www.kaggle.com/datasets/blastchar/telco-customer-churn"
MEANINGS = {
    "customerID": "Identitas unik pelanggan; tidak digunakan model.",
    "gender": "Jenis kelamin pelanggan (Female/Male).",
    "SeniorCitizen": "Indikator pelanggan senior: 1=ya, 0=tidak.",
    "Partner": "Apakah pelanggan memiliki pasangan (Yes/No).",
    "Dependents": "Apakah pelanggan memiliki tanggungan (Yes/No).",
    "tenure": "Lama berlangganan, dalam bulan.",
    "PhoneService": "Apakah pelanggan memakai layanan telepon (Yes/No).",
    "MultipleLines": "Layanan beberapa jalur telepon; No phone service jika tanpa telepon.",
    "InternetService": "Jenis internet: DSL, Fiber optic, atau No.",
    "OnlineSecurity": "Layanan keamanan online; No internet service jika tanpa internet.",
    "OnlineBackup": "Layanan backup online; No internet service jika tanpa internet.",
    "DeviceProtection": "Layanan perlindungan perangkat; No internet service jika tanpa internet.",
    "TechSupport": "Layanan bantuan teknis; No internet service jika tanpa internet.",
    "StreamingTV": "Layanan streaming TV; No internet service jika tanpa internet.",
    "StreamingMovies": "Layanan streaming film; No internet service jika tanpa internet.",
    "Contract": "Durasi kontrak: Month-to-month, One year, Two year.",
    "PaperlessBilling": "Penggunaan tagihan tanpa kertas (Yes/No).",
    "PaymentMethod": "Metode pembayaran: cek elektronik/pos atau transfer/kartu otomatis.",
    "MonthlyCharges": "Tagihan bulanan pelanggan, dalam dolar.",
    "TotalCharges": "Total tagihan kumulatif; tidak digunakan model aplikasi.",
    "Churn": "Target: Yes=berhenti berlangganan, No=tidak berhenti dalam periode label dataset.",
}


def md_table(frame):
    headers = list(frame.columns)
    lines = ["| " + " | ".join(map(str, headers)) + " |",
             "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in frame.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(v).replace("|", "/") for v in row) + " |")
    return "\n".join(lines)


def run_eda():
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "figure.facecolor": "white", "axes.facecolor": "white"})
    raw = pd.read_csv(BASE / "Telco-Customer-Churn.csv")
    numeric = raw.copy()
    numeric["TotalCharges"] = pd.to_numeric(numeric["TotalCharges"], errors="coerce")
    complete = numeric.dropna().reset_index(drop=True)
    y = complete["Churn"].eq("Yes").astype(int)
    train_idx, test_idx = train_test_split(np.arange(len(complete)), test_size=0.2,
                                         stratify=y, random_state=42)
    train = complete.iloc[train_idx].copy()
    test = complete.iloc[test_idx].copy()
    features = complete.drop(columns=["customerID", "TotalCharges", "Churn"])

    dictionary = pd.DataFrame([{
        "Variabel": col, "Tipe CSV": str(raw[col].dtype),
        "Tipe semantik": "target biner" if col == "Churn" else
        ("numerik kontinu" if col in ["MonthlyCharges", "TotalCharges"] else
         "numerik diskrit" if col == "tenure" else "ID" if col == "customerID" else "kategorikal"),
        "Jumlah nilai unik": int(numeric[col].nunique()), "Arti": MEANINGS[col],
        "Peran": "target" if col == "Churn" else "dihapus" if col in ["customerID", "TotalCharges"] else "fitur",
    } for col in raw.columns])
    dictionary.to_csv(OUT / "data_dictionary.csv", index=False, encoding="utf-8-sig")
    numeric.describe(include="all").T.to_csv(OUT / "descriptive_statistics.csv")
    missing = pd.DataFrame({"Kolom": raw.columns,
                            "Missing CSV awal": raw.isna().sum().values,
                            "Missing setelah konversi": numeric.isna().sum().values,
                            "Missing cohort bersih": complete.isna().sum().values})
    missing.to_csv(OUT / "missing_values.csv", index=False)
    outliers = []
    for col in ["tenure", "MonthlyCharges", "TotalCharges"]:
        values = numeric[col].dropna()
        q1, q3 = values.quantile([0.25, 0.75])
        low, high = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
        outliers.append({"Variabel": col, "Minimum": float(values.min()), "Maximum": float(values.max()),
                         "Batas IQR bawah": round(float(low), 4), "Batas IQR atas": round(float(high), 4),
                         "Jumlah outlier IQR": int(((values < low) | (values > high)).sum())})
    outliers_df = pd.DataFrame(outliers)
    outliers_df.to_csv(OUT / "outliers_iqr.csv", index=False)
    duplicate_counts = {
        "raw_full_rows": int(raw.duplicated().sum()),
        "customerID": int(raw["customerID"].duplicated().sum()),
        "raw_without_id": int(raw.drop(columns="customerID").duplicated().sum()),
        "clean_without_id_total_including_target": int(complete.drop(columns=["customerID", "TotalCharges"]).duplicated().sum()),
        "clean_features_only": int(features.duplicated().sum()),
        "test_features_matching_train": len(features.iloc[test_idx].merge(
            features.iloc[train_idx].drop_duplicates(), on=list(features.columns), how="inner")),
    }
    rates = []
    for col in features.columns:
        if col in ["tenure", "MonthlyCharges"]:
            continue
        for value, group in train.groupby(col):
            rates.append({"Fitur": col, "Kategori": str(value), "Jumlah train": len(group),
                          "Churn train": int(group["Churn"].eq("Yes").sum()),
                          "Churn rate train": round(float(group["Churn"].eq("Yes").mean()), 4)})
    rates_df = pd.DataFrame(rates)
    rates_df.to_csv(OUT / "categorical_churn_rates_train.csv", index=False)
    correlations = train[["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]].corr()
    correlations.to_csv(OUT / "correlations_train.csv")
    figure_notes = []

    def save(fig, name, caption):
        fig.tight_layout()
        fig.savefig(OUT / name, dpi=160, bbox_inches="tight")
        plt.close(fig)
        figure_notes.append({"file": name, "interpretation": caption})

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.7))
    for ax, data, title in zip(axes, [raw, complete, train],
                               ["Data mentah (7.043)", "Cohort bersih (7.032)", "Training (5.625)"]):
        counts = data["Churn"].value_counts().reindex(["No", "Yes"])
        ax.bar(["Tidak churn", "Churn"], counts, color=["#2563eb", "#ef4444"])
        ax.set_title(title)
        for i, count in enumerate(counts):
            ax.text(i, count, f"{count:,}\n{count / len(data):.1%}", ha="center", va="bottom", fontsize=10)
        ax.set_ylim(0, counts.max() * 1.25)
    save(fig, "01_target_distribution.png", "Kelas tidak churn dominan (sekitar 73,4%) dan churn sekitar 26,6% "
         "pada cohort bersih. Accuracy saja dapat menutupi kegagalan mendeteksi kelas churn; gunakan precision, recall, dan F1.")

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    for ax, col in zip(axes, ["tenure", "MonthlyCharges", "TotalCharges"]):
        ax.hist(train[col], bins=24, color="#7c3aed", alpha=0.85, edgecolor="white")
        ax.set_title(col + " — TRAIN")
        ax.set_ylabel("Pelanggan")
        ax.set_xlabel("Bulan" if col == "tenure" else "Dolar")
    save(fig, "02_numeric_histograms_train.png", "Tenure mencakup pelanggan baru hingga 72 bulan; tagihan memiliki "
         "beberapa kelompok sesuai paket layanan. TotalCharges berhubungan dengan durasi berlangganan. Bentuk histogram "
         "tidak mengharuskan normalisasi agar normal; StandardScaler digunakan untuk skala numerik Logistic Regression.")

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.7))
    for ax, col in zip(axes, ["tenure", "MonthlyCharges", "TotalCharges"]):
        ax.boxplot([train.loc[train.Churn == label, col] for label in ["No", "Yes"]],
                   tick_labels=["Tidak churn", "Churn"], patch_artist=True,
                   boxprops={"facecolor": "#ddd6fe"}, medianprops={"color": "#7c3aed"})
        ax.set_title(col + " — TRAIN")
    medians = train.groupby("Churn")[["tenure", "MonthlyCharges"]].median()
    save(fig, "03_numeric_boxplots_train.png", f"Median tenure pelanggan churn pada train adalah {medians.loc['Yes', 'tenure']:.0f} "
         f"bulan, dibanding {medians.loc['No', 'tenure']:.0f} bulan pada tidak churn. Median tagihan churn "
         f"${medians.loc['Yes', 'MonthlyCharges']:.2f} vs ${medians.loc['No', 'MonthlyCharges']:.2f}. "
         "Ini hubungan deskriptif, bukan bukti bahwa menaikkan tagihan atau mengganti kontrak menyebabkan churn. "
         "Titik outlier boxplot dihitung per kelas; berbeda dari pemeriksaan IQR seluruh cohort pada tabel kualitas data.")

    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(correlations, vmin=-1, vmax=1, cmap="RdBu_r")
    ax.set_xticks(range(4), correlations.columns, rotation=25, ha="right")
    ax.set_yticks(range(4), correlations.index)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, f"{correlations.iloc[i,j]:.2f}", ha="center", va="center",
                    color="white" if abs(correlations.iloc[i,j]) > 0.7 else "black")
    fig.colorbar(im, ax=ax)
    ax.set_title("Korelasi Pearson numerik — TRAIN")
    save(fig, "04_correlation_train.png", f"Korelasi TotalCharges–tenure pada train adalah "
         f"{correlations.loc['TotalCharges','tenure']:.3f}. Korelasi tinggi tidak membuktikan keduanya identik. "
         "TotalCharges dihapus untuk menyederhanakan input; manfaat penghapusan belum diuji dengan ablation.")

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.3))
    for ax, col in zip(axes, ["Contract", "InternetService", "PaymentMethod"]):
        subset = rates_df[rates_df.Fitur == col]
        ax.bar(subset.Kategori, subset["Churn rate train"] * 100, color="#2563eb")
        ax.set_title(col + " — TRAIN")
        ax.set_ylabel("Churn rate (%)")
        ax.tick_params(axis="x", rotation=25, labelsize=8)
        for i, value in enumerate(subset["Churn rate train"]):
            ax.text(i, value * 100, f"{value:.1%}", ha="center", va="bottom", fontsize=9)
        ax.set_ylim(0, 60)
    month = rates_df[(rates_df.Fitur == "Contract") & (rates_df.Kategori == "Month-to-month")].iloc[0]
    two = rates_df[(rates_df.Fitur == "Contract") & (rates_df.Kategori == "Two year")].iloc[0]
    save(fig, "05_categorical_churn_train.png", f"Pada train, churn rate kontrak bulanan {month['Churn rate train']:.1%}, "
         f"sedangkan kontrak dua tahun {two['Churn rate train']:.1%}. Pelanggan fiber/electronic check juga memiliki "
         "profil churn berbeda. Asosiasi ini mendukung pemilihan fitur, bukan jaminan efektivitas saran retensi.")

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, col in zip(axes, ["Contract", "InternetService", "SeniorCitizen"]):
        counts = train[col].astype(str).value_counts()
        ax.bar(counts.index, counts.values, color="#7c3aed")
        ax.set_title(col + " — TRAIN")
        ax.set_ylabel("Pelanggan")
        ax.tick_params(axis="x", rotation=20)
    save(fig, "06_categorical_distribution_train.png", "Distribusi kategori menunjukkan sebagian besar pelanggan "
         "bukan senior dan kategori kontrak/paket tidak sama besar. Bandingkan churn rate beserta jumlah pelanggan "
         "per kategori, sehingga kelompok kecil tidak dianggap mewakili seluruh populasi.")

    fig, ax = plt.subplots(figsize=(8, 4))
    for label, color in [("No", "#2563eb"), ("Yes", "#ef4444")]:
        sample = train[train.Churn == label].sample(n=min(500, int((train.Churn == label).sum())), random_state=42)
        ax.scatter(sample.tenure, sample.MonthlyCharges, s=13, alpha=0.35, color=color, label=label)
    ax.set(xlabel="Tenure (bulan)", ylabel="MonthlyCharges ($)", title="Sampel scatter train (maks. 500/kelas)")
    ax.legend(title="Churn")
    save(fig, "07_scatter_train.png", "Kedua kelas saling tumpang tindih pada tenure dan tagihan; tidak ada "
         "satu batas sederhana yang memisahkan semua pelanggan churn. Grafik memakai sampel per kelas untuk keterbacaan, "
         "bukan untuk menghitung proporsi populasi.")

    summary = {
        "source": DATASET_URL, "raw_rows": len(raw), "raw_columns": raw.shape[1],
        "clean_rows": len(complete), "input_features": features.shape[1],
        "n_train": len(train), "n_test": len(test), "missing_totalcharges": int(numeric.TotalCharges.isna().sum()),
        "dropped_rows_tenure_zero": int(numeric.loc[numeric.TotalCharges.isna(), "tenure"].eq(0).sum()),
        "target_clean": {k: int(v) for k, v in complete.Churn.value_counts().items()},
        "duplicates": duplicate_counts, "outliers": outliers, "figures": figure_notes,
        "associations_on": "train-only", "numeric_medians_train": medians.round(2).to_dict(),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    sections = ["# Exploratory Data Analysis — Telco Churn", "\nKelompok 12 • Kelas B2",
                f"\nSumber: {DATASET_URL}",
                "\n## 1. Informasi dataset",
                f"Mentah: **{len(raw):,} pelanggan, {raw.shape[1]} kolom**. Cohort bersih: **{len(complete):,} pelanggan, "
                f"18 fitur + 1 target**. customerID adalah ID; Churn Yes=1, No=0. "
                "Grafik hubungan fitur–target memakai train saja (5.625); test (1.407) disimpan untuk evaluasi akhir. "
                "Pemeriksaan kualitas data mentah tidak melakukan fitting preprocessing.",
                "\n## 2. Kamus variabel", md_table(dictionary),
                "\n## 3. Statistik deskriptif", md_table(numeric[["tenure", "MonthlyCharges", "TotalCharges"]].describe().round(3).reset_index()),
                "\n## 4. Missing value", md_table(missing),
                "Sebelas string kosong pada TotalCharges terdeteksi setelah konversi numerik. "
                "Seluruhnya tenure=0 dan Churn=No. Cohort awal dipertahankan untuk perbandingan eksperimen; "
                "karena fitur TotalCharges akhirnya dihapus, membuang baris ini bukan keharusan model. "
                "Eksklusi pelanggan baru merupakan keterbatasan yang perlu diuji pada pengembangan berikutnya.",
                "\n## 5. Duplikat", md_table(pd.DataFrame(duplicate_counts.items(), columns=["Pemeriksaan", "Jumlah"])),
                "Tidak ada ID ganda atau baris mentah identik. Setelah fitur identitas/kumulatif dihapus, "
                "sebagian profil menjadi sama. ID berbeda dapat mewakili pelanggan berbeda, sehingga tidak dihapus otomatis. "
                "Ada profil test identik dengan train; ini membatasi klaim generalisasi untuk profil yang benar-benar baru. "
                "Pengembangan: evaluasi group-aware berdasarkan profil untuk mengukur sensitivitas hasil.",
                "\n## 6. Outlier", md_table(outliers_df),
                "Tidak ada outlier dengan aturan 1,5×IQR pada tiga fitur numerik. Ini tidak berarti semua catatan "
                "bebas anomali domain. Tidak dilakukan clipping/penghapusan outlier; nilai layanan sah dipertahankan.",
                "\n## 7. Visualisasi dan interpretasi"]
    for figure in figure_notes:
        sections.extend([f"\n### {figure['file']}", f"![{figure['file']}]({figure['file']})", figure["interpretation"]])
    sections.extend(["\n## 8. Implikasi preprocessing",
                     "- StandardScaler pada SeniorCitizen (indikator biner), tenure, MonthlyCharges; "
                     "OneHotEncoder pada 15 fitur kategorikal. Scaling indikator biner valid secara matematis, "
                     "namun semantiknya tetap kategori; scaling tidak diperlukan pohon, dipakai untuk pipeline konsisten.",
                     "- Fit scaler/encoder hanya pada training fold melalui Pipeline; tidak memakai statistik test.",
                     "- Class weight diuji dalam GridSearch; tidak memakai SMOTE pada eksperimen ini.",
                     "- TotalCharges dihapus untuk input sederhana; tidak mengklaim koefisien negatif adalah kesalahan.",
                     "- Tabel lengkap churn rate semua kategori tersedia di categorical_churn_rates_train.csv."])
    (OUT / "EDA.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")
    print(f"EDA: {len(raw)} raw -> {len(complete)} clean; {len(figure_notes)} grafik -> {OUT}")
    return summary


if __name__ == "__main__":
    run_eda()
