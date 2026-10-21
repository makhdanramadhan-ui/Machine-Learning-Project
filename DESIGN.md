---
name: "Prediksi Customer Churn — Telco"
description: "Lembar gambar teknik: hairline sebagai satu-satunya pemisah, title block sebagai pembawa identitas model, dan satu tinta biru teknis."
colors:
  paper: "#F7F6F2"
  paper-dark: "#14161A"
  sheet: "#FFFFFF"
  sheet-dark: "#1B1E23"
  ink: "#16181A"
  ink-dark: "#E9E7E2"
  ink2: "#3C3F45"
  ink2-dark: "#C6C4BE"
  muted: "#6B6A64"
  muted-dark: "#8E8C86"
  rule: "#C9C4B8"
  rule-dark: "#33373E"
  rule-soft: "#E3E0D8"
  rule-soft-dark: "#262A30"
  accent: "#1F4FD8"
  accent-dark: "#7E9BFF"
  accent-ink: "#FFFFFF"
  accent-ink-dark: "#14161A"
  accent-soft: "#E4EAFB"
  accent-soft-dark: "#1E2740"
  danger: "#B3272D"
  danger-dark: "#E8746F"
  ramp1: "#EDEBE4"
  ramp1-dark: "#232830"
  ramp2: "#D9D6CD"
  ramp2-dark: "#2E333C"
  ramp4: "#C2BEB3"
  ramp4-dark: "#454B54"
  ramp6: "#9C988D"
  ramp6-dark: "#6E747D"
  ramp8: "#6E6A61"
  ramp8-dark: "#9DA3AB"
  ramp10: "#3A3833"
  ramp10-dark: "#D2D0CA"
  band-low-bg: "#EDEBE4"
  band-low-bg-dark: "#232830"
  band-low-fg: "#16181A"
  band-low-fg-dark: "#E9E7E2"
  band-mid-bg: "#C2BEB3"
  band-mid-bg-dark: "#454B54"
  band-mid-fg: "#16181A"
  band-mid-fg-dark: "#E9E7E2"
  band-high-bg: "#16181A"
  band-high-bg-dark: "#E9E7E2"
  band-high-fg: "#FFFFFF"
  band-high-fg-dark: "#14161A"
typography:
  display:
    fontFamily: "'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif"
    fontSize: "2.5rem"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.032em"
  headline:
    fontFamily: "'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif"
    fontSize: "1.32rem"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.022em"
  title:
    fontFamily: "'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif"
    fontSize: "1.02rem"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-0.015em"
  body:
    fontFamily: "'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif"
    fontSize: "0.85rem"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "-0.005em"
  label:
    fontFamily: "'JetBrains Mono', ui-monospace, monospace"
    fontSize: "0.625rem"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.11em"
  mono:
    fontFamily: "'JetBrains Mono', ui-monospace, monospace"
    fontSize: "0.85rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0"
  control:
    fontFamily: "'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif"
    fontSize: "0.84rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.005em"
  metric:
    fontFamily: "'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif"
    fontSize: "1.55rem"
    fontWeight: 650
    lineHeight: 1.15
    letterSpacing: "-0.025em"
    fontFeature: "'tnum' 1, 'cv05' 1"
  caption:
    fontFamily: "'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif"
    fontSize: "0.78rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "-0.005em"
  field-label:
    fontFamily: "'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif"
    fontSize: "0.74rem"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.005em"
  switch:
    fontFamily: "'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif"
    fontSize: "0.72rem"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "-0.005em"
  micro-label:
    fontFamily: "'JetBrains Mono', ui-monospace, monospace"
    fontSize: "0.58rem"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "0.11em"
  scale-readout:
    fontFamily: "'JetBrains Mono', ui-monospace, monospace"
    fontSize: "0.66rem"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.08em"
  marker-chip:
    fontFamily: "'JetBrains Mono', ui-monospace, monospace"
    fontSize: "0.68rem"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "0"
  unit:
    fontFamily: "'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif"
    fontSize: "1.15rem"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  display-compact:
    fontFamily: "'Archivo', 'Segoe UI', system-ui, -apple-system, sans-serif"
    fontSize: "2.1rem"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.032em"
rounded:
  panel: "8px"
  control: "6px"
  chip: "4px"
  marker: "3px"
spacing:
  xs: "0.25rem"
  sm: "0.5rem"
  md: "0.75rem"
  lg: "1.1rem"
  xl: "1.5rem"
  xxl: "2.2rem"
  xxxl: "3.5rem"
