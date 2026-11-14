# Prediksi Customer Churn Telco

Aplikasi web berbasis Streamlit untuk memprediksi risiko churn pelanggan telekomunikasi menggunakan probabilitas terkalibrasi, pemrosesan batch CSV, dan rekomendasi tindakan retensi berbasis aturan.

**Demo Langsung:** https://machine-learning-project-u8yovshrqrc5tm5s2y2qto.streamlit.app/

Proyek ini berawal dari proyek akhir mata kuliah Pembelajaran Mesin, lalu dikembangkan lebih lanjut menjadi aplikasi yang terstruktur secara modular, terkalibrasi probabilitasnya, dan dilengkapi rangkaian pengujian otomatis sebelum dideploy.

## Ringkasan Teknis

- **Model Utama:** Logistic Regression (`C=10.0`, `class_weight="balanced"`) dengan kalibrasi sigmoid 5-fold pada data latih.
- **Performa Holdout (n = 1.407, threshold = 0,32):** Recall `0,7353`, F1 `0,6166`, Precision `0,5309`, Accuracy `0,7569`, ROC AUC `0,8324`, Brier Score `0,1414`.
- **Validasi & Integritas:** Verifikasi SHA-256 pada artefak model saat startup, validasi skema dan konsistensi logika antar-fitur sebelum inferensi, serta 7 pengujian unit dan UI (`AppTest`).

## Cakupan Masalah dan Dataset

Data berasal dari dataset publik IBM Telco Customer Churn (`Telco-Customer-Churn.csv`) yang berisi 7.043 baris dan 21 kolom. Pada tahap pembersihan di `training_data.py`, 11 baris dengan nilai `TotalCharges` kosong (seluruhnya pada `tenure = 0`) dihapus sehingga tersisa 7.032 baris bersih.

- **Ketidakseimbangan Kelas:** Dari 7.032 pelanggan, terdapat 5.163 tidak churn (sekitar 73,4%) dan 1.869 churn (sekitar 26,6%). Karena kelas tidak seimbang, evaluasi berfokus pada F1, Recall, Precision, ROC AUC, dan Brier Score, bukan hanya akurasi.
- **Pemilihan 18 Fitur Input:** Kolom `customerID`, target `Churn`, dan `TotalCharges` tidak digunakan sebagai fitur model. `TotalCharges` sengaja dikeluarkan untuk menyederhanakan input form pengguna sekaligus menghindari kolinearitas tinggi dengan `tenure` (`r = 0,827` pada data latih).
- **Pembagian Data:** Data dibagi secara stratified 80/20 (`random_state=42`) menjadi 5.625 baris data latih dan 1.407 baris data uji holdout.

## Seleksi Model dan Analisis Overfitting

Pipeline pra-pemrosesan (`train.py`) menggunakan `ColumnTransformer` dengan `StandardScaler` untuk 3 fitur numerik (`SeniorCitizen`, `tenure`, `MonthlyCharges`) dan `OneHotEncoder(handle_unknown="ignore")` untuk 15 fitur kategorikal. Tiga kandidat algoritma dievaluasi menggunakan 5-fold `StratifiedKFold` dan `GridSearchCV` dengan metrik seleksi `CV_F1`.

Tabel berikut merangkum hasil perbandingan dari `hasil_perbandingan.csv` (evaluasi holdout diukur pada threshold default `0,50` sebelum kalibrasi):

| Model | CV F1 (std) | CV Train F1 | Train F1 | Accuracy | Precision | Recall | Test F1 | ROC AUC | Brier |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LogisticRegression | 0,6304 (0,0087) | 0,6354 | 0,6338 | 0,7264 | 0,4908 | 0,7861 | 0,6043 | 0,8321 | 0,1741 |
| RandomForest | 0,6260 (0,0126) | 0,8342 | 0,8217 | 0,7697 | 0,5548 | 0,6765 | 0,6096 | 0,8235 | 0,1567 |
| DecisionTree | 0,6147 (0,0083) | 0,6366 | 0,6433 | 0,7363 | 0,5025 | 0,7968 | 0,6163 | 0,8305 | 0,1721 |

`LogisticRegression` dipilih sebagai model inti karena mencatat `CV_F1` tertinggi (`0,6304`) dengan selisih performa latih dan validasi yang sangat kecil (`CV_TRAIN_F1` `0,6354` vs `CV_F1` `0,6304`). Sebaliknya, `RandomForest` menunjukkan kesenjangan latih-validasi yang lebar (`Train_F1` `0,8217` vs `CV_F1` `0,6260`), yang menandakan overfitting pada data latih.

## Kalibrasi Probabilitas dan Penyesuaian Threshold

Penggunaan `class_weight="balanced"` pada model inti menggeser skor probabilitas mentah ke atas sehingga tidak lagi mencerminkan peluang empiris sebenarnya. Untuk memperbaikinya, `calibrate.py` menerapkan `CalibratedClassifierCV` dengan metode `sigmoid` (5-fold) secara eksklusif pada data latih.

- **Penurunan Brier Score:** Pada data uji holdout, Brier Score turun dari `0,1741` (model dasar) menjadi `0,1414` (setelah kalibrasi).
- **Reliabilitas per Tingkat Risiko (data uji):**
  - `LOW` (< 0,32, n = 889): rata-rata prediksi `0,1068` vs tingkat churn aktual `0,1114`
  - `MID` (0,32 - < 0,60, n = 303): rata-rata prediksi `0,4613` vs tingkat churn aktual `0,4257`
  - `HIGH` (>= 0,60, n = 215): rata-rata prediksi `0,6872` vs tingkat churn aktual `0,6791`

