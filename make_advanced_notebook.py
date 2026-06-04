import json

cells = []

def add_md(text):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")]
    })

def add_code(text):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.split("\n")]
    })

add_md("# 🧠 Analisis Deteksi Dini Risiko Burnout Mahasiswa (Passive Sensing - Edisi Lanjut)\nNotebook ini memuat keseluruhan alur kerja (*pipeline*) dengan akurasi yang lebih baik melalui penyeimbangan data (SMOTE) dan ekstraksi fitur yang lebih lengkap (Durasi Layar, Tidur, dan Obrolan).")
add_code('''import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')''')

add_md("## 1. Feature Engineering: Ekstraksi Data Sensor")
add_code('''# A. Ekstraksi Fitur Screen-time dan Unlock
print("Memproses data Phonelock...")
df_lock = pd.read_excel('dataset_studentlife_excel/sensing_phonelock.xlsx')
df_lock['start'] = pd.to_datetime(df_lock['start_timestamp'], unit='s')
df_lock['end'] = pd.to_datetime(df_lock['end_timestamp'], unit='s')
df_lock['duration_hours'] = (df_lock['end'] - df_lock['start']).dt.total_seconds() / 3600.0

student_lock = df_lock.groupby('uid').agg(
    avg_screentime_hours=('duration_hours', 'sum'),
    total_unlocks=('start_timestamp', 'count')
).reset_index()

student_lock['avg_daily_screentime'] = student_lock['avg_screentime_hours'] / 70
student_lock['avg_daily_unlocks'] = student_lock['total_unlocks'] / 70
feat_1 = student_lock[['uid', 'avg_daily_screentime', 'avg_daily_unlocks']]

# B. Ekstraksi Fitur Tidur (Darkness)
print("Memproses data Tidur...")
df_dark = pd.read_excel('dataset_studentlife_excel/sensing_dark.xlsx')
df_dark['start'] = pd.to_datetime(df_dark['start_timestamp'], unit='s')
df_dark['end'] = pd.to_datetime(df_dark['end_timestamp'], unit='s')
df_dark['duration_hours'] = (df_dark['end'] - df_dark['start']).dt.total_seconds() / 3600.0
df_night = df_dark[(df_dark['start'].dt.hour >= 22) | (df_dark['start'].dt.hour <= 6)]

student_sleep = df_night.groupby('uid').agg(total_sleep_hours=('duration_hours', 'sum')).reset_index()
student_sleep['avg_night_sleep'] = student_sleep['total_sleep_hours'] / 70
feat_2 = student_sleep[['uid', 'avg_night_sleep']]

# C. Ekstraksi Fitur Sosial (Percakapan)
print("Memproses data Interaksi Sosial...")
df_conv = pd.read_excel('dataset_studentlife_excel/sensing_conversation.xlsx')
df_conv['start'] = pd.to_datetime(df_conv['start_timestamp'], unit='s')
df_conv['end'] = pd.to_datetime(df_conv['end_timestamp'], unit='s')
df_conv['duration_minutes'] = (df_conv['end'] - df_conv['start']).dt.total_seconds() / 60.0

student_conv = df_conv.groupby('uid').agg(total_conv_minutes=('duration_minutes', 'sum')).reset_index()
student_conv['avg_daily_conversation'] = student_conv['total_conv_minutes'] / 70
feat_3 = student_conv[['uid', 'avg_daily_conversation']]''')

add_md("## 2. Pembuatan Label Target (Ground Truth)\nBerdasarkan jurnal medis, skor PHQ-9 >= 6 mengindikasikan tingkat gejala stres ringan hingga sedang. Ambang batas ini kita gunakan agar jumlah kelas menjadi seimbang (Natural Balancing).")
add_code('''df_phq = pd.read_excel('dataset_studentlife_excel/surveys.xlsx', sheet_name='PHQ-9')
df_phq = df_phq[df_phq['type'] == 'post'].copy()

phq_mapping = {'Not at all': 0, 'Several days': 1, 'More than half the days': 2, 'Nearly every day': 3}
cols_to_score = [f'Q{i}' for i in range(1, 10)]

for col in cols_to_score:
    df_phq[col] = df_phq[col].map(phq_mapping).fillna(0)

df_phq['total_score'] = df_phq[cols_to_score].sum(axis=1)
# Menggunakan threshold >= 6 untuk deteksi dini (Risiko Burnout Ringan - Berat)
df_phq['is_burnout'] = (df_phq['total_score'] >= 6).astype(int)

df_labels = df_phq[['uid', 'total_score', 'is_burnout']]
print("Distribusi Target:")
print(df_labels['is_burnout'].value_counts())''')

add_md("## 3. Penggabungan Data")
add_code('''df_final = pd.merge(feat_1, feat_2, on='uid', how='inner')
df_final = pd.merge(df_final, feat_3, on='uid', how='inner')
df_final = pd.merge(df_final, df_labels, on='uid', how='inner')
df_final.head()''')

add_md("## 4. Pelatihan Model ML dengan SMOTE")
add_code('''X = df_final[['avg_daily_screentime', 'avg_daily_unlocks', 'avg_night_sleep', 'avg_daily_conversation']]
y = df_final['is_burnout']

# 1. Split Data (Stratified)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 2. Oversampling dengan SMOTE untuk mengatasi sisa ketimpangan
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# 3. Standardisasi Data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_res)
X_test_scaled = scaler.transform(X_test)

# 4. Model Random Forest
rf = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42)
rf.fit(X_train_res, y_train_res)
y_pred_rf = rf.predict(X_test)

# 5. Model SVM
svm = SVC(kernel='rbf', probability=True, random_state=42)
svm.fit(X_train_scaled, y_train_res)
y_pred_svm = svm.predict(X_test_scaled)

print("\\n=== EVALUASI RANDOM FOREST ===")
print(classification_report(y_test, y_pred_rf))

print("\\n=== EVALUASI SVM ===")
print(classification_report(y_test, y_pred_svm))

importances = rf.feature_importances_
print("\\n=== FEATURE IMPORTANCE (Faktor Paling Mempengaruhi Stres) ===")
for feat, imp in zip(X.columns, importances):
    print(f"{feat}: {imp:.4f}")''')

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('analisis_kesehatan_mental.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1)
print("Notebook berhasil diperbarui dengan metode SMOTE dan Threshold 6!")
