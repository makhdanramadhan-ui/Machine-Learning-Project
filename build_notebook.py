"""Buat dan eksekusi notebook laporan dari pipeline serta artefak aktual."""
from pathlib import Path
import nbformat as nbf
from nbclient import NotebookClient

BASE = Path(__file__).resolve().parent


def build_notebook():
    md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
    cells = [
        md("# Prediksi Customer Churn — Telco\n\n**Kelompok 12 • Kelas B2**\n\n"
           "Muhamad Akhdan Ramadhan (J0404241102), Thevan Erlangga (J0404241073), "
           "Fachri Abyasa Tarid (J0404241136).\n\n"
           "Notebook ini memakai pipeline terkini. EDA asosiasi dilakukan pada **train saja**. "
           "Evaluasi dihitung ulang dari model tersimpan; seluruh training tersedia di `train.py`. "
           "Notebook arsip ada di `docs/archive/projekk_awal.ipynb`."),
        md("## 1. Masalah, tujuan, dan sumber\n\nChurn berarti pelanggan berhenti berlangganan. "
           "Tujuan: membandingkan tiga classifier, mendeteksi kelas churn dengan metrik yang sesuai, "
           "dan menyediakan aplikasi single/batch dengan probabilitas terkalibrasi.\n\n"
           "[Dataset Telco Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn). "
           "Target Yes=1, No=0. Ini klasifikasi tabular, bukan forecasting.\n\n"
           "[Lima jurnal dan tabel literatur](docs/STUDI_LITERATUR.md)."),
        code("from pathlib import Path\nimport json\nimport joblib\nimport pandas as pd\n"
             "from IPython.display import display, Image, Markdown\n"
             "from eda import run_eda\nfrom training_data import load_training_split\n"
             "from prediction import input_schema, predict_customers, example_customers\n"
             "from calibrate import classification_metrics\n"
             "BASE = Path.cwd()\nsummary = run_eda()\nEDA = BASE / 'docs' / 'eda'\n"
             "raw = pd.read_csv(BASE / 'Telco-Customer-Churn.csv')\nprint('Raw shape:', raw.shape)"),
        md("## 2. Variabel, tipe data, dan statistik\n\nSeniorCitizen bertipe angka tetapi semantiknya "
           "indikator kategori biner; tenure adalah bulan. TotalCharges awalnya string karena nilai kosong. "
           "Kolom ID tidak digunakan untuk prediksi pelanggan baru."),
        code("display(pd.read_csv(EDA / 'data_dictionary.csv'))\n"
             "display(pd.read_csv(EDA / 'descriptive_statistics.csv').fillna('—'))"),
        md("## 3. Missing value, duplikat, dan outlier\n\nSebelas TotalCharges kosong terdeteksi "
           "setelah konversi numerik; seluruhnya tenure 0 dan tidak churn. Penghapusan baris "
           "mempertahankan cohort eksperimen awal, namun bukan kewajiban setelah fitur TotalCharges dibuang. "
           "Eksklusi pelanggan baru adalah keterbatasan.\n\n"
           "Profil identik setelah ID dibuang bisa merupakan pelanggan berbeda. Tidak dihapus otomatis. "
           "Pemeriksaan IQR merupakan alat screening, bukan bukti seluruh data bebas anomali."),
        code("display(pd.read_csv(EDA / 'missing_values.csv'))\n"
             "display(pd.DataFrame(summary['duplicates'].items(), columns=['Pemeriksaan','Jumlah']))\n"
             "display(pd.read_csv(EDA / 'outliers_iqr.csv'))"),
        md("## 4. Visualisasi dan interpretasi\n\nPemeriksaan kualitas memakai CSV mentah; "
           "grafik asosiasi target hanya memakai training set. Setiap grafik dijelaskan di bawahnya."),
        code("for figure in summary['figures']:\n"
             "    display(Image(filename=str(EDA / figure['file'])))\n"
             "    display(Markdown(figure['interpretation']))"),
        md("## 5. Preprocessing dan split\n\nCohort 7.032 → 5.625 train / 1.407 test secara "
           "stratified, random_state=42. customerID dihapus; TotalCharges tidak dipakai agar input "
           "lebih sederhana. Tidak mengklaim TotalCharges selalu MonthlyCharges×tenure atau "
           "bahwa penghapusan fitur pasti meningkatkan performa.\n\n"
           "StandardScaler pada SeniorCitizen, tenure, MonthlyCharges; OneHotEncoder pada 15 "
           "kategori. Pipeline fit hanya pada train/fold. Scaling berguna untuk LR; pohon tidak "
           "membutuhkannya namun tetap memakai pipeline konsisten. class_weight dituning; tidak "
           "menggunakan SMOTE."),
        code("X_train, X_test, y_train, y_test = load_training_split()\n"
             "pipe = joblib.load(BASE / 'model_churn.pkl')\ncal = joblib.load(BASE / 'calibrator.pkl')\n"
             "info = json.loads((BASE / 'model_info.json').read_text())\n"
             "deployment = json.loads((BASE / 'deployment_info.json').read_text())\n"
             "print('Train/test:', X_train.shape, X_test.shape)\n"
             "print('Jumlah fitur setelah transformasi:', len(pipe.named_steps['pre'].get_feature_names_out()))\n"
             "display(pipe)"),
        md("## 6. Training tiga algoritma dan alasan\n\n"
           "- Logistic Regression: baseline linear pada log-odds, ringan dan dapat diinterpretasikan.\n"
           "- Decision Tree: aturan non-linear/interaksi; kedalaman dituning untuk membatasi kompleksitas.\n"
           "- Random Forest: ensemble bagging pohon; pembanding model lebih kompleks dan reduksi varians.\n\n"
           "Stratified 5-Fold GridSearchCV dengan scoring F1 kelas churn. Hyperparameter dipilih pada train; "
           "pemenang berdasarkan CV-F1. Jalankan sel opsional berikut hanya jika ingin membangun ulang seluruh artefak."),
        code("RUN_TRAINING = False\nif RUN_TRAINING:\n    from train import train\n    train()\n"
             "comparison = pd.read_csv(BASE / 'hasil_perbandingan.csv')\n"
             "display(comparison)\ndisplay(pd.read_csv(BASE / 'cv_detail.csv'))"),
        md("## 7. Analisis perbandingan dan overfitting\n\nLR dipilih dengan CV-F1 0,6304; RF "
           "0,6260; DT 0,6147. Selisih LR–RF kecil dan tidak membuktikan keunggulan mutlak. "
           "Pada test, DT memiliki recall/F1 tertinggi model inti dan RF accuracy tertinggi. "
           "RF memiliki gap train–validation–test terbesar, indikasi overfitting. Tidak menyimpulkan "
           "underfitting hanya dari accuracy yang sedang.\n\n"
           "Kemungkinan perbedaan: kompleksitas/interaksi, class_weight, regularisasi, dan split. "
           "Baseline selalu tidak churn tetap mendapat accuracy sekitar 73,42% namun recall churn 0."),
        code("display(comparison[['Model','Train_F1','CV_TRAIN_F1','CV_F1','CV_F1_STD','F1']])\n"
             "print('Baseline majority accuracy:', round(float((y_test == 0).mean()), 4))\n"
             "base_prob = pipe.predict_proba(X_test)[:, 1]\n"
             "print('Verifikasi model inti:', classification_metrics(y_test, base_prob, 0.5))"),
        md("## 8. Kalibrasi, threshold, dan evaluasi model aplikasi\n\n"
           "Sigmoid calibration train-only. Threshold dipilih dari grid 0,10–0,60 langkah 0,01 "
           "dengan F1 maksimum prediksi OOF training, menggunakan kalibrasi di dalam outer training fold. "
           "Hyperparameter inti sudah dipilih pada train sehingga skor OOF ini adalah skor tuning, "
           "bukan estimasi generalisasi independen. Test tidak digunakan untuk pemilihan threshold.\n\n"
           "Probabilitas dan keputusan aplikasi berasal dari model yang sama: CHURN jika p≥0,32. "
           "ROC-AUC/Brier tidak berubah bila hanya threshold diubah."),
        code("prob, pred = predict_customers(X_test, cal, input_schema(pipe), deployment['threshold'])\n"
             "actual = classification_metrics(y_test, prob, deployment['threshold'])\n"
             "assert actual == deployment['metrics']\n"
             "display(pd.DataFrame([{'Konfigurasi':'Aplikasi threshold 0.32', **actual},\n"
             "                      {'Konfigurasi':'Kalibrasi threshold 0.50', **deployment['metrics_at_0_5']}]))\n"
             "print('Threshold:', deployment['threshold'], 'Skor OOF tuning:', deployment['oof_tuning_f1'])"),
        md("## 9. Kesalahan prediksi dan interpretasi\n\nAplikasi: TP 275, TN 790, FP 243, FN 99. "
           "Precision 53,09% dan recall 73,53% menjelaskan trade-off retensi; CHURN bukan kepastian. "
           "Koefisien model inti menunjukkan hubungan dengan log-odds dengan fitur lain tetap; "
           "bukan pengaruh kausal. Bobot numerik terstandardisasi tidak langsung sebanding dengan dummy kategori."),
        code("errors = X_test.copy()\nerrors['Aktual'] = y_test\nerrors['Prediksi'] = pred\n"
             "errors['Prob_Churn'] = prob\n"
             "display(errors[errors.Aktual != errors.Prediksi].head(10))\n"
             "coefficients = pd.DataFrame({'Fitur': pipe.named_steps['pre'].get_feature_names_out(),\n"
             "                             'Koefisien': pipe.named_steps['clf'].coef_[0]})\n"
             "display(coefficients.reindex(coefficients.Koefisien.abs().sort_values(ascending=False).index).head(15))"),
        md("## 10. Implementasi, sanity test, dan keterbatasan\n\n"
           "Streamlit → validasi 18 input → preprocessing dalam pipeline terkalibrasi → probabilitas "
           "→ threshold → label/risiko. CSV invalid ditolak dengan pesan; hasil dapat diunduh.\n\n"
           "Keterbatasan: dataset historis tunggal, profil identik lintas split, eksklusi tenure 0, "
           "F1 moderat, FP/FN tetap ada, saran retensi berbasis aturan belum diuji kausal. "
           "Pengembangan: validasi eksternal/temporal, group-aware split, ablation fitur, cost-based "
           "threshold, tuning RF, SHAP dan pengujian tindakan retensi."),
        code("example = example_customers()\np, labels = predict_customers(example, cal, input_schema(pipe), deployment['threshold'])\n"
             "example['Prob_Churn'] = p\nexample['Prediksi'] = labels\ndisplay(example)"),
        md("## 11. Berkas pengumpulan\n\n"
           "- [PPT](docs/ML2026_B2_Kelompok12_PrediksiCustomerChurn.pptx)\n"
           "- [Naskah video demo](docs/NASKAH_VIDEO_DEMO.md)\n"
           "- [Studi literatur](docs/STUDI_LITERATUR.md)\n"
           "- [Laporan EDA](docs/eda/EDA.md)\n"
           "- [Repository](https://github.com/makhdanramadhan-ui/Machine-Learning-Project)\n"
           "- [Aplikasi](https://machine-learning-project-u8yovshrqrc5tm5s2y2qto.streamlit.app/)\n\n"
           "Pembagian tugas aktual diisi kelompok. Rekaman video asli dilakukan anggota; naskah bukan pengganti video."),
    ]
    nb = nbf.v4.new_notebook(cells=cells, metadata={
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    })
    NotebookClient(nb, timeout=180, kernel_name="python3", resources={"metadata": {"path": str(BASE)}}).execute()
    nbf.write(nb, BASE / "projekk.ipynb")
    print(f"Notebook selesai: {len(cells)} sel, seluruh code cell dieksekusi tanpa error.")


if __name__ == "__main__":
    build_notebook()
