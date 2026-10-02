# Outline PPT

## Slide 1: Prediksi Customer Churn — Telco



Prediksi Customer Churn — Telco

Perbandingan tiga model dan aplikasi Streamlit terkalibrasi

ML 2026  •  B2  •  Kelompok 12                                      01

KELOMPOK 12  /  KELAS B2

Muhamad Akhdan Ramadhan  —  J0404241102
Thevan Erlangga  —  J0404241073
Fachri Abyasa Tarid  —  J0404241136

Mata Kuliah Pembelajaran Mesin • Project Akhir 2026

Catatan presenter: Perkenalkan seluruh anggota. Judul project, Kelompok 12 Kelas B2. Buka aplikasi live pada bagian demo.

## Slide 2: Latar belakang & rumusan masalah



Latar belakang & rumusan masalah

Churn = pelanggan berhenti berlangganan

ML 2026  •  B2  •  Kelompok 12                                      02

• Pelanggan memiliki profil kontrak, layanan, dan pembayaran yang berbeda.
• Identifikasi risiko membantu menentukan prioritas tindak lanjut retensi [1, 4].
• Masalah: bagaimana memprediksi churn dari data pelanggan secara terukur?
• Tantangan: kelas churn minoritas dan biaya false alarm / churn terlewat berbeda.
• Prediksi risiko belum membuktikan efektivitas tindakan retensi.

## Slide 3: Tujuan project



Tujuan project

Klasifikasi supervised tabular, bukan forecasting

ML 2026  •  B2  •  Kelompok 12                                      03

• Memahami dataset melalui EDA dan preprocessing yang sesuai.
• Membandingkan Logistic Regression, Decision Tree, dan Random Forest.
• Memilih model inti melalui validation CV-F1 pada data training.
• Menghasilkan probabilitas terkalibrasi dan keputusan dengan threshold train-only.
• Menyediakan aplikasi single/batch CSV dengan validasi dan dashboard transparan.

## Slide 4: Studi literatur — metode & evaluasi



Studi literatur — metode & evaluasi

Lima jurnal terverifikasi • ringkasan hasil penulis, bukan hasil project

ML 2026  •  B2  •  Kelompok 12                                      04

Referensi | Dataset | Metode | Hasil utama

[1] Sana et al. (2022) | 4 dataset; termasuk Telco 7.043 | 8 model; transformasi + feature selection + grid search | WOE+LR: AUC 0,796 / F1 0,79 (Dataset-1)

[2] Y., Ly & Son (2022) | Orange 3.333 | Kernel SVM + SFS/SBS + SMOTE-ENN | Accuracy 0,9888 / F1 0,9901

[3] Bilal et al. (2022) | GitHub 5.000 / BigML 3.333 | Clustering + classifier ensemble | Accuracy 94,7% / 92,43%

Project: 3 model tabular + pipeline train-only + sigmoid calibration + Streamlit. Skor jurnal tidak dibandingkan langsung karena dataset dan protokol berbeda.

## Slide 5: Studi literatur — early warning & pengembangan



Studi literatur — early warning & pengembangan

Lima jurnal terverifikasi • ringkasan hasil penulis, bukan hasil project

ML 2026  •  B2  •  Kelompok 12                                      05

Referensi | Dataset | Metode | Hasil utama

[4] Zhou et al. (2023) | Operator 900.000 mentah | RF-AdaBoost + SMOTE | P=0,99 / R=0,93 / F1=0,96 (churn)

[5] Khattak et al. (2023) | Telco; 7.033 menurut artikel | BiLSTM-CNN | Accuracy 81% / F-score 65%

Project: 3 model tabular + pipeline train-only + sigmoid calibration + Streamlit. Skor jurnal tidak dibandingkan langsung karena dataset dan protokol berbeda.

## Slide 6: Dataset & target



Dataset & target

Sumber: IBM Telco Customer Churn di Kaggle — blastchar

ML 2026  •  B2  •  Kelompok 12                                      06

Komponen | Jumlah / karakteristik

Data mentah | 7.043 pelanggan • 21 kolom (ID + 19 kandidat fitur + target)

Cohort pemodelan | 7.032 pelanggan • 18 input fitur + target

Target | Churn Yes=1 / No=0 • 1.869 churn dan 5.163 tidak churn

