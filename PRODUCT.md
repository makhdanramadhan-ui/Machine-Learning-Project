# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

**Pengguna utama: dosen atau kurator yang menilai tugas** (dikonfirmasi user, 21 Okt 2026).
Mereka membuka aplikasi untuk memeriksa apakah model churn ini andal dan apakah
penyajian angka metriknya jujur — bukan untuk jelajah.

Pengguna sekunder: anggota Kelompok 12 sendiri yang memakai app untuk demo dan
menjalankan eksperimen ulang, serta pembaca luar yang membuka tautan Streamlit
dari repository GitHub tanpa konteks tugas.

## Product Purpose

Memperkirakan churn pelanggan telco dari IBM Telco Customer Churn (7.043 baris),
dengan memuat model Logistic Regression yang dikalibrasi sigmoid dan ambang
keputusan 0,32 yang dipilih dari F1 out-of-fold data latih. Keberhasilan berarti
penilai bisa melihat, memverifikasi, dan mencoba prediksi tanpa perlu membaca
kode; angka metrik dan setiap asumsi metodologis terlihat terbuka, bukan
disembunyikan di balik klaim.

## Positioning

Mekanisme pembeda: probabilitas yang **sudah dikalibrasi** (sigmoid, Brier
0,1741 → 0,1414) dengan ambang yang **tidak** 0,50 dan dipilih hanya dari data
latih, plus jejak audit out-of-fold dan verifikasi SHA-256 artefak model terhadap
metadata evaluasi. Aplikasi ini menampilkan trade-off precision–recall secara
terbuka, termasuk acknowledge bahwa konfigurasi tidak unggul pada semua metrik.

## Operating Context

- Tugas mata kuliah ML, semester 5, kelas B2, IPB — Kelompok 12.
- Dinilai lewat presentasi, video demo (maks. 7 menit), dan peninjauan repo.
- Demo berlangsung di depan kelas: presenter buka tautan Streamlit di laptop.
- Tiga anggota: Muhamad Akhdan Ramadhan (J0404241102), Thevan Erlangga
  (J0404241073), Fachri Abyasa Tarid (J0404241136).
- Deploy: Streamlit Community Cloud, branch `main`, entrypoint `app.py`,
  Python ≥ 3.12, artefak model ikut disimpan di repository.
- Bahasa antarmuka: **Indonesia**, seluruhnya.
- Desktop dan mobile sama-sama penting (dikonfirmasi user, 21 Okt 2026).

## Capabilities and Constraints

- Empat area kerja: Prediksi Single, Prediksi Batch (CSV), Dashboard & Model,
  EDA & Dokumentasi.
- 18 fitur input. Opsi add-on terkunci otomatis mengikuti layanan telepon dan
  internet yang dipilih.
- Ambang 0,32: CHURN bila probabilitas ≥ 32%. Kategori tampilan RENDAH < 32%,
  SEDANG 32–60%, TINGGI ≥ 60%. Kategori risiko **bukan** target klasifikasi
  tambahan.
- Validasi input: kolom wajib, angka kosong/non-numerik/tak berhingga, rentang
  angka, kategori tak dikenal, header duplikat, konsistensi layanan. Batch
  ditolak utuh dengan nomor baris — tidak ada penghapusan baris diam-diam.
- Acuan tagihan (median, Q1–Q3, min–max) berasal dari training set, bukan
  tarif pasar.
- Hasil lama disembunyikan saat input berubah sampai diprediksi ulang.
- Batasan yang harus dinyatakan jujur: satu dataset; akurasi baseline 0,7342;
  Random Forest overfit (F1 train 0,8217 vs test 0,6096); TotalCharges dihapus
  tanpa eksperimen ablation; saran retensi belum diuji kausal; prediksi TETAP
  bukan jaminan loyalitas.
- Batas teknis: Streamlit 1.64, Python 3.14 lokal, pandas/matplotlib/joblib.
  Deployment di Streamlit Community Cloud — aplikasi harus tetap jalan hanya
  dari artefak yang ada di repository, tanpa training ulang.

## Brand Commitments

- Nama produk: "Prediksi Customer Churn — Telco".
- Identitas kelompok dan NIM wajib tampil di footer (lihat footer saat ini).
- Footer **tidak** boleh memuat "Built with ❤️ Streamlit" atau kalimat
  sejenis — dihapus atas permintaan user (sesi opencode, Okt 2026).
- Klaim harus jujur: hasil evaluasi tidak boleh dilebih-lebihkan; ambang 0,32
  dinyatakan eksplisit beserta konsekuensinya.

## Evidence on Hand

- `Telco-Customer-Churn.csv` — 7.043 baris, 21 kolom, dari IBM/Kaggle.
- `model_info.json`, `deployment_info.json`, `calib_info.json` — metrik,
  ambang, jejak tuning, versi sklearn 1.9.1, hash SHA-256 artefak.
- `hasil_perbandingan.csv`, `cv_detail.csv` — perbandingan tiga model inti dan
  F1 per sesi validasi.
- `docs/eda(explaratory data analysis)/` — tujuh grafik EDA dengan interpretasi,
  kamus variabel, pemeriksaan kualitas data.
- `docs/STUDI_LITERATUR.md`, `docs/referensi.bib`, `docs/jurnal/` — lima jurnal
  dengan teks lengkap.
- `docs/ML2026_B2_Kelompok12_PrediksiCustomerChurn.pptx` — 29 slide.
- `projekk.ipynb` — notebook terkini yang sudah dieksekusi.
- Tidak ada testimoni, logo, atau branding pihak ketiga. Jangan mengarangnya.

## Product Principles

1. **Angka harus bisa ditelusuri.** Setiap metrik menyebut mana yang dihitung
   pada data latih dan mana pada data uji.
2. **Kekurangan diakui, bukan disembunyikan.** Trade-off dan keterbatasan tampil
   di tempat yang sama dengan klaim.
3. **Penilai tidak boleh terjebak.** Satu prediksi selesai dalam beberapa detik
   tanpa perlu memahami machine learning.
4. **Tidak ada garnish.** Hiasan visual tidak boleh menambah apa pun ke
   keputusan penilai.

## Accessibility & Inclusion

- Bahasa Indonesia; istilah teknis selalu disertai penjelasan singkat.
- Kontras teks dan kontrol harus tetap terbaca di kedua tema (terang dan gelap).
- Fokus keyboard, label kontrol, dan state error harus tetap utuh setelah
   gaya dirapikan.
- Angka pada tabel harus memakai tabular figures agar kolom sejajar.
