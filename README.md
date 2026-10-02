# Prediksi Customer Churn — Telco

Aplikasi Streamlit untuk memprediksi churn pelanggan, menampilkan probabilitas
terkalibrasi, memberikan saran retensi berbasis aturan, dan memproses CSV massal.

**Aplikasi:** https://machine-learning-project-u8yovshrqrc5tm5s2y2qto.streamlit.app/

## Kelompok 12

| Anggota | NIM |
|---|---|
| Muhamad Akhdan Ramadhan | J0404241102 |
| Thevan Erlangga | J0404241073 |
| Fachri Abyasa Tarid | J0404241136 |

## Menjalankan aplikasi

Gunakan **Python 3.12 atau lebih baru**. Versi dependensi dikunci di
`requirements.txt`; model terbaru dilatih menggunakan scikit-learn 1.9.1.

```bash
python -m venv .venv
```

Aktifkan environment di Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Atau di Linux/macOS:

```bash
source .venv/bin/activate
```

Kemudian, dari folder repository:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Artefak model tersedia di repository sehingga training ulang tidak diperlukan
untuk menjalankan aplikasi. Di Streamlit Community Cloud, pilih repository ini,
branch `main`, entrypoint `app.py`, dan Python 3.12 atau lebih baru.

## Fitur dan aturan prediksi

- **Single:** input 18 fitur pelanggan. Opsi add-on otomatis menyesuaikan layanan
  telepon/internet. Hasil lama disembunyikan saat input berubah sampai diprediksi ulang.
- **Batch:** unduh template langsung dari aplikasi, unggah CSV UTF-8 dengan
  pemisah koma, lihat ringkasan, lalu unduh semua hasil.
- **Validasi:** kolom wajib, angka kosong/non-numerik/tak berhingga, rentang angka,
  kategori tidak dikenal, header duplikat, dan konsistensi layanan diperiksa.
  Jika ada baris invalid, batch ditolak dengan pesan dan nomor baris data;
  tidak ada penghapusan baris diam-diam.
- **Dashboard:** evaluasi model aplikasi, perbandingan tiga model inti,
  confusion matrix, validation-fold F1, analisis train–test, dan koefisien model inti.

**Probabilitas dan label berasal dari model terkalibrasi yang sama.** Ambang saat ini
adalah **0,32**: CHURN jika probabilitas ≥ 32%, TETAP jika lebih rendah.
Ambang dipilih dengan F1 maksimum pada prediksi out-of-fold **data train**,
bukan menggunakan test set. Karena ambangnya 32%, CHURN tidak harus memiliki
probabilitas di atas 50%; ini merupakan trade-off precision–recall yang dinyatakan eksplisit.

Kategori tampilan: RENDAH <32%, SEDANG 32%–<60%, TINGGI ≥60%.
Kategori risiko bukan target/model klasifikasi tambahan. Saran retensi berbasis
aturan profil, bukan hasil pengujian kausal efektivitas penawaran.

CSV harus memuat:

```text
gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges
```

`SeniorCitizen` menerima 0/1, `tenure` bulan bulat 0–72, dan `MonthlyCharges`
angka 0–120 dolar. Rentang data latih MonthlyCharges adalah 18,25–118,75;
nilai di luarnya ditandai sebagai informasi. Tenure 0 juga ditandai karena cohort
latih bersih dimulai pada 1 bulan. Kolom tambahan, termasuk `customerID`,
`TotalCharges`, dan `Churn`, diabaikan oleh model dan tetap disertakan dalam hasil.

## Hasil pengujian aktual

Dataset di-split stratified 80:20 (`random_state=42`): 5.625 train dan 1.407 test.
Model inti dipilih dari Stratified 5-Fold GridSearchCV pada training set.

| Model inti, threshold 0,50 | CV-F1 | Accuracy test | Precision test | Recall test | F1 test |
|---|---:|---:|---:|---:|---:|
| Logistic Regression — dipilih | 0,6304 | 0,7264 | 0,4908 | 0,7861 | 0,6043 |
| Random Forest | 0,6260 | 0,7697 | 0,5548 | 0,6765 | 0,6096 |
| Decision Tree | 0,6147 | 0,7363 | 0,5025 | 0,7968 | 0,6163 |

Logistic Regression dipilih karena **CV-F1 tertinggi**, bukan karena recall test
tertinggi. Selisih CV-F1 dengan Random Forest kecil, sehingga tidak membuktikan
keunggulan mutlak. Decision Tree memiliki recall test tertinggi.

**Konfigurasi aplikasi: Logistic Regression + sigmoid calibration, threshold 0,32.**