Numerik | tenure (bulan), MonthlyCharges ($); SeniorCitizen indikator 0/1

Kategorikal | 15 fitur: kontrak, layanan, pembayaran, demografi

Sumber dan kamus seluruh 21 variabel: docs/eda/EDA.md

## Slide 7: Pemeriksaan kualitas data



Pemeriksaan kualitas data

Missing, duplikat, outlier, dan keputusan cleaning

ML 2026  •  B2  •  Kelompok 12                                      07

• 11 TotalCharges kosong → numeric coercion → missing; seluruhnya tenure 0 / tidak churn.
• Tidak ada customerID ganda atau baris mentah identik.
• 27 profil duplikat setelah ID/TotalCharges dihapus (termasuk target); tidak dibuang otomatis.
• IQR 1,5× pada tenure, MonthlyCharges, TotalCharges: 0 outlier; tidak dilakukan clipping.
• 18 profil test cocok dengan profil train; menjadi keterbatasan generalisasi profil baru.

## Slide 8: EDA — distribusi kelas



EDA — distribusi kelas

Hubungan fitur–target dianalisis pada training set saja

ML 2026  •  B2  •  Kelompok 12                                      08

Kelas tidak churn dominan (sekitar 73,4%) dan churn sekitar 26,6% pada cohort bersih. Accuracy saja dapat menutupi kegagalan mendeteksi kelas churn; gunakan precision, recall, dan F1.

Catatan presenter: Kelas tidak churn dominan (sekitar 73,4%) dan churn sekitar 26,6% pada cohort bersih. Accuracy saja dapat menutupi kegagalan mendeteksi kelas churn; gunakan precision, recall, dan F1.

## Slide 9: EDA — distribusi numerik



EDA — distribusi numerik

Hubungan fitur–target dianalisis pada training set saja

ML 2026  •  B2  •  Kelompok 12                                      09

Tenure mencakup pelanggan baru hingga 72 bulan; tagihan memiliki beberapa kelompok sesuai paket layanan. TotalCharges berhubungan dengan durasi berlangganan. Bentuk histogram tidak mengharuskan normalisasi agar normal; StandardScaler digunakan untuk skala numerik Logistic Regression.

Catatan presenter: Tenure mencakup pelanggan baru hingga 72 bulan; tagihan memiliki beberapa kelompok sesuai paket layanan. TotalCharges berhubungan dengan durasi berlangganan. Bentuk histogram tidak mengharuskan normalisasi agar normal; StandardScaler digunakan untuk skala numerik Logistic Regression.

## Slide 10: EDA — profil churn vs tidak churn



EDA — profil churn vs tidak churn

Hubungan fitur–target dianalisis pada training set saja

ML 2026  •  B2  •  Kelompok 12                                      10

Median tenure pelanggan churn pada train adalah 10 bulan, dibanding 38 bulan pada tidak churn. Median tagihan churn $79.90 vs $64.68. Ini hubungan deskriptif, bukan bukti bahwa menaikkan tagihan atau mengganti kontrak menyebabkan churn. Titik outlier boxplot dihitung per kelas; berbeda dari pemeriksaan IQR seluruh cohort pada tabel kualitas data.

Catatan presenter: Median tenure pelanggan churn pada train adalah 10 bulan, dibanding 38 bulan pada tidak churn. Median tagihan churn $79.90 vs $64.68. Ini hubungan deskriptif, bukan bukti bahwa menaikkan tagihan atau mengganti kontrak menyebabkan churn. Titik outlier boxplot dihitung per kelas; berbeda dari pemeriksaan IQR seluruh cohort pada tabel kualitas data.

## Slide 11: EDA — kontrak, internet, pembayaran



EDA — kontrak, internet, pembayaran

Hubungan fitur–target dianalisis pada training set saja

ML 2026  •  B2  •  Kelompok 12                                      11

Pada train, churn rate kontrak bulanan 43.1%, sedangkan kontrak dua tahun 2.9%. Pelanggan fiber/electronic check juga memiliki profil churn berbeda. Asosiasi ini mendukung pemilihan fitur, bukan jaminan efektivitas saran retensi.

