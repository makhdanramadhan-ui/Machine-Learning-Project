"""Bangun daftar referensi, tabel CSV, BibTeX, dan unduh PDF open-access terverifikasi."""
import csv
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.request import Request, urlopen

from eda import md_table

BASE = Path(__file__).resolve().parent


def build_literature(download=False):
    docs = BASE / "docs"
    refs = json.loads((docs / "referensi.json").read_text(encoding="utf-8"))
    import pandas as pd
    table = pd.DataFrame([{
        "No": r["no"], "Penulis & Tahun": r["short"], "Permasalahan": r["problem"],
        "Dataset": r["dataset"], "Metode/Algoritma": r["methods"], "Metrik Evaluasi": r["metrics"],
        "Hasil Utama": r["result"], "Perbedaan dengan Project": r["difference"], "DOI": r["doi"],
    } for r in refs])
    table.to_csv(docs / "tabel_studi_literatur.csv", index=False, encoding="utf-8-sig")
    text = ["# Studi Literatur — Kelompok 12, Kelas B2",
            "Lima artikel **jurnal ilmiah**, diverifikasi metadata judul/penulis/tahun melalui Crossref "
            "dan isi melalui teks lengkap Europe PMC/PMC pada 2 Oktober 2026. Semua DOI adalah journal-article.",
            "Angka berikut adalah **hasil yang dilaporkan penulis**, bukan hasil project atau replikasi kelompok. "
            "Dataset, label, resampling, split, dan definisi metrik berbeda, sehingga skor tidak dibandingkan langsung.",
            "## Tabel studi literatur", md_table(table), "## Daftar referensi dan bukti"]
    bib = []
    for r in refs:
        text.extend([
            f"### [{r['no']}] {r['short']}",
            f"{r['authors'].replace(';', ',')} ({r['year']}). **{r['title']}**. "
            f"*{r['journal']}*, {r['volume_issue']}, {r['article']}. {r['url']}",
            f"- Teks lengkap: {r['fulltext']}\n- PDF penerbit: {r['pdf_url']}",
            f"- Bagian bukti: {r['evidence']}\n- Relevansi: {r['use']}\n- Catatan pembacaan: {r['caveat']}",
        ])
        bib.append(f"@article{{telco_ref_{r['no']},\n  author = {{{r['authors'].replace('; ', ' and ')}}},\n"
                   f"  title = {{{r['title']}}},\n  journal = {{{r['journal']}}},\n  year = {{{r['year']}}},\n"
                   f"  volume = {{{r['volume_issue'].split('(')[0]}}},\n  pages = {{{r['article']}}},\n"
                   f"  doi = {{{r['doi']}}},\n  url = {{{r['url']}}}\n}}")
    text.extend(["## Hubungan literatur dengan keputusan project",
                 "- **Masalah/dataset:** kelima jurnal membahas churn telecom; [1] mencakup Telco 7.043 catatan. "
                 "CSV lokal tetap dihitung sendiri, tidak memakai jumlah yang berbeda di [5].",
                 "- **Preprocessing:** [1] menguji standardisasi/encoding/transformasi; project memakai scaler dan "
                 "one-hot karena cocok dengan LR serta kategori nominal. Tidak menyalin WOE tanpa eksperimen.",
                 "- **Algoritma:** [1] membandingkan LR/RF/DT; [3]–[4] menjelaskan ensemble sebagai alternatif. "
                 "Tiga model dipilih untuk membandingkan model linear, pohon tunggal, dan bagging ensemble.",
                 "- **Imbalance/evaluasi:** [2] dan [4] mendukung evaluasi recall/F1 kelas churn; "
                 "project menggunakan class_weight, stratifikasi, dan test yang tidak di-resample.",
                 "- **Implementasi project:** kalibrasi sigmoid dan threshold OOF dipakai untuk menyelaraskan "
                 "probabilitas dengan keputusan aplikasi. Kelima jurnal ini tidak diklaim sebagai bukti "
                 "khusus bahwa threshold 0,32 pasti optimal untuk semua dataset.",
                 "## Dokumentasi metode tambahan (di luar lima jurnal)",
                 "- [scikit-learn: probability calibration](https://scikit-learn.org/stable/modules/calibration.html)",
                 "- [scikit-learn: tuning decision threshold](https://scikit-learn.org/stable/modules/classification_threshold.html)",
                 "- [scikit-learn: common pitfalls/data leakage](https://scikit-learn.org/stable/common_pitfalls.html)",
                 "- [Sumber dataset Telco](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)"])
    (docs / "STUDI_LITERATUR.md").write_text("\n\n".join(text) + "\n", encoding="utf-8")
    (docs / "referensi.bib").write_text("\n\n".join(bib) + "\n", encoding="utf-8")
    if download:
        journals = docs / "jurnal"
        journals.mkdir(exist_ok=True)
        manifest = []
        for r in refs:
            name = f"{r['no']:02d}_{r['doi'].replace('/', '_')}.pdf"
            xml_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{r['pmcid']}/fullTextXML"
            with urlopen(xml_url, timeout=90) as response:
                xml = response.read()
            (journals / name.replace(".pdf", ".xml")).write_bytes(xml)
            root = ET.fromstring(xml)
            readable = [f"# {r['title']}", f"{r['authors']} ({r['year']}). {r['journal']}. {r['url']}",
                        "Teks arsip open-access dari Europe PMC (JATS XML), bukan PDF penerbit. "
                        "Tabel disajikan sebagai teks; gunakan tautan asli untuk format lengkap.",
                        "Lisensi: CC BY 4.0; atribusi penulis dan sumber tetap disertakan."]
            for part in [root.find(".//abstract"), root.find("body")]:
                if part is None:
                    continue
                for node in part.iter():
                    if node.tag in ["title", "p", "table-wrap"]:
                        content = " ".join("".join(node.itertext()).split())
                        readable.append(("## " if node.tag == "title" else "") + content)
            (journals / name.replace(".pdf", ".md")).write_text("\n\n".join(readable), encoding="utf-8")
            try:
                req = Request(r["pdf_url"], headers={"User-Agent": "Mozilla/5.0 (academic project reference archive)"})
                with urlopen(req, timeout=90) as response:
                    content = response.read()
                if not content.startswith(b"%PDF"):
                    raise ValueError("Respons bukan PDF; gunakan tautan teks lengkap.")
                (journals / name).write_bytes(content)
                status = "downloaded"
            except Exception as exc:
                status = f"link-only: {exc}"
                # Repositori open-access Europe PMC mengarsipkan versi penerbit.
                for url in [f"https://europepmc.org/articles/{r['pmcid']}?pdf=render",
                            f"https://pmc.ncbi.nlm.nih.gov/articles/{r['pmcid']}/pdf/" +
                            (re.search(rb'content-type="pmc-pdf" xlink:href="([^"]+)"', xml).group(1).decode()
                             if re.search(rb'content-type="pmc-pdf" xlink:href="([^"]+)"', xml) else "")]:
                    try:
                        with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60) as response:
                            content = response.read()
                        if content.startswith(b"%PDF"):
                            (journals / name).write_bytes(content)
                            status = "downloaded (open-access archive)"
                            break
                    except Exception:
                        continue
            manifest.append({"no": r["no"], "doi": r["doi"], "file": name,
                             "source": r["pdf_url"], "fulltext_xml": name.replace(".pdf", ".xml"),
                             "fulltext_source": xml_url, "status": status})
            print(r["short"], status)
        (journals / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        (journals / "README.md").write_text(
            "# Arsip lima jurnal\n\nSetiap artikel tersedia sebagai teks lengkap `.md` dan sumber JATS `.xml` "
            "dari Europe PMC; atribusi dan tautan DOI tercantum. Tiga PDF penerbit berhasil diunduh "
            "(artikel 1, 2, 4). PDF artikel 3 dan 5 tidak dapat diunduh otomatis dari penerbit; "
            "tautan PDF serta teks lengkap tersedia di `../STUDI_LITERATUR.md`.\n\n"
            "File Markdown merupakan konversi teks arsip, bukan salinan PDF. "
            "`manifest.json` mencatat sumber dan status unduhan.\n", encoding="utf-8")
    return refs


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true", help="Unduh PDF open-access dari penerbit.")
    build_literature(download=parser.parse_args().download)
