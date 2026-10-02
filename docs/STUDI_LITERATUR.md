# Studi Literatur — Kelompok 12, Kelas B2

Lima artikel **jurnal ilmiah**, diverifikasi metadata judul/penulis/tahun melalui Crossref dan isi melalui teks lengkap Europe PMC/PMC pada 2 Oktober 2026. Semua DOI adalah journal-article.

Angka berikut adalah **hasil yang dilaporkan penulis**, bukan hasil project atau replikasi kelompok. Dataset, label, resampling, split, dan definisi metrik berbeda, sehingga skor tidak dibandingkan langsung.

## Tabel studi literatur

| No | Penulis & Tahun | Permasalahan | Dataset | Metode/Algoritma | Metrik Evaluasi | Hasil Utama | Perbedaan dengan Project | DOI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Sana et al. (2022) | Mengoptimalkan prediksi churn telekomunikasi melalui transformasi data, pemilihan fitur, dan tuning. | Empat dataset publik: 100.000, 5.000, 3.333, dan 7.043 catatan; dataset keempat adalah Telco Customer Churn Kaggle. | LR, RF, Decision Tree, KNN, NB, GB, FNN, RNN; enam transformasi termasuk Z-score/WOE; univariate feature selection dan grid search. | AUC, precision, recall, F-measure; 10-fold CV. | Penulis melaporkan peningkatan hingga 26,2% AUC dan 17% F-measure. Pada Dataset-1, WOE+LR AUC 0,796 dan F-measure 0,79 (Tabel 9). | Project ini memakai satu dataset Telco, 3 model, StandardScaler+OneHotEncoder, CV 5-fold dengan holdout 20%, kalibrasi, dan aplikasi Streamlit; tidak menerapkan WOE. | 10.1371/journal.pone.0278095 |
| 2 | Y., Ly & Son (2022) | Prediksi churn pada dataset tidak seimbang dengan kernel SVM, pemilihan fitur, dan resampling. | Orange telecom Kaggle: 3.333 pelanggan, 19 fitur + 1 label; sekitar 14% churn menurut artikel. | SVM RBF/polynomial/linear/sigmoid; SFS/SBS; SMOTE-Tomek dan SMOTE-ENN; hyperparameter tuning. | Accuracy, precision, recall, F1; hasil konfigurasi pada Tabel 6. | SMOTE-ENN + SFS/SBS + RBF-SVM: accuracy 0,9888 dan F1 0,9901 (Tabel 6), sesuai protokol artikel. | Project tidak memakai SVM/resampling; class_weight diuji pada train-CV, test tetap berdistribusi alami, dan threshold dipilih train-only. | 10.1371/journal.pone.0267935 |
| 3 | Bilal et al. (2022) | Menggabungkan segmentasi pelanggan dan klasifikasi untuk meningkatkan prediksi churn. | Dua dataset menurut artikel: GitHub 5.000 catatan (707 churn) dan BigML 3.333 (483 churn). | K-means/K-medoids/X-means/random clustering; tujuh classifier; voting, bagging, stacking, AdaBoost. | Accuracy, precision, recall, F-measure; evaluasi multi-dataset. | Konfigurasi K-med+GBT+DT+DL+AdaBoost: accuracy 94,7% GitHub dan 92,43% BigML; F-measure 80,63% dan 71,81% (Tabel 9–10). | Project membandingkan 3 classifier supervised secara langsung, tanpa clustering atau hybrid ensemble; fokus probabilitas terkalibrasi dan deploy. | 10.7717/peerj-cs.854 |
| 4 | Zhou et al. (2023) | Early warning churn pada data operator dengan ketidakseimbangan kelas besar. | 900.000 catatan operator, 35 atribut mentah; setelah preprocessing/resampling dilaporkan 386.269 catatan, 14 fitur. | Cleaning, SMOTE, standardisasi; BPNN, Random Forest, AdaBoost, RF-AdaBoost dan classifier pembanding. | Precision/recall/F1 kelas positif dan weighted average; ROC. | RF-AdaBoost melaporkan precision churn 0,99, recall 0,93, F1 0,96 (Tabel 6); weighted F1 0,98. | Project memakai dataset publik jauh lebih kecil; RF dibandingkan dengan LR dan DT, class_weight tanpa SMOTE; F1 yang dilaporkan adalah kelas churn, bukan weighted F1. | 10.1371/journal.pone.0292466 |
| 5 | Khattak et al. (2023) | Menguji model hybrid deep learning untuk prediksi churn telekomunikasi. | Telco Kaggle menurut artikel: 7.033 baris dan 20 fitur; split 80:20. | Preprocessing missing TotalCharges, hybrid BiLSTM-CNN, pembanding metode ML/DL. | Accuracy, precision, recall, F-score. | BiLSTM-CNN: accuracy 81%, precision 66%, recall 64%, F-score 65% (Tabel 6). | Project memakai classifier tabular klasik yang lebih ringan, 7.043 baris mentah/7.032 bersih; pipeline train-only, CV, dan model terkalibrasi dalam aplikasi. | 10.1038/s41598-023-44396-w |

## Daftar referensi dan bukti

### [1] Sana et al. (2022)

Joydeb Kumar Sana, Mohammad Zoynul Abedin, M. Sohel Rahman, M. Saifur Rahman (2022). **A novel customer churn prediction model for the telecommunication industry using data transformation methods and feature selection**. *PLOS ONE*, 17(12), e0278095. https://doi.org/10.1371/journal.pone.0278095

- Teks lengkap: https://pmc.ncbi.nlm.nih.gov/articles/PMC9714823/
- PDF penerbit: https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0278095&type=printable

