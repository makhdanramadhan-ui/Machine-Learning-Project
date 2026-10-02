# Berkas pengumpulan — Kelompok 12, B2

Gunakan nama folder **ML2026_B2_Kelompok12_PrediksiCustomerChurn**.

| Komponen | Lokasi / tautan |
|---|---|
| PPT laporan | `ML2026_B2_Kelompok12_PrediksiCustomerChurn.pptx` |
| Versi PDF | `ML2026_B2_Kelompok12_PrediksiCustomerChurn.pdf` |
| Source code | https://github.com/makhdanramadhan-ui/Machine-Learning-Project |
| Dataset | `../Telco-Customer-Churn.csv`; https://www.kaggle.com/datasets/blastchar/telco-customer-churn |
| Model | `../model_churn.pkl`, `../calibrator.pkl`, metadata deployment |
| EDA dan notebook | `eda/EDA.md`; `../projekk.ipynb` |
| Lima jurnal | `STUDI_LITERATUR.md`, `referensi.bib`, `jurnal/` |
| Tabel studi literatur | `tabel_studi_literatur.csv`; tabel lengkap pada `STUDI_LITERATUR.md` |
| Naskah demo | `NASKAH_VIDEO_DEMO.md`, target 6 menit 40 detik |
| Aplikasi | https://machine-learning-project-u8yovshrqrc5tm5s2y2qto.streamlit.app/ |

## Yang diisi/direkam anggota

1. Isi tugas aktual tiap anggota di **slide 27**; peran sengaja tidak diasumsikan.
2. Rekam video asli dengan aplikasi benar-benar digunakan sesuai naskah; cek
   durasi final **≤7 menit**. Cantumkan link video/berkas MP4 saat pengumpulan.
3. Cek ulang bahwa materi menjelaskan hasil dan keterbatasan yang dipahami
   seluruh anggota; gunakan notebook untuk membaca contoh kesalahan prediksi.

## Anggota

- Muhamad Akhdan Ramadhan — J0404241102
- Thevan Erlangga — J0404241073
- Fachri Abyasa Tarid — J0404241136

## Reproduksi

`python train.py` membangun ulang model dan metadata; `python eda.py` membangun
EDA; `python -m unittest discover -s tests -v` memeriksa aplikasi. Model memakai
dependency terkunci dan Python ≥3.12. Laporan dibuat dari hasil aktual tersimpan.