components:
  title-block:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "0.6rem 0.75rem 0.62rem"
  title-block-cell-key:
    typography: "{typography.label}"
    textColor: "{colors.muted}"
  title-block-cell-value:
    typography: "{typography.title}"
    textColor: "{colors.ink}"
  title-block-strip:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.muted}"
    padding: "0.5rem 0.75rem"
  tab-rail:
    typography: "{typography.label}"
    textColor: "{colors.muted}"
  tab-rail-active:
    typography: "{typography.label}"
    textColor: "{colors.ink}"
    height: "2px"
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.control}"
    typography: "{typography.control}"
    padding: "0.5rem 1rem"
  button-primary-hover:
    backgroundColor: "{colors.ink2}"
    textColor: "{colors.paper}"
  button-secondary:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    typography: "{typography.control}"
    padding: "0.5rem 1rem"
  button-secondary-hover:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
  input-text:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    typography: "{typography.body}"
  input-label:
    typography: "{typography.label}"
    textColor: "{colors.muted}"
  theme-toggle:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.muted}"
    rounded: "{rounded.control}"
  theme-toggle-active:
    backgroundColor: "{colors.accent-soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.chip}"
  risk-chip-low:
    backgroundColor: "{colors.band-low-bg}"
    textColor: "{colors.band-low-fg}"
    rounded: "{rounded.chip}"
    typography: "{typography.label}"
    padding: "0.28rem 0.5rem"
  risk-chip-mid:
    backgroundColor: "{colors.band-mid-bg}"
    textColor: "{colors.band-mid-fg}"
    rounded: "{rounded.chip}"
    typography: "{typography.label}"
    padding: "0.28rem 0.5rem"
  risk-chip-high:
    backgroundColor: "{colors.band-high-bg}"
    textColor: "{colors.band-high-fg}"
    rounded: "{rounded.chip}"
    typography: "{typography.label}"
    padding: "0.28rem 0.5rem"
  verdict-block:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "1rem 1.15rem 1.05rem"
  verdict-figure:
    typography: "{typography.display}"
    textColor: "{colors.ink}"
  calibrated-scale:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "0.85rem 1rem 0.7rem"
  calibrated-scale-track:
    height: "26px"
    rounded: "{rounded.chip}"
  confusion-matrix:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
  confusion-matrix-hit:
    backgroundColor: "{colors.ramp1}"
  summary-strip:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.panel}"
    padding: "0.62rem 0.8rem"
  recommendation-item:
    typography: "{typography.body}"
    textColor: "{colors.ink2}"
    padding: "0.62rem 0.1rem"
  eda-plate:
    backgroundColor: "#FFFFFF"
    rounded: "{rounded.panel}"
  eda-plate-caption:
    typography: "{typography.caption}"
    textColor: "{colors.muted}"
  section-title:
    typography: "{typography.title}"
    textColor: "{colors.ink}"
  alert-message:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink2}"
    rounded: "{rounded.control}"
    typography: "{typography.body}"
  sheet-footer:
    typography: "{typography.mono}"
    textColor: "{colors.muted}"
    padding: "0.85rem 0 0"
---

# Design System: Prediksi Customer Churn — Telco

<!-- impeccable:design-schema 1 -->

Sistem visual ini dicatat dari build yang sudah jadi. Semua nilai di bawah dibaca
langsung dari `ui.py` (token `LIGHT`/`DARK`, stylesheet `_BASE_CSS`, dan fungsi
komponen) serta `eda.py` (palet grafik), bukan dari rencana.

## Overview

**Creative North Star: "Lembar Gambar Teknik"**

Aplikasi ini bukan dasbor. Ia adalah satu lembar gambar teknik: satu bidang
kertas yang berisi title block sebagai pembawa identitas model, hairline 1px
sebagai satu-satunya pemisah, dan satu tinta biru teknis sebagai satu-satunya
warna kromatik. Evaluator membuka aplikasi untuk memeriksa apakah model
churn bisa dipercaya, dan lembar gambar teknik memberi jawaban atas
pertanyaan itu secara harfiah: model apa, ambang berapa, performannya
bagaimana, dan di mana buktinya. Urutan baca yang dibangun di layar adalah
identitas model, lalu alat kerja, lalu bukti.

Kepadatan dokumen ini teknis, bukan sekadar dekoratif. Angka selalu tabular sehingga
kolom bisa dibandingkan sekilas, dan setiap label yang menyebut sebuah
pengukuran ditulis dalam huruf monospace huruf besar dengan spasi lebar,
seperti anotasi dimensi pada gambar teknik. Karena itu, dua huruf dengan
peran yang berbeda: Archivo untuk kalimat dan angka, JetBrains Mono
untuk label terukur, kode, dan penanda. Keduanya di-host sendiri di
`static/fonts/` sebagai woff2 variabel, jadi halaman tidak bergantung pada
stylesheet pihak ketiga.

Kedalaman tidak dibangun dari bayangan. Dua nada permukaan saja yang
membedakan lembar dari panel di atasnya, dan garis rambut yang memisahkan
sel. Tidak ada gradien, tidak ada kaca, tidak ada emoji, tidak ada warna
lalu lintas untuk menandai risiko. Risiko dibaca sebagai posisi pada satu
ramp nada abu, bukan sebagai tiga warna berbeda.

**Key Characteristics:**

- Satu tinta biru teknis; sisanya satu ramp abu yang dibaca sebagai besaran.
- Hairline 1px sebagai satu-satunya pemisah; tanpa bayangan di seluruh sistem.
- Title block sembilan sel sebagai identitas model, selalu di atas lembar.
- Angka tabular, label mono huruf besar, spasi lebar.
- Dua nada permukaan (kertas dan panel) yang membawa kedalaman.
- Radius pendek: 8px panel, 6px kontrol, 4px chip, 3px penanda.

