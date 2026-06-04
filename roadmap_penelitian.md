# Panduan Awal & Peta Jalan Penelitian (Roadmap)

Dokumen ini menjelaskan rangkuman alur penelitian dari awal hingga akhir, serta panduan berkas data mana saja yang harus digunakan.

---

## 1. Peta Jalan Langkah Kerja (Step-by-Step)

```
[ Tahap 1: Eksplorasi Data ] ➔ [ Tahap 2: Ekstraksi Fitur ] ➔ [ Tahap 3: Pelabelan Stres ]
                                                                        ↓
[ Tahap 6: Penulisan Proposal ] ➔ [ Tahap 5: Pemodelan ML ] ➔ [ Tahap 4: Penggabungan Data ]
```

*   **Langkah 1: Eksplorasi Awal (EDA):** Buka data kuesioner dan data sensor di folder `dataset_studentlife_excel/` menggunakan Excel untuk memahami kolom-kolomnya (terutama kolom `uid` sebagai pengenal mahasiswa).
*   **Langkah 2: Ekstraksi Fitur (Feature Engineering):** Agregasikan data sensor (yang berupa baris log waktu transaksi) menjadi rata-rata nilai per mahasiswa (`uid`).
*   **Langkah 3: Pembuatan Label Risiko (Ground Truth):** Klasifikasikan status mental mahasiswa berdasarkan skor kuesioner akhir semester (PHQ-9 atau PSS-10).
*   **Langkah 4: Penggabungan Data (Data Merging):** Lakukan penggabungan (*join*) data fitur sensor pasif dengan label risiko berdasarkan kolom `uid`.
*   **Langkah 5: Melatih Model Machine Learning:** Masukkan data gabungan ke algoritma SVM dan Random Forest (gunakan skrip Python di `analisis_kesehatan_mental.md`).
*   **Langkah 6: Penyusunan Laporan/Proposal:** Ambil metrik performa (akurasi, recall) dan *feature importance* (faktor gawai terpenting) untuk ditulis di proposal riset Anda.

---

## 2. Berkas Data yang Wajib Digunakan

Semua berkas di bawah ini terletak di folder **`dataset_studentlife_excel/`** (untuk format Excel/CSV) atau **`dataset_studentlife/dataset_rds/`** (untuk R/Python):

| Nama Berkas | Kategori Data | Variabel Penelitian yang Diwakili | Alasan/Fungsi dalam Analisis |
| :--- | :--- | :--- | :--- |
| **`surveys.xlsx`** (Sheet: `PHQ-9` & `PerceivedStressScale`) | Kuesioner Mental (Aktif) | Tingkat Gejala Depresi dan Stres Akademik | **Label Target ($y$):** Digunakan untuk mengklasifikasikan mahasiswa ke kelas Stres (1) atau Normal (0). |
| **`surveys.xlsx`** (Sheet: `psqi`) | Kuesioner Tidur (Aktif) | Kualitas Tidur Mahasiswa (*Pittsburgh Sleep Quality Index*) | **Variabel Pembanding:** Digunakan untuk memvalidasi apakah sensor pasif malam hari sesuai dengan kualitas tidur subjektif mahasiswa. |
| **`sensing_phonelock.xlsx`** | Sensor Gawai (Pasif) | Durasi Penggunaan Layar (*Screen-time*) & Frekuensi Buka Kunci (*Unlock Frequency*) | **Fitur Utama ($X_1$):** Mengukur tingkat kecemasan (frekuensi unlock tinggi) dan adiksi gawai (durasi layar tinggi). |
| **`sensing_dark.xlsx`** | Sensor Gawai (Pasif) | Durasi Tidur Pasif Mahasiswa (*Darkness Duration*) | **Fitur Utama ($X_2$):** Mengukur durasi tidur pasif berdasarkan kondisi gawai diletakkan di ruangan gelap/telungkup pada pukul 22.00 - 06.00. |
| **`sensing_conversation.xlsx`** | Sensor Gawai (Pasif) | Durasi Percakapan Harian (*Conversation Duration*) | **Fitit Utama ($X_3$):** Log mikrofon pasif untuk mengukur isolasi sosial (mahasiswa stres/depresi cenderung menarik diri dan jarang berbicara). |
| **`other_app_usage.csv`** | Log Gawai (Pasif) | Kategori Aplikasi (Sosial Media vs. Produktivitas) | **Fitur Utama ($X_4$):** Mengukur kecenderungan prokrastinasi (durasi buka Instagram/Tiktok) vs belajar (aplikasi produktivitas). |
| **`other_call_log.xlsx`** & **`other_sms.xlsx`** | Log Komunikasi (Pasif) | Frekuensi Kontak Sosial (Panggilan & SMS) | **Fitur Tambahan ($X_5$):** Mengukur penurunan interaksi sosial aktif mahasiswa sebagai indikator awal kelelahan emosional. |

---

## 3. Contoh Hasil Akhir Matriks Data untuk ML

Setelah data sensor pasif selesai diagregasikan dan digabungkan dengan label kuesioner, Anda akan mendapatkan tabel akhir seperti ini yang siap dimasukkan ke model ML:

| UID | Rata-rata Screen-time (Jam/Hari) | Rata-rata Unlock (Kali/Hari) | Rata-rata Tidur (Jam/Malam) | Durasi Sosial (Menit/Hari) | Label Target (Stres/Depresi) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `u01` | 6.8 | 85 | 5.2 | 45 | **1** (Stres) |
| `u02` | 3.2 | 30 | 7.5 | 120 | **0** (Normal) |
| `u03` | 7.5 | 92 | 4.8 | 15 | **1** (Stres) |
| `u04` | 4.1 | 42 | 6.8 | 90 | **0** (Normal) |