Catatan presenter: Pada train, churn rate kontrak bulanan 43.1%, sedangkan kontrak dua tahun 2.9%. Pelanggan fiber/electronic check juga memiliki profil churn berbeda. Asosiasi ini mendukung pemilihan fitur, bukan jaminan efektivitas saran retensi.

## Slide 12: EDA — korelasi & pilihan fitur



EDA — korelasi & pilihan fitur

Korelasi bukan identitas dan bukan sebab-akibat

ML 2026  •  B2  •  Kelompok 12                                      12

• TotalCharges berkorelasi kuat dengan tenure.
• TotalCharges dihapus agar input aplikasi sederhana.
• Tidak selalu MonthlyCharges × tenure.
• Belum ada ablation untuk membuktikan keuntungan penghapusan fitur.

## Slide 13: Preprocessing & pencegahan leakage



Preprocessing & pencegahan leakage

Fit preprocessing hanya pada training fold

ML 2026  •  B2  •  Kelompok 12                                      13

• customerID dihapus; TotalCharges tidak digunakan; 11 catatan tidak lengkap dieksklusi.
• StandardScaler: SeniorCitizen, tenure, MonthlyCharges; OneHotEncoder: 15 kategori.
• Scaling membantu LR; pohon tetap memakai pipeline konsisten walau tidak memerlukannya.
• Class weight dituning untuk imbalance; tanpa SMOTE pada eksperimen project.
• ColumnTransformer + classifier dalam Pipeline; test tidak dipakai untuk fit/tuning.

## Slide 14: Tiga algoritma & alasan pemilihan



Tiga algoritma & alasan pemilihan

Membandingkan model linear, pohon tunggal, dan ensemble

ML 2026  •  B2  •  Kelompok 12                                      14

Model | Alasan | Risiko / kontrol

Logistic Regression | Ringan; baseline linear log-odds; koefisien mudah dibahas | C dan class_weight dituning

Decision Tree | Aturan non-linear dan interaksi fitur | max_depth / min_samples_split / class_weight

Random Forest | Bagging banyak pohon; pembanding kompleksitas | Kedalaman dan split dituning; periksa overfitting

Dasar literatur: [1] membandingkan ketiganya; [3]–[4] membahas ensemble churn.

## Slide 15: Training, validation & parameter terbaik



Training, validation & parameter terbaik

80:20 stratified • random_state=42 • CV 5-fold • GridSearch scoring F1

ML 2026  •  B2  •  Kelompok 12                                      15

Model | Parameter terbaik | CV-F1

Logistic Regression | C=10; class_weight=balanced; max_iter=1.000 | 0,6304

Decision Tree | max_depth=5; min_samples_split=2; balanced | 0,6147

Random Forest | 200 pohon; depth=12; min_samples_split=5; balanced_subsample | 0,6260

Train 5.625; test 1.407. Grid: LR 6, DT 12, RF 8 konfigurasi × 5 fold = 130 fit CV, ditambah refit pemenang setiap model. Test tidak masuk fold training.

## Slide 16: Evaluasi & perbandingan model inti



Evaluasi & perbandingan model inti

Label positif: churn • threshold 0,50 • holdout yang sama

ML 2026  •  B2  •  Kelompok 12                                      16

Model | CV-F1 | Accuracy | Precision | Recall | F1 | AUC

LogisticRegression | 0.6304 | 0.7264 | 0.4908 | 0.7861 | 0.6043 | 0.8321

RandomForest | 0.6260 | 0.7697 | 0.5548 | 0.6765 | 0.6096 | 0.8235

DecisionTree | 0.6147 | 0.7363 | 0.5025 | 0.7968 | 0.6163 | 0.8305

LR dipilih dengan CV-F1 tertinggi pada train. DT memiliki recall/F1 test tertinggi; RF accuracy tertinggi. DT CV-F1 terendah; LR F1 test terendah di antara model inti. Selisih CV-F1 LR–RF hanya 0,0044, bukan bukti unggul mutlak.

## Slide 17: Analisis model & overfitting



Analisis model & overfitting

Gunakan train–validation–test, bukan accuracy saja

ML 2026  •  B2  •  Kelompok 12                                      17

• RF: F1 train 0,8217 vs test 0,6096 → indikasi overfitting.
• LR: train 0,6338 vs test 0,6043; gap lebih kecil.
• Baseline selalu tidak churn: accuracy 73,42%, recall churn 0.
• Kompleksitas, regularisasi, class_weight dan interaksi dapat memengaruhi hasil.