**Catatan penyimpangan dari kontrak arah.** Kontrak arah menyebut ramp nada
sebelas langkah. Build yang jadi hanya mendeklarasikan enam jangkar ramp
(`ramp1`, `ramp2`, `ramp4`, `ramp6`, `ramp8`, `ramp10`); angka genap dan `ramp1`
yang dipakai, langkah ganjil di antaranya tidak pernah didefinisikan sebagai
token. Yang tercatat di sini adalah enam jangkar yang benar-benar ada di
`ui.py`. Aturan jaraknya tetap berlaku: `ramp1` selalu menempel pada permukaan
lembar, `ramp10` selalu menempel pada tinta.

## Colors

Palet ini satu tinta biru teknis di atas kertas hangat, dengan satu ramp abu
untuk besaran; tidak ada warna lain yang berdiri sendiri.

### Primary

- **Tinta Biru Teknis** (`accent`, #1F4FD8 terang / #7E9BFF gelap): satu-satunya
  warna kromatik. Dipakai untuk tautan, cincin fokus, tombol tema yang aktif,
  ikon judul bagian, ikon daftar saran, dan batang yang disorot pada grafik
  matplotlib. Tidak pernah dipakai sebagai isian panel atau latar tabel.
- **Tinta di Atas Biru** (`accent-ink`, #FFFFFF terang / #14161A gelap): warna
  teks di atas tinta biru, dipakai pada seleksi teks (`::selection`).
- **Biru Pudar** (`accent-soft`, #E4EAFB terang / #1E2740 gelap): isian
  cincin fokus pada kontrol, tombol tema yang aktif, dan arah kursor pada
  tombol angka.

### Secondary

- **Merah Bahaya** (`danger`, #B3272D terang / #E8746F gelap): satu-satunya
  warna untuk border pesan galat dan sukses. Tidak dipakai untuk menandai
  risiko pelanggan.

### Neutral

- **Kertas Gambar** (`paper`, #F7F6F2 terang / #14161A gelap): latar lembar.
- **Lembar Panel** (`sheet`, #FFFFFF terang / #1B1E23 gelap): latar panel,
  kartu, tabel, dan pita mikro title block.
- **Tinta** (`ink`, #16181A terang / #E9E7E2 gelap): teks utama dan nilai
  angka besar.
- **Tinta Ringan** (`ink2`, #3C3F45 terang / #C6C4BE gelap): teks paragraf
  dan kalimat penjelasan.
- **Tinta Bisu** (`muted`, #6B6A64 terang / #8E8C86 gelap): label, caption,
  dan anotasi mikro.
- **Garis Rambut** (`rule`, #C9C4B8 terang / #33373E gelap): bingkai luar
  panel, title block, tabel, dan garis dasar rail tab.
- **Garis Rambut Halus** (`rule-soft`, #E3E0D8 terang / #262A30 gelap):
  pemisah antar sel di dalam satu panel.
- **Ramp Nada** (`ramp1`, `ramp2`, `ramp4`, `ramp6`, `ramp8`, `ramp10`):
  `#EDEBE4`/`#D9D6CD`/`#C2BEB3`/`#9C988D`/`#6E6A61`/`#3A3833`
  pada tema terang, `#232830`/`#2E333C`/`#454B54`/`#6E747D`/`#9DA3AB`/`#D2D0CA`
  pada tema gelap. Satu keluarga abu untuk besaran: `ramp1` menempel pada
  permukaan lembar, `ramp10` menempel pada tinta, langkah di antaranya
  menandai besaran.
- **Pita Risiko** (`band-low-bg`/`band-low-fg`, `band-mid-bg`/`band-mid-fg`,
  `band-high-bg`/`band-high-fg`): pasangan isian dan teks untuk tiga kategori
  risiko. Isian LOW adalah `ramp1`, isian MID adalah `ramp4`, isian HIGH adalah
  tinta. Teksnya kebalikan dari isiannya.

### Tabel Token Warna

| Token | Tema Terang | Tema Gelap |
| --- | --- | --- |
| `paper` | #F7F6F2 | #14161A |
| `sheet` | #FFFFFF | #1B1E23 |
| `ink` | #16181A | #E9E7E2 |
| `ink2` | #3C3F45 | #C6C4BE |
| `muted` | #6B6A64 | #8E8C86 |
| `rule` | #C9C4B8 | #33373E |
| `rule-soft` | #E3E0D8 | #262A30 |
| `accent` | #1F4FD8 | #7E9BFF |
| `accent-ink` | #FFFFFF | #14161A |
| `accent-soft` | #E4EAFB | #1E2740 |
| `danger` | #B3272D | #E8746F |
| `ramp1` | #EDEBE4 | #232830 |
| `ramp2` | #D9D6CD | #2E333C |
| `ramp4` | #C2BEB3 | #454B54 |
| `ramp6` | #9C988D | #6E747D |
| `ramp8` | #6E6A61 | #9DA3AB |
| `ramp10` | #3A3833 | #D2D0CA |
| `band-low-bg` | #EDEBE4 | #232830 |
| `band-low-fg` | #16181A | #E9E7E2 |
| `band-mid-bg` | #C2BEB3 | #454B54 |
| `band-mid-fg` | #16181A | #E9E7E2 |
| `band-high-bg` | #16181A | #E9E7E2 |
| `band-high-fg` | #FFFFFF | #14161A |

### Named Rules

**The One Ink Rule.** Satu tinta biru teknis adalah satu-satunya warna
kromatik di seluruh aplikasi. Setiap warna lain adalah abu dari ramp yang
sama. Risiko pelanggan tidak pernah memakai merah-amber-hijau, dan aksen
tidak pernah dipakai sebagai isian panel atau pita.

**The Ramp Rule.** Besaran selalu dibaca dari posisi pada ramp, bukan dari
warna lalu lintas. Kalau sebuah besaran butuh langkah ramp yang belum ada,
tambahkan langkah abu, jangan langkah baru berwarna.

**The Ramp Anchor Rule.** `ramp1` selalu menempel pada permukaan lembar dan
`ramp10` selalu menempel pada tinta, di kedua tema. Karena itu, pita
risiko RENDAH selalu paling dekat kertas dan pita TINGGI selalu paling dekat
tinta, apa pun temanya.

## Typography

**Display Font:** Archivo (dengan fallback 'Segoe UI', system-ui, -apple-system,
sans-serif)
**Body Font:** Archivo (fallback yang sama)
**Label/Mono Font:** JetBrains Mono (dengan fallback ui-monospace, monospace)

Kedua huruf di-host sendiri sebagai woff2 variabel di `static/fonts/`
(`archivo-latin.woff2`, `jetbrains-mono-latin.woff2`), dibaca melalui
`@font-face` dengan rentang bobot 400-700 dan `font-display: swap`. Bila
static serving tidak aktif, halaman jatuh ke stack sistem tanpa mengubah tata
letak. Huruf JetBrains Mono juga dipasang sebagai `--font-family-code` sehingga
blok kode dan `st.json` mengikuti keluarga yang sama.

Streamlit memasang huruf temanya sendiri pada isi markdown dan label widget,
sehingga aturan `font-family` pada `body` saja tidak cukup: Archivo dimuat
tetapi tidak terpakai. Karena itu `ui.py`override
`[data-testid="stMarkdownContainer"]` beserta paragraf, span, div, li, dan
heading di dalamnya, plus `[data-testid="stCaptionContainer"]` dan label
widget, memakai `!important`. Elemen yang memakai mono — kunci title block,
strip mikro, kunci matriks, chip risiko, label dan tick skala, chip penanda,
footer — didaftarkan ulang dengan spesifisitas lebih tinggi supaya tidak
kalah oleh aturan umum itu.

**Character:** satu grotesk untuk kalimat dan angka, satu mono untuk hal yang
diukur. Archivo selalu dirapatkan negatif (hingga -0,032em) supaya rapat pada
ukuran kecil; JetBrains Mono untuk label huruf besar selalu dirapatkan positif
(0,08em sampai 0,12em) supaya tidak rapat dan terbaca sebagai anotasi.

### Hierarchy

- **Display** (700, 2,5rem, line-height 1,05): angka probabilitas pada blok
  vonis. Angka terbesar di layar, dan satu-satunya. Satuan persennya 1,15rem
  berbobot 600 dengan warna bisu.
- **Headline** (700, 1,32rem, line-height 1,1): nama produk di kepala lembar.
- **Title** (600, 1,02rem, line-height 1,15): nilai pada title block; versi
  kecil 0,8rem untuk nama model. Judul bagian memakai 1rem berbobot 650.
- **Body** (400, 0,85rem, line-height 1,6, lebar maksimum 72ch untuk kalimat
  tujuan dan 78ch untuk catatan bagian): paragraf, isian formulir, dan
  kalimat pada daftar saran.
- **Label** (500, 0,625rem, tracking 0,11em, huruf besar): kunci sel title
  block, strip mikro, kunci sel matriks konfusi, label skala dan tanda
  centang. Varian label chip 0,66rem berbobot 600 dengan tracking 0,1em,
  label sumbu 0,58rem dengan tracking 0,08em, kunci matriks 0,6rem dengan
  tracking 0,12em.
- **Metric** (650, 1,55rem, line-height 1,15): angka pada matriks konfusi.

Ramp ukuran yang dipakai, tidak ada nilai lain yang boleh muncul:
`2.5rem`, `2.1rem`, `1.55rem`, `1.32rem`, `1.15rem`, `1.02rem`, `0.85rem`,
`0.84rem`, `0.8rem`, `0.78rem`, `0.74rem`, `0.72rem`, `0.68rem`, `0.66rem`,
`0.625rem`, `0.6rem`, `0.58rem`. Di layar kecil display turun ke `2.1rem`;
selain itu ukuran tidak pernah berubah per breakpoint.

### Angka dan bentuk huruf

- `font-feature-settings: 'tnum' 1, 'cv05' 1` dipasang pada `html`, `body`,
  dan wadah aplikasi; angka besar memakai `font-variant-numeric: tabular-nums`
  secara eksplisit.
- Format angka memakai gaya Indonesia: koma untuk desimal, titik untuk
  ribuan (`fmt_num`, `fmt_pct`, `count_text` di `ui.py`).

### Named Rules

**The Measured Number Rule.** Setiap angka yang mungkin dibandingkan antar
kolom memakai angka tabular. Setiap label yang menyebut sebuah pengukuran
ditulis dalam JetBrains Mono huruf besar dengan tracking lebar. Teks biasa
tidak pernah diberi tracking lebar, dan angka tidak pernah diberi huruf
mono kecuali di dalam blok kode.

**The Two-Face Rule.** Hanya dua keluarga huruf yang boleh muncul: Archivo
dan JetBrains Mono. Menambahkan huruf ketiga, memetik ikon emoji, atau
memakai huruf display bawaan sistem akan memecah lembar.

## Layout

Satu kolom lembar lebar, maks 1440px, dengan padding `3.5rem 2.6rem 3rem`
dan jarak antar blok vertikal 0,55rem. Sidebar disembunyikan sepenuhnya
(`section[data-testid="stSidebar"] { display: none; }`) dan toolbar Streamlit
dibuat transparan (opacity .55), sehingga tidak ada kerangka di luar lembar.

Kepala lembar adalah baris flex dengan jarak 2rem: kiri berisi nama produk
dan satu kalimat tujuan (maks 72ch), kanan berisi pengalih tema. Di bawahnya
title block, lalu rail tab, lalu area kerja. Ketiga bagian itu dipisahkan
hanya oleh hairline dan jarak 1,1rem.

- **Title block:** grid `repeat(9, minmax(0, 1fr))`; tiap sel punya padding
  0,6rem 0,75rem 0,62rem dan pemisah `rule-soft`. Strip mikro di bawahnya
  memakai `display: flex; flex-wrap: wrap; gap: 0 1,5rem` di atas latar
  `paper`.
- **Rail tab:** `gap: 0,35rem`, garis bawah `rule`, tiap tab punya
  `margin-right: 1,35rem` dan padding 0,5rem 0 0,55rem. Indikator tab aktif
  setinggi 2px.
- **Panel:** setiap `st.container(border=True)` menjadi kotak hairline penuh
  dengan padding 1,1rem 1,25rem 1,15rem.
- **Formulir 18 fitur:** tiga kolom sama besar; tombol Prediksi duduk di
  kolom tengah baris `1 : 2 : 1` supaya menjadi titik berat yang jelas.
- **Matriks konfusi:** grid `1fr 1fr`; **strip ringkasan:** grid tiga kolom
  sama; **skala probabilitas:** penuh lebar, tinggi track 26px.

### Ritme jarak

Sistem memakai rem longgar, bukan skala ketat. Langkah yang benar-benar
berulang: 0,25rem (tombol angka, chip), 0,5rem (padding sel, padding strip),
0,75rem (padding horizontal title block), 1,1rem (padding panel, jarak
heading), 1,5rem (jarak blok), 2,2rem (jarak footer), 3,5rem (padding atas
lembar).

### Responsif

- **Lebar 900px:** padding kontainer menjadi `1rem 0,9rem 2rem`; kepala
  lembar menjadi satu kolom dengan jarak 0,8rem; grid title block menjadi
  tiga kolom; strip ringkasan menjadi satu kolom; angka vonis turun ke
  2,1rem; tab mengecil ke 0,78rem dengan jarak 0,9rem.
- **Lebar 640px:** grid title block menjadi dua kolom; label di dalam
  segmen skala disembunyikan sehingga hanya batas dan penanda yang tersisa;
  matriks konfusi menjadi satu kolom.

## Elevation & Depth

Sistem ini tidak memakai bayangan. Setiap panel dan expander memaksa
`box-shadow: none`, dan tidak ada aturan `box-shadow` lain selain cincin
fokus pada kontrol (`0 0 0 2px var(--accent-soft)`) serta garis fokus global
`outline: 2px solid var(--accent); outline-offset: 2px`. Tidak ada token
bayangan di kedua tema: `box-shadow` sendiri ditolak sebagai alat kedalaman.
Kedalaman datang dari tiga hal saja: dua nada permukaan (kertas `paper` di
belakang, panel `sheet` di depan), garis rambut 1px, dan ramp nada.

### Cincin fokus

- **Cincin kontrol** (`box-shadow: 0 0 0 2px var(--accent-soft)`): muncul
  pada selectbox, number input, dan text input saat fokus; border kontrol
  bergeser ke `accent` bersamaan waktunya.
- **Garis fokus** (`outline: 2px solid var(--accent); outline-offset: 2px`):
  dipakai pada tombol, tab, dan apa pun yang menerima `:focus-visible`.

### Named Rules

**The Hairline-Only Rule.** Kedalaman ditanggung oleh satu garis rambut 1px
dan perbedaan dua nada permukaan. Tidak ada bayangan, tidak ada glow, tidak
ada gradien, tidak ada kaca. Panel datar adalah keadaan yang benar, bukan
kekurangan yang perlu diperbaiki.

## Shapes

Bahasa bentuknya pendek dan tegas. Empat radius saja yang dipakai:

- **Panel** (8px): title block, panel formulir, expander, blok vonis, skala,
  matriks konfusi, strip ringkasan, tabel data, dan gambar EDA.
- **Kontrol** (6px): selectbox, text input, number input, file uploader,
  tombol, pengalih tema, dan pesan.
- **Chip** (4px): chip risiko, track skala, dan tombol di dalam pengalih tema.
- **Penanda** (3px): kotak nilai pada penanda ambang di skala probabilitas.

Tidak ada bentuk pil, tidak ada lingkaran penuh pada tombol, dan tidak ada
sudut lebih dari 8px. Bingkai luar selalu `1px solid var(--rule)`; pemisah
antar sel di dalam panel selalu `1px solid var(--rule-soft)`. Pesan
peringatan menambah satu garis tegak `3px solid var(--ramp8)` di sisi kiri.
Sudut membulat selalu dipotong rapi: title block, matriks konfusi, strip
ringkasan, dan tabel memakai `overflow: hidden` supaya garis rambut di dalam
sel bertemu rapi di ujung yang membulat. Penanda ambang pada skala adalah garis
2px dengan kepala bulat 8px, satu-satunya bentuk melengkung di dalam sistem.

## Components

Setiap komponen di bawah ini ditulis ulang dari `ui.py`; nama kelas,
ukuran, dan warna diambil apa adanya.

### Title block (pita identitas model)

Pita sel berhairline yang membawa identitas model, selalu di atas lembar.

- **Shape:** bingkai `1px solid var(--rule)`, radius 8px, `overflow: hidden`,
  latar `sheet`.
- **Sel:** sembilan sel pada grid `repeat(9, minmax(0, 1fr))`. Tiap sel punya
  kunci mono (0,625rem, 500, tracking 0,11em, huruf besar, `muted`) dan nilai
  (1,02rem, 600, angka tabular, `ink`, `white-space: nowrap` dengan ellipsis
  bila panjang). Nama model memakai varian kecil 0,8rem.
- **Strip mikro:** baris di bawah grid dengan latar `paper`, pemisah atas
  `rule-soft`, memuat enam pasangan (data latih, data uji, fitur, kalibrasi,
  versi sklearn, hash SHA-256) dalam mono 0,625rem tracking 0,1em; nilai
  dicetak tebal dengan angka tabular.
- **Perilaku:** nilai tidak pernah dipotong secara visual pada lebar normal;
  sembilan sel dan label yang sama tidak pernah diulang. Title block adalah
  dokumen identitas, bukan kartu hias.

### Rail tab (empat area kerja)

- **Bentuk:** `gap: 0,35rem`, garis bawah `1px solid var(--rule)`, tiap tab
  `margin-right: 1,35rem`, padding 0,5rem 0 0,55rem.
- **Tipografi:** Archivo 0,82rem, 600, tracking -0,01em.
- **State:** default `muted`; aktif `ink` dengan indikator 2px `ink`; hover
  `ink2`; fokus `outline: 2px solid var(--accent); outline-offset: 2px`.
- **Ikon:** tiap tab punya ikon garis 15x15 yang dipasang sebagai mask CSS
  dari data URI sehingga warnanya ikut `currentColor`. Urutannya: `user`
  (Prediksi Single), `upload` (Prediksi Batch), `chart` (Dashboard & Model),
  `search` (EDA & Dokumentasi). Ikon ditambahkan lewat pseudo-element
  `::before` dengan lebar 15px, tinggi 15px, dan jarak kanan 0,45rem.

### Blok vonis (hasil prediksi)

- **Shape:** bingkai `1px solid var(--rule)`, radius 8px, latar `sheet`,
  padding 1rem 1,15rem 1,05rem, margin 0,2rem 0 0,9rem.
- **Kepala:** chip risiko 16px + kalimat keputusan 0,84rem; kata `CHURN` dan
  `TETAP` tebal dengan warna `ink`, sisanya `ink2`.
- **Angka:** 2,5rem, 700, tracking -0,032em, angka tabular, line-height 1,05;
  satuan persen 1,15rem berbobot 600 warna `muted`.
- **Sub-teks:** 0,8rem `muted`, "Probabilitas churn terkalibrasi".
- **State:** blok hanya muncul setelah prediksi; tidak ada keadaan kosong
  yang dipakai.

### Chip risiko

- **Bentuk:** radius 4px, padding 0,28rem 0,5rem, JetBrains Mono 0,66rem,
  600, tracking 0,1em, huruf besar.
- **Isian:** LOW = `ramp1` dengan teks `ink`; MID = `ramp4` dengan teks `ink`;
  HIGH = tinta dengan teks `sheet`. Di tema gelap ketiganya berbalik arah
  kontras, dan HIGH tetap berupa pita terang di atas lembar gelap.
- **State:** chip adalah label hasil, bukan tombol; tidak punya keadaan fokus
  atau hover.

### Skala probabilitas terkalibrasi

Skala terukur: posisi pada ramp adalah besarnya, warna hanya langkah dari
ramp yang sama.

- **Shape:** panel hairline radius 8px, padding 0,85rem 1rem 0,7rem. Track
  setinggi 26px dengan radius 4px dan border `rule`; tiga segmen: RENDAH
  (lebar = ambang, 32%), SEDANG (lebar = batas tinggi 60% dikurangi ambang),
  TINGGI (sisa lebar).
- **Label segmen:** JetBrains Mono 0,58rem tracking 0,11em huruf besar, rata
  kiri dengan padding kiri 0,55rem; disembunyikan di bawah 640px.
- **Penanda ambang:** garis vertikal 2px `ink` yang menonjol 6px di atas dan
  bawah track, dengan kepala bulat 8px; label nilainya (0,68rem mono, 600)
  berada di kotak `sheet` dengan border `rule` dan radius 3px.
- **Tick:** 0,58rem mono tracking 0,08em; tick ambang ditebalkan dengan
  warna `ink2`, tick lain `muted`. Tick pertama digeser -8% dan terakhir -92%
  supaya tidak terpotong tepi.

### Matriks konfusi

- **Shape:** grid `1fr 1fr` dengan bingkai hairline radius 8px, `overflow:
  hidden`, pemisah antar sel `rule-soft`.
- **Sel:** kunci mono 0,6rem tracking 0,12em huruf besar `muted`; nilai
  1,55rem berbobot 650 dengan angka tabular; keterangan 0,76rem `muted`.
- **Penekanan:** sel TP dan TN (dua hasil benar) mendapat latar `ramp1`.
  Tidak ada warna hijau atau merah: yang ditebalkan hanya ketepatan.

### Strip ringkasan

- **Shape:** grid tiga kolom sama, bingkai hairline radius 8px, `overflow:
  hidden`, pemisah vertikal `rule-soft`, padding sel 0,62rem 0,8rem.
- **Isi:** label mono di atas, angka tabular di bawah, memakai kelas yang
  sama dengan sel title block.
- **Responsif:** di bawah 900px menjadi satu kolom; pemisah vertikal
  diganti pemisah horizontal.

### Daftar saran retensi

- **Bentuk:** baris flex dengan jarak 0,6rem, padding 0,62rem 0,1rem,
  pemisah bawah `rule-soft`; item terakhir tanpa pemisah.
- **Warna:** ikon garis 15px dengan warna `accent`; label tebal `ink`;
  kalimat `ink2` 0,85rem line-height 1,5.
- **Isi:** saran dipilih dari data yang diisi, bukan dari daftar tetap; ikon
  yang dipakai `doc`, `layers`, `check`, `flag`, `user`, dan `target`.

### Plate EDA (gambar yang direkat ke lembar)

- **Shape:** gambar dibingkai `1px solid var(--rule)` dengan radius 8px dan
  latar `#FFFFFF` di kedua tema, seperti cetakan yang dijepit di atas meja
  gelap. Keterangan 0,78rem `muted`, padding 0,5rem 0,05rem 0,55rem.
- **Asal gambar:** ketujuh PNG di `docs/eda(explaratory data analysis)/`
  dihasilkan ulang oleh `python eda.py` dari CSV `Telco-Customer-Churn.csv`
  yang ada di repository, memakai palet yang sama dengan aplikasi. Bukan
  gambar hasil generator gambar.

### Footer lembar

- **Shape:** garis atas `1px solid var(--rule)`, margin atas 2,2rem, padding
  atas 0,85rem, JetBrains Mono 0,625rem tracking 0,06em, warna `muted`.
- **Isi:** identitas kelompok, kelas, dan NIM tiga anggota. Sesuai
  komitmen produk, footer tidak memuat kalimat "Built with Streamlit" atau
  sejenisnya.

### Tombol

- **Shape:** radius 6px, Archivo 0,84rem, 600, tracking -0,005em, tanpa
  bayangan, border `1px solid var(--rule)`.
- **Primer:** latar `ink`, teks `paper`, border `ink`. Hover: latar dan
  border `ink2`, teks tetap `paper`. Fokus: `outline: 2px solid var(--accent)`
  dengan offset 2px. Nonaktif: opacity .45.
- **Sekunder:** latar `sheet`, teks `ink`, border `rule`. Hover: latar
  `paper`, border `ink2`.
- **Transisi:** `background .12s ease, border-color .12s ease` pada kedua
  jenis tombol.

### Kontrol isian

- **Gaya:** latar `sheet`, border `1px solid var(--rule)`, radius 6px, teks
  0,85rem, `box-shadow: none`. Label control 0,74rem, 500, `muted`.
- **Fokus:** border berpindah ke `accent` dan cincin `0 0 0 2px
  var(--accent-soft)` menyertainya.
- **Tangga angka:** tombol naik/turun memakai `muted`; hover memakai
  `accent-soft` dengan teks `ink`.
- **Menu dan popover:** latar `sheet`, border `rule`, opsi 0,85rem `ink`.

### Pengalih tema

- **Gaya:** wadah `sheet` dengan border `rule`, radius 6px, padding 2px.
  Tombol di dalamnya radius 4px, 0,72rem, 600, `muted`.
- **State:** hover memakai latar `paper` dan teks `ink`; pilihan aktif memakai
  latar `accent-soft`, border `accent`, dan teks `ink`.

### Judul bagian dan catatan

- **Judul:** Archivo 1rem, 650, tracking -0,018em, `ink`; ikon garis 16px
  berwarna `accent` mendahului teks.
- **Catatan:** 0,82rem `muted`, lebar maksimum 78ch, line-height 1,55.

### Pesan dan tabel

- **Pesan:** radius 6px, border `rule`, latar `sheet`, teks `ink2` 0,85rem.
  Galat dan sukses memakai border `danger`; peringatan memakai garis kiri
  3px `ramp8`.
- **Tabel:** bingkai hairline radius 8px dengan `overflow: hidden`; isi tabel
  Streamlit dibiarkan tanpa bingkai sendiri. Streamlit 1.64 tidak menerima
  tema kustom untuk `st.dataframe`, jadi di tema gelap tabel tetap putih.
  Perlakukan itu sebagai keputusan, bukan kegagalan: tabel dan gambar EDA
  adalah plate putih yang direkat ke lembar, sama seperti cetakan yang
  dijepit di atas meja gelap.

### Ikon garis

- **Keluarga:** satu keluarga, viewBox 24x24, `fill="none"`,
  `stroke="currentColor"`, `stroke-width="1.5"`, `stroke-linecap="round"`,
  `stroke-linejoin="round"`, `aria-hidden="true"`, kelas `ico`.
- **Ukuran:** 16px secara bawaan, 15px untuk ikon daftar saran, 15x15
  sebagai mask pada rail tab. Ikon tidak pernah diperbesar untuk menjadi
  ilustrasi.
- **Isi katalog:** 19 ikon didefinisikan di `ui.py`: `target`, `user`,
  `upload`, `download`, `chart`, `linechart`, `search`, `sun`, `moon`,
  `check`, `alert`, `info`, `chevron`, `play`, `reset`, `doc`, `grid`,
  `layers`, `flag`. Sepuluh dari sembilan belas ikon itu terpakai di build:
  delapan sebagai ikon judul bagian, empat sebagai ikon rail tab, dan enam
  sebagai ikon daftar saran (sebagian dipakai dua kali). `download`, `sun`,
  `moon`, `alert`, `info`, `chevron`, `play`, `reset`, dan `grid` sudah
  tersedia di katalog tetapi belum dipakai.
- **Aturan:** tidak ada ikon emoji, tidak ada font ikon, tidak ada ikon
  berwarna sendiri. Warna ikon selalu `currentColor`; hanya ikon judul
  bagian dan ikon daftar saran yang diberi `accent`.

## Do's and Don'ts

### Do:

- **Do** bingkai setiap panel dengan `1px solid var(--rule)` dan pisahkan
  sel di dalamnya dengan `1px solid var(--rule-soft)`.
- **Do** pakai `paper` untuk latar lembar dan `sheet` untuk panel, agar
  kedalaman datang dari nada, bukan dari bayangan.
- **Do** baca risiko sebagai posisi pada ramp: pakai pasangan
  `band-low`/`band-mid`/`band-high` yang sudah ada, jangan karang warna
  kategori baru.
- **Do** tulis label terukur dalam JetBrains Mono huruf besar dengan
  tracking 0,08em sampai 0,12em, dan semua angka besar dengan angka
  tabular.
- **Do** tulis angka gaya Indonesia: koma untuk desimal, titik untuk ribuan.
- **Do** tandai fokus dengan `outline: 2px solid var(--accent)` dan
  `outline-offset: 2px`, atau cincin `0 0 0 2px var(--accent-soft)` pada
  kontrol.
- **Do** gunakan `accent` hanya untuk tautan, fokus, pilihan tema aktif,
  ikon judul bagian, ikon daftar saran, dan batang yang disorot pada grafik.
- **Do** pertahankan plate EDA tetap putih di kedua tema, seperti cetakan
  yang dijepit di atas lembar.
- **Do** nyatakan batas dan ketidakpastian di tempat yang sama dengan
  klaim, dan jangan pernah menampilkan angka metrik tanpa keterangan
  datanya.

### Don't:

- **Don't** menambah bayangan, glow, gradien, atau efek kaca. Panel datar
  dengan `box-shadow: none` adalah keadaan yang benar.
- **Don't** memberi warna lalu lintas pada risiko (merah-amber-hijau) atau
  memakai `accent` sebagai isian pita.
- **Don't** menambahkan emoji, glyph ikon, font ikon, atau huruf ketiga.
  Ikon hanya dari katalog 24x24 stroke 1,5 di `ui.py`.
- **Don't** memakai `shadow` atau bayangan luar untuk membuat panel
  "terangkat"; token itu tidak dipakai di build ini.
- **Don't** membiarkan hasil prediksi lama tetap tampil setelah input
  berubah. Pola yang sudah berjalan: tampilkan "Input telah berubah. Klik
  Prediksi untuk memperbarui hasil." dan jangan mengganti hasil secara
  diam-diam.
- **Don't** menambahkan kalimat informasi seperti "Built with Streamlit" di
  footer, dan jangan memuat klaim yang tidak diuji.
- **Don't** meletakkan angka yang sama di dua tempat dengan nilai berbeda;
  frontmatter di file ini adalah lapisan token yang normatif.
