# Naskah Video Demo — Kelompok 12, Kelas B2

**Target durasi: 6 menit 40 detik; batas pengumpulan 7 menit.**
Pembaca segmen dipilih sendiri oleh kelompok. Seluruh anggota diperkenalkan;
peran pengerjaan aktual tidak diasumsikan dalam naskah ini.

## Persiapan rekaman

- Buka [aplikasi live](https://machine-learning-project-u8yovshrqrc5tm5s2y2qto.streamlit.app/)
  dan pastikan sudah siap sebelum mulai merekam.
- Buka PPT `ML2026_B2_Kelompok12_PrediksiCustomerChurn.pptx`.
- Siapkan `docs/template_pelanggan.csv` (dua contoh input valid, tanpa hasil)
  dan CSV invalid dengan kolom `tenure` dihapus untuk demonstrasi validasi.
- `docs/contoh_demo.csv` berisi hasil contoh yang dihitung aktual: profil pertama
  sekitar **74,79% CHURN**, profil kedua **0,99% TETAP** pada artefak saat ini.
- Isi sendiri tabel pembagian tugas pada PPT. Rekam layar dan suara nyata;
  demonstrasi wajib memperlihatkan klik/input/upload, bukan rangkaian screenshot.
- Latihan dengan timer; angka durasi berikut adalah target, bukan klaim durasi rekaman jadi.

## 00:00–00:25 — Perkenalan dan judul (25 detik)

**Layar:** slide 1; perkenalkan masing-masing anggota secara bergantian.

> Halo, kami Kelompok 12 dari kelas B2. Saya Muhamad Akhdan Ramadhan,
> NIM J0404241102. Saya Thevan Erlangga, NIM J0404241073. Saya Fachri Abyasa Tarid,
> NIM J0404241136. Project kami adalah Prediksi Customer Churn Telco,
> dengan perbandingan tiga model dan implementasi aplikasi Streamlit.

## 00:25–00:55 — Latar belakang dan tujuan (30 detik)

**Layar:** slide 2–3.

> Churn berarti pelanggan berhenti berlangganan. Prediksi risiko dapat membantu
> menentukan prioritas tindak lanjut pelanggan. Tantangannya, pelanggan churn
> merupakan kelas minoritas sehingga accuracy saja belum cukup. Tujuan kami
> adalah memahami data, membandingkan tiga algoritma, dan membuat aplikasi
> yang menampilkan keputusan serta probabilitas secara konsisten.

## 00:55–01:15 — Studi literatur (20 detik)

**Layar:** slide 4–5, ringkas; daftar DOI pada slide 28 tersedia untuk rujukan.

> Kami memakai lima jurnal tentang churn telekomunikasi. Sana dan rekan membahas
> transformasi data dan berbagai classifier, sementara studi SVM dan ensemble
> menekankan evaluasi kelas churn. Artikel BiLSTM-CNN menjadi alternatif
> pengembangan. Hasil jurnal tidak kami samakan dengan hasil project karena
> dataset dan protokol pengujiannya berbeda.

## 01:15–01:55 — Dataset dan EDA (40 detik)

**Layar:** slide 6–7, lalu 8 dan 11.

> Dataset berasal dari IBM Telco Customer Churn di Kaggle, sebanyak 7.043
> pelanggan dan 21 kolom. Targetnya Churn Yes atau No. Ada sebelas TotalCharges
> kosong; cohort pemodelan kami berisi 7.032 pelanggan dengan 18 fitur input.
> Sekitar 26,6 persen adalah churn. EDA menunjukkan hubungan churn dengan
> kontrak, tenure, internet, dan pembayaran. Grafik hubungan target memakai
> data train saja. Tidak ada outlier numerik menurut IQR; profil identik dengan
> customerID berbeda dipertahankan dan dicatat sebagai keterbatasan.

## 01:55–02:35 — Preprocessing dan training (40 detik)

**Layar:** slide 13–15.

> customerID dihapus. TotalCharges tidak diminta untuk menyederhanakan input;
> kami belum menguji manfaat penghapusan fitur dengan ablation. Fitur numerik
> memakai StandardScaler dan kategori memakai OneHotEncoder, dalam pipeline
> yang fit hanya pada training fold. Split stratified 80:20 menghasilkan 5.625
> train dan 1.407 test. Kami membandingkan Logistic Regression sebagai model
> linear, Decision Tree sebagai pohon aturan, dan Random Forest sebagai
> ensemble, menggunakan GridSearchCV lima fold dengan scoring F1 churn.

## 02:35–03:20 — Evaluasi dan pemilihan model (45 detik)

**Layar:** slide 16–19.

> Logistic Regression dipilih karena CV-F1 training tertinggi, 0,6304,
> dibanding Random Forest 0,6260 dan Decision Tree 0,6147. Pada test model inti,
> Decision Tree mempunyai recall tertinggi dan Random Forest accuracy tertinggi.
> Random Forest menunjukkan overfitting karena F1 train jauh lebih tinggi
> daripada test. Untuk aplikasi, probabilitas dikalibrasi sigmoid dan threshold
> 0,32 dipilih dari prediksi out-of-fold training, tanpa memilih dari test.
> Konfigurasi aplikasi memperoleh accuracy 75,69 persen, precision 53,09 persen,
> recall 73,53 persen, dan F1 0,6166.

## 03:20–04:20 — Demo prediksi single (60 detik)

**Layar:** aplikasi live → tab Prediksi Single. Isi profil pertama pada template.

| Field | Nilai profil demo |
|---|---|
| gender / SeniorCitizen | Male / No |
| Partner / Dependents | No / No |
| tenure | 2 |
| PhoneService / MultipleLines | Yes / No |
| InternetService | Fiber optic |
| OnlineSecurity / OnlineBackup / DeviceProtection / TechSupport | No / No / No / No |
| StreamingTV / StreamingMovies | Yes / Yes |
| Contract / PaperlessBilling | Month-to-month / Yes |
| PaymentMethod / MonthlyCharges | Electronic check / 95 |

> Ini aplikasi kami yang dijalankan langsung. Pengguna memasukkan 18 fitur.
> Opsi add-on menyesuaikan layanan internet dan telepon. Kami masukkan profil
> pelanggan baru dengan kontrak bulanan dan fiber, kemudian klik Prediksi
> Sekarang. Probabilitas sekitar 74,79 persen sehingga diprediksi CHURN.
> Threshold adalah batas keputusan: probabilitas minimal 32 persen diberi
> label CHURN. Risiko tinggi adalah kategori tampilan untuk probabilitas
> minimal 60 persen. Saran retensi di bawah hasil berbasis aturan profil,
> bukan bukti bahwa penawaran pasti mengurangi churn.

**Aksi:** ubah tenure 2→3. Tunjukkan hasil lama disembunyikan; klik prediksi ulang.

> Ketika input berubah, aplikasi meminta prediksi ulang agar hasil tidak tertukar
> dengan input sebelumnya.

## 04:20–05:10 — Demo CSV massal dan validasi (50 detik)

**Layar:** tab Prediksi Batch. Download template, upload template valid, download hasil,
kemudian upload CSV invalid tanpa tenure.

> Untuk prediksi massal, pengguna mengunduh template lalu mengunggah CSV.
> Dua profil ini menghasilkan satu CHURN dan satu TETAP. Kolom tambahan
> seperti customerID dan Churn tidak dipakai model. Hasil memuat probabilitas,
> label, risiko, dan threshold; semua baris dapat diunduh. Sekarang kami unggah
> CSV tanpa tenure. Aplikasi memberi pesan kolom wajib yang kurang, bukan
> langsung error atau membuang pelanggan diam-diam. Nilai kosong, kategori
> salah, dan layanan yang tidak konsisten juga diperiksa.

## 05:10–05:55 — Demo dashboard dan kesalahan model (45 detik)

**Layar:** tab Dashboard & Model → evaluasi aplikasi → tabel model inti → train/test.

> Dashboard menampilkan evaluasi konfigurasi yang benar-benar dipakai aplikasi,
> terpisah dari tiga model inti. Dari 374 pelanggan churn pada test, 275 terdeteksi
> dan 99 terlewat; ada 243 false alarm. Threshold 0,32 menangkap lebih banyak
> churn dibanding 0,50, dengan konsekuensi false alarm bertambah. Brier turun
> dari 0,1741 ke 0,1414 setelah kalibrasi. Tabel validation fold dan gap
> train–test membantu menjelaskan pemilihan model serta indikasi overfitting.

**Jika masih ada waktu dalam segmen ini:** tunjukkan tab EDA & Dokumentasi sebagai
akses tambahan ke grafik dan laporan; tidak perlu membacakan seluruh grafik.

## 05:55–06:25 — Kesimpulan dan keterbatasan (30 detik)

**Layar:** slide 25–26.

> Kesimpulannya, kami menghasilkan model yang dapat diuji ulang dan aplikasi
> single serta batch yang berjalan. Pemilihan model dan threshold menggunakan
> data training, kemudian dievaluasi pada holdout. Keterbatasannya adalah satu
> dataset historis, eksklusi pelanggan tenure nol, profil identik lintas split,
> serta FP dan FN yang masih ada. Pengembangan berikutnya mencakup validasi
> eksternal, ablation fitur, tuning, dan threshold berdasarkan biaya retensi nyata.

## 06:25–06:40 — Penutup (15 detik)

**Layar:** slide 29 / tautan repository dan deployment.

> Source code, dataset, model, EDA, dan referensi tersedia di repository kami.
> Link aplikasi dapat digunakan untuk mencoba prediksi. Terima kasih.

## Catatan untuk tanya jawab

- CV-F1 memilih **model inti**, bukan hasil test tertinggi.
- Threshold 32% **bukan accuracy 32%** dan bukan probabilitas pasti churn.
- Precision/recall/F1 yang dilaporkan adalah kelas churn=1, bukan weighted average.
- Threshold hanya mengubah label; ROC-AUC/Brier tetap sama untuk probabilitas yang sama.
- Tidak mengklaim seluruh preprocessing otomatis optimal; penghapusan TotalCharges belum diuji ablation.
- Durasi aktual bergantung kecepatan berbicara dan interaksi; lakukan latihan lalu periksa rekaman ≤7 menit.