## Slide 18: Kalibrasi & pemilihan threshold



Kalibrasi & pemilihan threshold

Model aplikasi: LR + sigmoid calibration 5-fold, train-only

ML 2026  •  B2  •  Kelompok 12                                      18

• Grid threshold 0,10–0,60; langkah 0,01.
• F1 maksimum prediksi OOF train → threshold 0,32.
• Kalibrasi di dalam setiap outer training fold.
• OOF F1 0,6338 adalah skor tuning, bukan estimasi independen.
• CHURN jika probabilitas ≥32%; TETAP jika lebih rendah.

Hyperparameter inti telah dipilih pada train-CV. Test hanya dipakai untuk evaluasi akhir.

## Slide 19: Evaluasi konfigurasi aplikasi



Evaluasi konfigurasi aplikasi

Probabilitas dan keputusan berasal dari model yang sama

ML 2026  •  B2  •  Kelompok 12                                      19

Konfigurasi | Accuracy | Precision | Recall | F1 | AUC | Brier

Threshold 0,32 | 0.7569 | 0.5309 | 0.7353 | 0.6166 | 0.8324 | 0.1414

Threshold 0,50 | 0.8024 | 0.6472 | 0.5642 | 0.6029 | 0.8324 | 0.1414

Threshold 0,32 mendeteksi 275 churn vs 211 pada 0,50; false alarm naik 115 → 243. Trade-off precision–recall; ROC-AUC/Brier tidak berubah jika hanya threshold diganti.

## Slide 20: Confusion matrix & kesalahan prediksi



Confusion matrix & kesalahan prediksi

Test: 1.033 tidak churn dan 374 churn

ML 2026  •  B2  •  Kelompok 12                                      20

• TP 275: churn berhasil terdeteksi.
• FN 99: churn terlewat.
• FP 243: pelanggan tidak churn ditandai churn.
• TN 790: tidak churn diprediksi benar.
• Precision 53,09%; recall 73,53%. Biaya retensi nyata belum diukur.

## Slide 21: ROC & kualitas probabilitas



ROC & kualitas probabilitas

Kurva dihitung dari model tersimpan pada holdout test

ML 2026  •  B2  •  Kelompok 12                                      21

AUC aplikasi 0,8324. Brier turun 0,1741 → 0,1414 setelah kalibrasi. Reliability curve memperlihatkan kedekatan prediksi dan frekuensi aktual; bukan jaminan tiap pelanggan.

## Slide 22: Interpretasi fitur



Interpretasi fitur

Koefisien model inti sebelum kalibrasi

ML 2026  •  B2  •  Kelompok 12                                      22

• Tenure negatif: hubungan bersyarat dengan log-odds churn.
• Kontrak bulanan dan fiber punya bobot positif pada model inti.
• Koefisien MonthlyCharges negatif tidak otomatis salah.
• Fitur saling berhubungan; bobot bukan bukti kausal atau peringkat universal.

## Slide 23: Arsitektur & implementasi aplikasi



Arsitektur & implementasi aplikasi

Python • scikit-learn • pandas • joblib • Streamlit

ML 2026  •  B2  •  Kelompok 12                                      23



INPUT

Form 18 fitur
CSV UTF-8
Template unduhan



VALIDASI

Kolom & kategori
Angka & rentang
Konsistensi layanan



MODEL

Pipeline preprocess
Sigmoid calibrated
Probabilitas churn



OUTPUT

Threshold 0,32
CHURN/TETAP
Risiko + CSV hasil

Artefak dan metadata diperiksa SHA-256. Hasil lama disembunyikan saat input berubah. CSV invalid ditolak dengan pesan dan nomor baris; tidak dibuang diam-diam.

## Slide 24: Demo aplikasi — jalankan langsung



Demo aplikasi — jalankan langsung

Buka URL live; tunjukkan interaksi, bukan hanya screenshot

ML 2026  •  B2  •  Kelompok 12                                      24

