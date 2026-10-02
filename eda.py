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
OUT = BASE / "docs" / "eda(explaratory data analysis)"
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
    "TotalCharges": "Total tagihan selama berlangganan; tidak digunakan model aplikasi.",
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
                            "Kosong pada CSV awal": raw.isna().sum().values,
                            "Kosong setelah konversi angka": numeric.isna().sum().values,
                            "Kosong setelah data dibersihkan": complete.isna().sum().values})
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
                               ["Data awal (7.043)", "Setelah dibersihkan (7.032)", "Data training (5.625)"]):
        counts = data["Churn"].value_counts().reindex(["No", "Yes"])
        ax.bar(["Tidak churn", "Churn"], counts, color=["#2563eb", "#ef4444"])
        ax.set_title(title)
        for i, count in enumerate(counts):
            ax.text(i, count, f"{count:,}\n{count / len(data):.1%}", ha="center", va="bottom", fontsize=10)
        ax.set_ylim(0, counts.max() * 1.25)
    save(fig, "01_target_distribution.png", "Setelah data dibersihkan, sekitar 73,4% pelanggan tidak churn dan "
         "26,6% churn. Jumlah kedua kelompok tidak seimbang. Karena itu, akurasi perlu dilihat bersama "
         "precision, recall, dan F1 agar kemampuan mendeteksi churn tidak terlewat.")

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    for ax, col in zip(axes, ["tenure", "MonthlyCharges", "TotalCharges"]):
        ax.hist(train[col], bins=24, color="#7c3aed", alpha=0.85, edgecolor="white")
        ax.set_title(col + " — data training")
        ax.set_ylabel("Pelanggan")
        ax.set_xlabel("Bulan" if col == "tenure" else "Dolar")
    save(fig, "02_numeric_histograms_train.png", "Tenure menunjukkan lama berlangganan, dari pelanggan baru "
         "hingga 72 bulan. Tagihan bulanan tersebar dalam beberapa kelompok, sedangkan total tagihan "
         "banyak berada pada nilai rendah. StandardScaler menyamakan skala fitur angka untuk Logistic "
         "Regression, bukan membuat distribusinya menjadi normal.")

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.7))
    for ax, col in zip(axes, ["tenure", "MonthlyCharges", "TotalCharges"]):
        ax.boxplot([train.loc[train.Churn == label, col] for label in ["No", "Yes"]],
                   tick_labels=["Tidak churn", "Churn"], patch_artist=True,
                   boxprops={"facecolor": "#ddd6fe"}, medianprops={"color": "#7c3aed"})
        ax.set_title(col + " — data training")
    medians = train.groupby("Churn")[["tenure", "MonthlyCharges"]].median()
    save(fig, "03_numeric_boxplots_train.png", f"Pada data training, median lama berlangganan pelanggan "
         f"churn adalah {medians.loc['Yes', 'tenure']:.0f} bulan, sedangkan pelanggan tidak churn "
         f"{medians.loc['No', 'tenure']:.0f} bulan. Median tagihannya masing-masing "
         f"${medians.loc['Yes', 'MonthlyCharges']:.2f} dan ${medians.loc['No', 'MonthlyCharges']:.2f}. "
         "Pola ini belum membuktikan sebab-akibat. Titik outlier pada boxplot dihitung per kelompok, "
         "berbeda dari tabel IQR yang memeriksa seluruh data sekaligus.")

    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(correlations, vmin=-1, vmax=1, cmap="RdBu_r")
    ax.set_xticks(range(4), correlations.columns, rotation=25, ha="right")
    ax.set_yticks(range(4), correlations.index)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, f"{correlations.iloc[i,j]:.2f}", ha="center", va="center",
                    color="white" if abs(correlations.iloc[i,j]) > 0.7 else "black")
    fig.colorbar(im, ax=ax)
    ax.set_title("Korelasi fitur angka — data training")
    save(fig, "04_correlation_train.png", f"Korelasi total tagihan (TotalCharges) dan lama berlangganan "
         f"(tenure) adalah {correlations.loc['TotalCharges','tenure']:.3f} pada data training. "
         "Keduanya berkaitan, tetapi tidak selalu bisa saling menggantikan. TotalCharges tidak "
         "diminta di aplikasi agar pengisian lebih mudah. Hasil model dengan dan tanpa fitur ini belum dibandingkan.")

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.3))
    for ax, col in zip(axes, ["Contract", "InternetService", "PaymentMethod"]):
        subset = rates_df[rates_df.Fitur == col]
        ax.bar(subset.Kategori, subset["Churn rate train"] * 100, color="#2563eb")
        ax.set_title(col + " — data training")
        ax.set_ylabel("Pelanggan churn (%)")
        ax.tick_params(axis="x", rotation=25, labelsize=8)
        for i, value in enumerate(subset["Churn rate train"]):
            ax.text(i, value * 100, f"{value:.1%}", ha="center", va="bottom", fontsize=9)
        ax.set_ylim(0, 60)
    month = rates_df[(rates_df.Fitur == "Contract") & (rates_df.Kategori == "Month-to-month")].iloc[0]
    two = rates_df[(rates_df.Fitur == "Contract") & (rates_df.Kategori == "Two year")].iloc[0]
    save(fig, "05_categorical_churn_train.png", f"Pada data training, {month['Churn rate train']:.1%} "
         f"pelanggan kontrak bulanan churn, dibanding {two['Churn rate train']:.1%} pada kontrak dua tahun. "
         "Persentase churn juga berbeda menurut layanan internet dan cara pembayaran. Ini membantu "
         "mengenali pola pelanggan, tetapi belum membuktikan bahwa mengganti kontrak atau metode pembayaran akan mencegah churn.")

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, col in zip(axes, ["Contract", "InternetService", "SeniorCitizen"]):
        counts = train[col].astype(str).value_counts()
        ax.bar(counts.index, counts.values, color="#7c3aed")
        ax.set_title(col + " — data training")
        ax.set_ylabel("Pelanggan")
        ax.tick_params(axis="x", rotation=20)
    save(fig, "06_categorical_distribution_train.png", "Sebagian besar pelanggan bukan senior. Jumlah "
         "pelanggan juga berbeda di setiap jenis kontrak dan layanan internet. Saat membandingkan "
         "persentase churn, perhatikan jumlah pelanggan dalam kelompoknya: hasil kelompok kecil belum tentu mewakili semua pelanggan.")

    fig, ax = plt.subplots(figsize=(8, 4))
    for label, color in [("No", "#2563eb"), ("Yes", "#ef4444")]:
        sample = train[train.Churn == label].sample(n=min(500, int((train.Churn == label).sum())), random_state=42)
        ax.scatter(sample.tenure, sample.MonthlyCharges, s=13, alpha=0.35, color=color, label=label)
    ax.set(xlabel="Lama berlangganan (bulan)", ylabel="Tagihan bulanan ($)",
           title="Lama berlangganan dan tagihan — data training")
    ax.legend(title="Churn")
    save(fig, "07_scatter_train.png", "Pelanggan churn dan tidak churn tersebar pada lama berlangganan "
         "dan tagihan yang mirip. Dua fitur ini saja belum dapat memisahkan semua pelanggan dengan jelas. "
         "Grafik mengambil paling banyak 500 pelanggan per kelompok agar mudah dibaca; jumlah titiknya bukan perbandingan jumlah kelas.")

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
                f"Data awal: **{len(raw):,} pelanggan, {raw.shape[1]} kolom**. Setelah dibersihkan: **{len(complete):,} pelanggan, "
                f"18 fitur + 1 target**. customerID adalah ID; Churn Yes=1, No=0. "
                "Grafik hubungan fitur–target memakai train saja (5.625); test (1.407) disimpan untuk evaluasi akhir. "
                "Pemeriksaan kualitas data mentah tidak melakukan fitting preprocessing.",
                "\n## 2. Kamus variabel", md_table(dictionary),
                "\n## 3. Statistik deskriptif", md_table(numeric[["tenure", "MonthlyCharges", "TotalCharges"]].describe().round(3).reset_index()),
                "\n## 4. Missing value", md_table(missing),
                "Sebelas string kosong pada TotalCharges terdeteksi setelah konversi numerik. "
                "Seluruhnya tenure=0 dan Churn=No. Data pemodelan awal dipertahankan untuk perbandingan eksperimen; "
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
