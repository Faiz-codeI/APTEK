import os
import pandas as pd
import numpy as np

# 1. Buat folder dataset_baru jika belum ada
os.makedirs('dataset_baru', exist_ok=True)

print("Mulai memproses data panel harian...")

# A. Ambil data Phonelock (durasi layar aktif dan buka kunci)
print("1. Membaca Phonelock...")
df_lock = pd.read_excel('dataset_studentlife_excel/sensing_phonelock.xlsx')
df_lock['start'] = pd.to_datetime(df_lock['start_timestamp'], unit='s')
df_lock['date'] = df_lock['start'].dt.date
df_lock['duration'] = (pd.to_datetime(df_lock['end_timestamp'], unit='s') - df_lock['start']).dt.total_seconds() / 3600.0
lock_daily = df_lock.groupby(['uid', 'date']).agg(
    screentime_hours=('duration', 'sum'),
    unlock_frequency=('start_timestamp', 'count')
).reset_index()

# B. Ambil data Tidur/Kegelapan (sleep duration)
print("2. Membaca Sensor Kegelapan/Tidur...")
df_dark = pd.read_excel('dataset_studentlife_excel/sensing_dark.xlsx')
df_dark['start'] = pd.to_datetime(df_dark['start_timestamp'], unit='s')
df_dark['date'] = df_dark['start'].dt.date
df_dark['duration'] = (pd.to_datetime(df_dark['end_timestamp'], unit='s') - df_dark['start']).dt.total_seconds() / 3600.0
# Ambil hanya malam hari
df_night = df_dark[(df_dark['start'].dt.hour >= 22) | (df_dark['start'].dt.hour <= 6)]
sleep_daily = df_night.groupby(['uid', 'date']).agg(
    sleep_hours=('duration', 'sum')
).reset_index()

# C. Ambil data Percakapan (sosial)
print("3. Membaca Sensor Percakapan...")
df_conv = pd.read_excel('dataset_studentlife_excel/sensing_conversation.xlsx')
df_conv['start'] = pd.to_datetime(df_conv['start_timestamp'], unit='s')
df_conv['date'] = df_conv['start'].dt.date
df_conv['duration'] = (pd.to_datetime(df_conv['end_timestamp'], unit='s') - df_conv['start']).dt.total_seconds() / 60.0
conv_daily = df_conv.groupby(['uid', 'date']).agg(
    conversation_minutes=('duration', 'sum')
).reset_index()

# D. Gabungkan fitur-fitur sensor harian
print("4. Menggabungkan fitur sensor...")
merged = pd.merge(lock_daily, sleep_daily, on=['uid', 'date'], how='outer')
merged = pd.merge(merged, conv_daily, on=['uid', 'date'], how='outer')

# Isi data kosong dengan 0 (karena tidak ada aktivitas terekam sensor)
merged = merged.fillna(0)

# E. Ambil Label Target PHQ-9 (Stres/Burnout)
print("5. Menghitung Target Label PHQ-9...")
df_phq = pd.read_excel('dataset_studentlife_excel/surveys.xlsx', sheet_name='PHQ-9')
df_phq = df_phq[df_phq['type'] == 'post'].copy()
phq_mapping = {'Not at all': 0, 'Several days': 1, 'More than half the days': 2, 'Nearly every day': 3}
cols = [f'Q{i}' for i in range(1, 10)]
for c in cols:
    df_phq[c] = df_phq[c].map(phq_mapping).fillna(0)
df_phq['total_score'] = df_phq[cols].sum(axis=1)
# Threshold >= 6 (Stres Ringan - Berat)
df_phq['is_burnout'] = (df_phq['total_score'] >= 6).astype(int)
df_labels = df_phq[['uid', 'is_burnout']]

# F. Gabungkan Fitur dan Label
print("6. Menyaring mahasiswa dengan data survey lengkap...")
final_panel = pd.merge(merged, df_labels, on='uid', how='inner')

# Urutkan berdasarkan UID dan Tanggal
final_panel = final_panel.sort_values(by=['uid', 'date']).reset_index(drop=True)

# G. Simpan ke folder dataset_baru
excel_path = 'dataset_baru/daily_panel_data.xlsx'
csv_path = 'dataset_baru/daily_panel_data.csv'

print(f"7. Menyimpan file ke {excel_path} dan {csv_path}...")
final_panel.to_excel(excel_path, index=False)
final_panel.to_csv(csv_path, index=False)

print("Proses Selesai!")
print("Jumlah Baris Data Hasil Akhir:", final_panel.shape[0])
print("Jumlah Baris Kelas 0 (Normal):", (final_panel['is_burnout'] == 0).sum())
print("Jumlah Baris Kelas 1 (Burnout):", (final_panel['is_burnout'] == 1).sum())