- Bagian bukti: Abstrak; bagian kontribusi; Tabel 2, Tabel 9; bagian experimental setup.
- Relevansi: Dasar memilih LR/RF/Decision Tree, standardisasi, tuning, dan evaluasi multi-metrik.
- Catatan pembacaan: Angka Tabel 9 berasal dari Dataset-1 (100.000 catatan), bukan hasil Telco 7.043 catatan. Tidak dibandingkan langsung dengan metrik project.

### [2] Y., Ly & Son (2022)

Nguyen Nhu Y., Tran Van Ly, Dao Vu Truong Son (2022). **Churn prediction in telecommunication industry using kernel Support Vector Machines**. *PLOS ONE*, 17(5), e0267935. https://doi.org/10.1371/journal.pone.0267935

- Teks lengkap: https://pmc.ncbi.nlm.nih.gov/articles/PMC9128990/
- PDF penerbit: https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0267935&type=printable

- Bagian bukti: Abstrak; bagian dataset; bagian model performance evaluation; Tabel 2 dan Tabel 6.
- Relevansi: Alasan tidak memakai accuracy saja pada kelas imbalanced; bahan pengembangan alternatif penyeimbangan kelas.
- Catatan pembacaan: Dataset, resampling, dan protokol evaluasi berbeda. Skor setelah resampling tidak dapat disamakan dengan performa holdout alami project.

### [3] Bilal et al. (2022)

Syed Fakhar Bilal, Abdulwahab Ali Almazroi, Saba Bashir, Farhan Hassan Khan, Abdulaleem Ali Almazroi (2022). **An ensemble based approach using a combination of clustering and classification algorithms to enhance customer churn prediction in telecom industry**. *PeerJ Computer Science*, 8, e854. https://doi.org/10.7717/peerj-cs.854

- Teks lengkap: https://pmc.ncbi.nlm.nih.gov/articles/PMC9044233/
- PDF penerbit: https://peerj.com/articles/cs-854.pdf

- Bagian bukti: Abstrak; bagian data acquisition; Tabel 9–10.
- Relevansi: Dasar pembanding Random Forest/ensemble dan gagasan segmentasi sebagai pengembangan selanjutnya.
- Catatan pembacaan: Artikel menyebut dataset GitHub 5.000; jangan menganggap identik dengan CSV Telco lokal 7.043 meskipun menyebut tautan Telco pada bagian lain.

### [4] Zhou et al. (2023)

Yancong Zhou, Wenyue Chen, Xiaochen Sun, Dandan Yang (2023). **Early warning of telecom enterprise customer churn based on ensemble learning**. *PLOS ONE*, 18(10), e0292466. https://doi.org/10.1371/journal.pone.0292466

- Teks lengkap: https://pmc.ncbi.nlm.nih.gov/articles/PMC10566699/
- PDF penerbit: https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0292466&type=printable

- Bagian bukti: Abstrak; bagian dataset/preprocessing; Tabel 6.
- Relevansi: Memperjelas pentingnya recall churn dan membedakan metrik kelas positif dari weighted average.
- Catatan pembacaan: Dataset operator dan distribusi setelah resampling berbeda; skor weighted average tidak dipakai sebagai padanan F1 churn project.

### [5] Khattak et al. (2023)

Asad Khattak, Zartashia Mehak, Hussain Ahmad, Muhammad Usama Asghar, Muhammad Zubair Asghar, Aurangzeb Khan (2023). **Customer churn prediction using composite deep learning technique**. *Scientific Reports*, 13, 17294. https://doi.org/10.1038/s41598-023-44396-w

- Teks lengkap: https://pmc.ncbi.nlm.nih.gov/articles/PMC10570272/
- PDF penerbit: https://www.nature.com/articles/s41598-023-44396-w.pdf

- Bagian bukti: Abstrak; bagian dataset; Tabel 3 dan Tabel 6.
- Relevansi: Mendukung konteks dataset Telco dan memberi alternatif deep learning untuk pengembangan, bukan alasan menganggap tabular sebagai time series.
- Catatan pembacaan: Jumlah 7.033 berasal dari laporan artikel dan berbeda dari CSV lokal. Hubungan urutan fitur tabular tidak otomatis merupakan urutan waktu; prosedur test project tetap independen.

## Hubungan literatur dengan keputusan project

- **Masalah/dataset:** kelima jurnal membahas churn telecom; [1] mencakup Telco 7.043 catatan. CSV lokal tetap dihitung sendiri, tidak memakai jumlah yang berbeda di [5].

- **Preprocessing:** [1] menguji standardisasi/encoding/transformasi; project memakai scaler dan one-hot karena cocok dengan LR serta kategori nominal. Tidak menyalin WOE tanpa eksperimen.

- **Algoritma:** [1] membandingkan LR/RF/DT; [3]–[4] menjelaskan ensemble sebagai alternatif. Tiga model dipilih untuk membandingkan model linear, pohon tunggal, dan bagging ensemble.

- **Imbalance/evaluasi:** [2] dan [4] mendukung evaluasi recall/F1 kelas churn; project menggunakan class_weight, stratifikasi, dan test yang tidak di-resample.

- **Implementasi project:** kalibrasi sigmoid dan threshold OOF dipakai untuk menyelaraskan probabilitas dengan keputusan aplikasi. Kelima jurnal ini tidak diklaim sebagai bukti khusus bahwa threshold 0,32 pasti optimal untuk semua dataset.

## Dokumentasi metode tambahan (di luar lima jurnal)

- [scikit-learn: probability calibration](https://scikit-learn.org/stable/modules/calibration.html)

- [scikit-learn: tuning decision threshold](https://scikit-learn.org/stable/modules/classification_threshold.html)

- [scikit-learn: common pitfalls/data leakage](https://scikit-learn.org/stable/common_pitfalls.html)

- [Sumber dataset Telco](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