• 1. Buka aplikasi: KPI dan tab single, batch, dashboard, serta EDA.
• 2. Isi profil pelanggan; klik Prediksi Sekarang dan jelaskan probabilitas/threshold.
• 3. Download template → upload CSV → tampilkan ringkasan → download hasil.
• 4. Tunjukkan validasi: CSV tanpa tenure atau kategori Contract yang salah.
• 5. Buka dashboard: perbandingan model inti dan evaluasi model aplikasi.

https://machine-learning-project-u8yovshrqrc5tm5s2y2qto.streamlit.app/

Catatan presenter: Gunakan template_pelanggan.csv. Klik Prediksi untuk contoh pelanggan, upload batch, unduh hasil, lalu upload CSV salah untuk menunjukkan validasi. Lihat docs/NASKAH_VIDEO_DEMO.md.

## Slide 25: Kesimpulan



Kesimpulan

Model terukur, aplikasi berjalan, hasil bisa direproduksi

ML 2026  •  B2  •  Kelompok 12                                      25

• LR dipilih berdasarkan CV-F1 training tertinggi (0,6304).
• Konfigurasi aplikasi: sigmoid calibration + threshold 0,32 train-only.
• Test aplikasi: accuracy 75,69%; precision 53,09%; recall 73,53%; F1 0,6166.
• 275 dari 374 churn terdeteksi; 99 terlewat dan 243 false alarm.
• Nilai tambah: probabilitas konsisten, validasi input, batch CSV, dan dashboard evaluasi.

## Slide 26: Keterbatasan & pengembangan



Keterbatasan & pengembangan

Kesimpulan disesuaikan dengan bukti yang tersedia

ML 2026  •  B2  •  Kelompok 12                                      26

Keterbatasan | Pengembangan

Dataset historis tunggal; pelanggan tenure 0 dieksklusi | Validasi eksternal/temporal dan uji cohort pelanggan baru

Profil identik lintas split; fitur TotalCharges dibuang tanpa ablation | Group-aware split; ablation fitur; laporkan perubahan performa

RF overfit; FP/FN masih cukup besar | Regularisasi/tuning; alternatif boosting; threshold berbasis biaya nyata

Retensi berbasis aturan; belum diuji efektivitasnya | SHAP dan eksperimen tindakan retensi; monitoring drift

## Slide 27: Pembagian tugas



Pembagian tugas

Diisi oleh anggota sesuai pengerjaan aktual — tanpa asumsi peran

ML 2026  •  B2  •  Kelompok 12                                      27

Anggota | NIM | Tugas aktual

Muhamad Akhdan Ramadhan | J0404241102 | [Isi sendiri]

Thevan Erlangga | J0404241073 | [Isi sendiri]

Fachri Abyasa Tarid | J0404241136 | [Isi sendiri]

Seluruh anggota wajib memahami konsep, dataset, preprocessing, algoritma, evaluasi, dan aplikasi.

## Slide 28: Referensi jurnal



Referensi jurnal

DOI dan teks lengkap tersedia di docs/STUDI_LITERATUR.md

ML 2026  •  B2  •  Kelompok 12                                      28

[1] Sana et al. (2022) — PLOS ONE
10.1371/journal.pone.0278095

[2] Y., Ly & Son (2022) — PLOS ONE
10.1371/journal.pone.0267935

[3] Bilal et al. (2022) — PeerJ Computer Science
10.7717/peerj-cs.854

[4] Zhou et al. (2023) — PLOS ONE
10.1371/journal.pone.0292466

[5] Khattak et al. (2023) — Scientific Reports
10.1038/s41598-023-44396-w

## Slide 29: Source code & berkas pengumpulan



Source code & berkas pengumpulan

Format folder: ML2026_B2_Kelompok12_PrediksiCustomerChurn

ML 2026  •  B2  •  Kelompok 12                                      29

• PPT: docs/ML2026_B2_Kelompok12_PrediksiCustomerChurn.pptx
• EDA: docs/eda/EDA.md • notebook: projekk.ipynb
• Lima jurnal & tabel: docs/STUDI_LITERATUR.md • docs/jurnal/
• Naskah demo ≤7 menit: docs/NASKAH_VIDEO_DEMO.md
• Pembagian tugas: isi pada slide 27; video asli direkam anggota.

Repository: https://github.com/makhdanramadhan-ui/Machine-Learning-Project
https://machine-learning-project-u8yovshrqrc5tm5s2y2qto.streamlit.app/