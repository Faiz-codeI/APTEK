# Contoh Kode Pembacaan Data StudentLife (.Rds) di Python & R
# Dibuat untuk menunjang pengerjaan analisis data Anda.

"""
=========================================
1. CARA MEMBACA DATA DI PYTHON (Pandas)
=========================================
Untuk membaca file .Rds di Python, Anda memerlukan pustaka `pyreadr`.
Pustaka ini membaca objek RData/RDS dan mengonversinya menjadi Pandas DataFrame secara otomatis.

Instalasi:
pip install pyreadr

Contoh Kode Python:
\"\"\"
import pyreadr
import pandas as pd

# Contoh 1: Membaca data stress survey (Kuesioner Perceived Stress Scale)
pss_data = pyreadr.read_r("dataset_studentlife/dataset_rds/survey/PerceivedStressScale.Rds")
df_pss = pss_data[None]  # Objek RDS tunggal diekstrak dengan key [None]
print("--- Data Kuesioner Stres (PSS) ---")
print(df_pss.head())

# Contoh 2: Membaca data durasi pemakaian kunci layar (Phone Lock pasif)
phonelock_data = pyreadr.read_r("dataset_studentlife/dataset_rds/sensing/phonelock.Rds")
df_lock = phonelock_data[None]
print("\n--- Data Pasif Phone Lock ---")
print(df_lock.head())
\"\"\"


=========================================
2. CARA MEMBACA DATA DI R (RStudio)
=========================================
Di R, pembacaan file .Rds sangat sederhana karena merupakan format bawaan R.
Anda hanya perlu menggunakan fungsi `readRDS()`.

Contoh Kode R:
\"\"\"R
# Load data kuesioner depresi (PHQ-9)
phq_data <- readRDS("dataset_studentlife/dataset_rds/survey/PHQ-9.Rds")
head(phq_data)

# Load data kuesioner stres harian (EMA Stress)
ema_stress <- readRDS("dataset_studentlife/dataset_rds/EMA/Stress.Rds")
head(ema_stress)

# Load data pasif durasi tidur (Darkness/Sensor Cahaya)
dark_data <- readRDS("dataset_studentlife/dataset_rds/sensing/dark.Rds")
head(dark_data)

# Menggabungkan data (Join) berdasarkan kolom UID (User ID)
library(dplyr)
combined_data <- inner_join(phq_data, ema_stress, by = "uid")
head(combined_data)
\"\"\"
"""

import os

# Cek ketersediaan file-file utama
survey_path = "dataset_studentlife/dataset_rds/survey/PerceivedStressScale.Rds"
sensing_path = "dataset_studentlife/dataset_rds/sensing/phonelock.Rds"

if os.path.exists(survey_path) and os.path.exists(sensing_path):
    print("Contoh lokasi file siap:")
    print(f"- File Survei Stres: {survey_path}")
    print(f"- File Sensor Layar: {sensing_path}")
    print("\nSilakan gunakan template kode di atas untuk membaca data menggunakan Python (pyreadr) atau R.")
else:
    print("File data tidak ditemukan. Pastikan Anda telah menjalankan download_dataset.py terlebih dahulu.")