| Accuracy | Precision | Recall | F1 | ROC-AUC | Brier |
|---:|---:|---:|---:|---:|---:|
| 0,7569 | 0,5309 | 0,7353 | 0,6166 | 0,8324 | 0,1414 |

Confusion matrix aplikasi: TN=790, FP=243, FN=99, TP=275. Brier sebelum
kalibrasi 0,1741. Kalibrasi meningkatkan kualitas probabilitas pada holdout ini;
konfigurasi baru tidak unggul pada semua metrik: recall lebih rendah dari model
inti threshold 0,50, sementara precision dan F1 meningkat.

Random Forest menunjukkan indikasi overfitting: F1 train 0,8217 vs test 0,6096.
Accuracy baseline selalu memprediksi tidak churn adalah 0,7342, sehingga
accuracy saja tidak cukup untuk menilai keberhasilan deteksi churn.

## Melatih ulang dan mengevaluasi

```bash
python train.py
```

Perintah ini menjalankan tiga model dan GridSearchCV, menyimpan model terbaik
berdasarkan CV-F1, kemudian melakukan kalibrasi dan seleksi threshold train-only.
Kalibrasi 5-fold dilakukan di dalam masing-masing outer training fold untuk
membuat prediksi out-of-fold pemilihan threshold. Hyperparameter model inti
sudah dipilih dari data train; skor OOF threshold adalah **skor tuning**,
bukan estimasi generalisasi independen. Holdout 20% dipakai untuk evaluasi akhir.

Jika hanya memperbarui kalibrasi setelah model inti tersedia:

```bash
python calibrate.py
```

Deploy artefak model dan metadata hasil perintah ini bersama-sama. Aplikasi
memeriksa SHA-256 model terhadap metadata evaluasi agar hasil dashboard
tidak tertukar dengan versi model lain.

## Berkas aplikasi

| Berkas | Fungsi |
|---|---|
| `app.py` | UI Streamlit |
| `prediction.py` | Validasi bersama, probabilitas, threshold, kategori risiko, template |
| `training_data.py` | Cleaning dan split acuan yang dipakai training/kalibrasi |
| `train.py`, `calibrate.py` | Training, evaluasi, kalibrasi, seleksi threshold |
| `model_churn.pkl` | Pipeline model inti dan preprocessing |
| `calibrator.pkl` | Ensemble terkalibrasi yang dipakai aplikasi |
| `deployment_info.json` | Threshold, metrik aplikasi, versi sklearn, hash artefak |
| `model_info.json`, `hasil_perbandingan.csv`, `cv_detail.csv` | Perbandingan model inti |
| `calib_info.json`, `threshold_selection.csv` | Evaluasi probabilitas dan jejak tuning threshold |
| `tests/test_app.py` | Uji regresi validasi, hasil prediksi, dan alur aplikasi |

`projekk.ipynb`, `scaler.pkl`, dan `feature_columns.pkl` adalah berkas dari
alur eksperimen sebelumnya. Aplikasi tidak memakai scaler/daftar fitur lama.
Untuk membangun artefak aplikasi terkini, gunakan `train.py`; notebook lama
belum menyimpan metadata lengkap konfigurasi deployment terbaru.

## Pengujian aplikasi

```bash
python -m unittest discover -s tests -v
```

Enam test mencakup input invalid, dataset/template valid, kesamaan metrik
holdout dengan metadata deployment, keputusan di batas threshold, form
layanan dan hasil kedaluwarsa, serta CSV valid/invalid melalui Streamlit AppTest.

## Dataset dan keterbatasan

Sumber: [IBM Telco Customer Churn di Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn).
CSV lokal berisi 7.043 pelanggan dan 21 kolom. Untuk menjaga cohort pembanding
eksperimen awal, training menggunakan 7.032 pelanggan setelah 11 TotalCharges
kosong dikonversi menjadi missing dan barisnya dihapus. Seluruh 11 baris tersebut
bertenure 0 dan tidak churn; ini merupakan keterbatasan cohort training.

customerID dihapus karena identitas pelanggan bukan fitur prediktif yang
ditujukan untuk generalisasi. TotalCharges tidak diminta untuk menyederhanakan
input aplikasi. Nilainya berkorelasi dengan tenure, tetapi **tidak selalu persis
MonthlyCharges × tenure**. Keuntungan penghapusan fitur belum dibuktikan
dengan eksperimen ablation. Koefisien negatif MonthlyCharges tidak otomatis
berarti model salah: interpretasi mempertimbangkan fitur layanan lainnya.

Dataset ini bukan gambaran seluruh operator/pelanggan saat ini. Prediksi
TETAP bukan jaminan loyalitas; efektivitas rekomendasi retensi belum diuji.
