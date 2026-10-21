---
version: 1
slug: "app-py"
primary_target: "app.py"
related_targets: []
---

# Permukaan: aplikasi prediksi churn (Streamlit)

## Scope dan mode

Satu permukaan: aplikasi Streamlit untuk prediksi churn pelanggan telco.
Mode **Operate** — pengunjung datang untuk mengerjakan tugas, bukan untuk
menilkai tampilan. Empat area kerja (prediksi single, prediksi batch CSV,
dashboard model, EDA dan dokumentasi) dipertahankan apa adanya.

## Audiens, tugas, aksi, batasan

- **Audiens utama:** dosen atau kurator yang menilai tugas (dikonfirmasi user).
- **Tugas:** memeriksa apakah model churn dapat dipercaya, dan mencoba prediksi.
- **Aksi:** isi 18 fitur pelanggan, klik Prediksi, baca risiko dan ambangnya.
- **Bukti:** angka metrik dari `deployment_info.json`, ambang 0,32 terpilih dari
  F1 out-of-fold data latih, jejak kalibrasi, dan SHA-256 artefak model.
- **Batasan:** bahasa Indonesia; isi dan angka existing tidak boleh berubah;
  fungsi dan tata letak widget dipertahankan; hanya lapisan visual yang diganti.

## Arah terpilih

**Lembar Gambar Teknik** — aplikasi sebagai satu lembar gambar teknik: hairline
sebagai pemisah, title block sebagai pembawa identitas model, dan satu tinta
biru teknis sebagai satu-satunya warna.

### Momen yang diingat

Title block: pita sel berhairline yang selalu terlihat di atas lembar, memuat
model, ambang, CV-F1, akurasi, precision, recall, F1, ROC-AUC, Brier, ukuran
data, versi sklearn, dan hash SHA-256 model. Penilai membaca kartu model tanpa
mencari.

### Raises yang diterima

- **Dari Peta Taman Zo:** satu geometri mengatur layout, art, dan state —
  geometri title block menjadi armature seluruh lembar, bukan kotak metadata terpisah.
- **Dari Dompet Tiket Jet Age:** state mem-stempel dirinya — prediksi basi dibatalkan eksplisit, tidak pernah diam-diam diganti.
- **Dari Kartu Eksposur Darkroom:** ramp tonal sebelas langkah sebagai satu-satunya token nada — probabilitas digambar pada skala terukur, bukan tiga warna terpisah.

### Decision round

Challenger yang diper wrestle: Katalog Desain — Bagian Plate (competitive),
Manual Kotak Ber-tab (competitive), Spesimen Grid Crouwel (competitive). Declined:
Peta Taman Zo, Dompet Tiket Jet Age, Kartu Eksposur Darkroom — ketiganya tetap
donor disiplinnya lewat tiga raise di atas.

## Direction contract

**THESIS:** Aplikasi ini menolak susunan bawaan kategori — hero bergradien di
atas baris kartu metrik — dan menggantinya dengan satu lembar gambar teknik:
title block yang membawa identitas model, hairline sebagai satu-satunya
pemisah, dan satu warna aksen.

**OWN-WORLD:** Kertas `#F7F6F2` (terang) / `#14161A` (gelap), tinta `#16181A`
/ `#E9E7E2`, satu tinta biru teknis `#1F4FD8` / `#7E9BFF`, hairline `#C9C4B8` /
`#33373E`, ramp nada abu sebelas langkah untuk besaran risiko. Huruf Archivo
(heading dan isi) dan JetBrains Mono (label terukur dan angka tabular), keduanya
di-host sendiri di `static/fonts/`. Radius panel 8px, kontrol 6px, chip 4px.
Satu hairline 1px, tanpa bayangan. Ikon garis 24x24, stroke 1,5px, satu keluarga.

**STORY:** Pengunjung lebih dulu membaca kartu model, lalu menghitung risiko
satu pelanggan, lalu memverifikasi modelnya di dashboard. Urutan itu terlihat
di layar: identitas model, alat kerja, bukti.

**FIRST VIEWPORT:** Baris atas berisi nama produk di kiri dan pengalih tema di
kanan; di bawahnya satu kalimat tujuan maksimal 72ch; lalu title block sebagai
pita sembilan sel (model, ambang, CV-F1, akurasi, precision, recall, F1,
ROC-AUC, Brier) dengan strip mikro mono (data latih, data uji, fitur,
kalibrasi, sklearn, SHA-256); lalu rail empat tab dengan ikon garis; lalu area
kerja form 18 fitur dalam tiga kolom, dengan tombol Prediksi tinta penuh.

**FORM:** Lembar Gambar Teknik dengan title block. Roll arah: seed `bd66d2a3`
(direction scope, mode operate), dapat diulang dengan
`impeccable concept-seed --scope direction --mode operate --from bd66d2a3 --candidate-count 7`.

**FINISH:** unreviewed and undocumented is unfinished; this build ends with the
finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.

## Keputusan yang belum ditutup

- Huruf Archivo dan JetBrains Mono di-host sendiri lewat `static/fonts/`. Bila
  static serving tidak aktif di lingkungan deploy, halaman jatuh ke stack
  sistem tanpa mengubah tata letak.
- Grafik EDA adalah plate putih yang direkat ke lembar; di tema gelap tetap
  putih, seperti cetakan yang dijepit di atas meja gelap.
