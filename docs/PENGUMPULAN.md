# Berkas pengumpulan — Kelompok 12, B2

Gunakan nama folder **ML2026_B2_Kelompok12_PrediksiCustomerChurn**.

| Komponen | Lokasi / tautan |
|---|---|
| Source code | https://github.com/makhdanramadhan-ui/Machine-Learning-Project |
| Dataset | `../Telco-Customer-Churn.csv`; https://www.kaggle.com/datasets/blastchar/telco-customer-churn |
| Model | `../model_churn.pkl`, `../calibrator.pkl`, metadata deployment |
| EDA | `eda(explaratory data analysis)/EDA.md`; `../01_EDA.ipynb` |
| Lima jurnal | `STUDI_LITERATUR.md`, `referensi.bib`, `jurnal/` |
| Tabel studi literatur | `tabel_studi_literatur.csv`; tabel lengkap pada `STUDI_LITERATUR.md` |
| Aplikasi | https://machine-learning-project-u8yovshrqrc5tm5s2y2qto.streamlit.app/ |

## Yang diisi/direkam anggota

1. Pembagian tugas aktual tiap anggota sudah diisi di **slide 15** PPT dan tabel di bawah.
2. Rekam video asli dengan aplikasi benar-benar dijalankan; cek
   durasi final **≤7 menit**. Cantumkan link video/berkas MP4 saat pengumpulan.
3. Cek ulang bahwa materi menjelaskan hasil dan keterbatasan yang dipahami
   seluruh anggota; gunakan aplikasi untuk membaca contoh kesalahan prediksi.

## Anggota dan Pembagian Tugas

| Anggota | NIM | Pembagian Tugas |
|---|---|---|
| Muhamad Akhdan Ramadhan | J0404241102 | Preprocessing data, training dan evaluasi tiap model, pembuatan serta deployment aplikasi Streamlit |
| Thevan Erlangga | J0404241073 | Pencarian dataset dan penyusunan PPT laporan project |
| Fachri Abyasa Tarid | J0404241136 | Pencarian 5 jurnal studi literatur dan penyusunan EDA |

## Reproduksi

`01_EDA.ipynb` membangun EDA; `02_Training_Model.ipynb` lalu
`03_Kalibrasi_dan_Threshold.ipynb` membangun ulang model dan metadata;
`04_Penjelasan_Aplikasi.ipynb` memperagakan alur prediksi aplikasi;
`python -m unittest discover -s tests -v` memeriksa aplikasi. Model memakai
dependency terkunci dan Python ≥3.12. Laporan dibuat dari hasil aktual tersimpan.