Threshold keputusan dipilih melalui pencarian rentang `0,10` hingga `0,60` (step `0,01`) terhadap probabilitas out-of-fold (OOF) 5-fold pada data latih saja. Threshold `0,32` menghasilkan OOF F1 tertinggi sebesar `0,6338`, dengan batas kategori risiko tinggi ditetapkan pada `0,60`.

Perbandingan performa model terkalibrasi pada 1.407 data uji holdout (`deployment_info.json`):

| Threshold | Accuracy | Precision | Recall | F1 | ROC AUC | Brier | TN | FP | FN | TP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0,50 (default) | 0,8024 | 0,6472 | 0,5642 | 0,6029 | 0,8324 | 0,1414 | 918 | 115 | 163 | 211 |
| 0,32 (terpilih) | 0,7569 | 0,5309 | 0,7353 | 0,6166 | 0,8324 | 0,1414 | 790 | 243 | 99 | 275 |

Penurunan threshold dari `0,50` ke `0,32` menaikkan Recall dari `56,42%` menjadi `73,53%` dan menekan jumlah pelanggan churn yang terlewat (False Negative) dari 163 menjadi 99, dengan konsekuensi peningkatan False Positive dari 115 menjadi 243.

## Arsitektur dan Praktik Rekayasa Perangkat Lunak

Kode dipisahkan berdasarkan tanggung jawab agar alur pelatihan, kalibrasi, validasi, dan antarmuka mudah dipelihara serta diuji secara terpisah:

- `training_data.py`: Memuat `Telco-Customer-Churn.csv`, membersihkan baris kosong, dan menghasilkan stratified 80/20 split yang deterministik.
- `train.py`: Menjalankan `GridSearchCV` 5-fold, menyimpan tabel perbandingan (`hasil_perbandingan.csv`, `cv_detail.csv`), artefak `model_churn.pkl`, lalu memanggil `calibrate()`.
- `calibrate.py`: Melatih kalibrator sigmoid pada data latih, mencari threshold OOF optimal, dan menulis metadata `calib_info.json` serta `deployment_info.json`.
- `prediction.py`: Mengekstrak skema fitur langsung dari pipeline terlatih, melakukan validasi ketat pada input tunggal maupun CSV, menghitung probabilitas, dan memetakan tingkat risiko (`RENDAH`, `SEDANG`, `TINGGI`).
- `app.py` & `ui.py`: Antarmuka Streamlit dengan mode tema Terang/Gelap, simulasi pelanggan tunggal beserta saran retensi berbasis aturan, pemrosesan batch CSV dengan unduhan hasil, serta panel metrik evaluasi model.

Pengamanan dan pengujian yang diterapkan:

- **Verifikasi Integritas Artefak:** Saat startup, `app.py` menghitung hash SHA-256 file `model_churn.pkl` dan `calibrator.pkl`, lalu mencocokkannya dengan nilai di `deployment_info.json` sebelum memuat model.
- **Validasi Skema dan Konsistensi Logika:** `validate_input()` memeriksa kelengkapan dan duplikasi kolom, batasan numerik (`SeniorCitizen` 0/1, `tenure` bilangan bulat 0-72, `MonthlyCharges` 0-120 dolar), daftar nilai kategori valid, serta konsistensi antar-layanan (misalnya `PhoneService=No` mewajibkan `MultipleLines=No phone service`, dan `InternetService=No` mewajibkan nilai `No internet service` pada 6 fitur tambahan internet).
- **Pengujian Otomatis (`tests/test_app.py`):** Berisi 7 skenario pengujian unit dan `streamlit.testing.v1.AppTest` yang memverifikasi penerimaan dataset mentah dan template, penolakan input tidak valid tanpa menjalankan prediksi, kesesuaian hasil evaluasi holdout dengan `deployment_info.json`, konsistensi batas threshold, serta alur UI form tunggal dan unggah batch CSV.

## Menjalankan Secara Lokal

Pastikan Python 3 telah terpasang, lalu instal dependensi dari `requirements.txt`:

```bash
pip install -r requirements.txt
```

Untuk melatih ulang model, melakukan kalibrasi, dan memperbarui artefak evaluasi:

```bash
python train.py
```

Untuk menjalankan aplikasi Streamlit secara lokal:

```bash
streamlit run app.py
```

Untuk menjalankan seluruh rangkaian unit test dan UI test:

```bash
python -m unittest discover -s tests -v
```

## Keterbatasan Model dan Data

- Model dilatih pada dataset historis publik IBM Telco Customer Churn (7.032 baris bersih) dari satu titik waktu; distribusi fitur dan tingkat churn di lingkungan produksi nyata dapat berbeda sehingga memerlukan kalibrasi atau pelatihan ulang secara berkala.
- Analisis korelasi pada data latih menunjukkan hubungan antar-fitur seperti kontrak bulanan dan tagihan bulanan dengan churn, namun pola tersebut bersifat asosiatif dan tidak membuktikan hubungan sebab-akibat.
- Fitur `TotalCharges` tidak disertakan untuk menjaga kesederhanaan pengisian form, dan perbandingan performa eksperimental dengan serta tanpa `TotalCharges` belum dilakukan.
- Rekomendasi tindakan retensi pada aplikasi disusun berbasis aturan statis dari profil input, bukan dari model kausal (uplift modeling) atau hasil eksperimen A/B.
