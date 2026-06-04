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

add_md("# 🧠 Analisis Klasifikasi Risiko Burnout Mahasiswa (Data Panel Harian)\n"
       "Notebook ini menggunakan dataset panel harian (**2.263 baris**) yang dikompilasi di folder `dataset_baru/`. "
       "Kita akan melatih model Machine Learning (Random Forest & SVM) untuk memprediksi apakah pola perilaku harian mahasiswa mengindikasikan kecenderungan burnout.")

add_code('''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import warnings
warnings.filterwarnings('ignore')''')

add_md("## 1. Memuat Dataset Panel Harian\n"
       "Dataset ini menggabungkan data sensor durasi layar aktif (*screentime*), frekuensi buka kunci (*unlocks*), durasi tidur malam, dan durasi percakapan harian.")

add_code('''# Load data
df = pd.read_excel('dataset_baru/daily_panel_data.xlsx')
print("Ukuran Dataset:", df.shape)
print("Distribusi Target (is_burnout):")
print(df['is_burnout'].value_counts())
df.head()''')

add_md("## 2. Pembagian Data (Train-Test Split)\n"
       "Kita akan memisahkan Fitur (X) dan Target Label (y). Data dibagi menjadi 80% untuk pelatihan dan 20% untuk pengujian.")

add_code('''# Fitur sensor pasif
X = df[['screentime_hours', 'unlock_frequency', 'sleep_hours', 'conversation_minutes']]
y = df['is_burnout']

# Split data 80:20 secara stratified agar proporsi kelas tetap seimbang
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Jumlah Data Training:", X_train.shape[0])
print("Jumlah Data Testing:", X_test.shape[0])''')

add_md("## 3. Standardisasi Fitur (Scaling)\n"
       "Proses penskalaan sangat penting agar fitur dengan skala besar (seperti frekuensi unlock) tidak mendominasi fitur berskala kecil (seperti durasi tidur).")

add_code('''scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)''')

add_md("## 4. Pemodelan & Evaluasi")

add_code('''# A. Random Forest Classifier
rf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42, class_weight='balanced')
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print("=== EVALUASI RANDOM FOREST ===")
print(f"Accuracy: {accuracy_score(y_test, y_pred_rf):.4f}")
print(classification_report(y_test, y_pred_rf))''')

add_code('''# B. Support Vector Machine (SVM)
svm = SVC(kernel='rbf', C=1.0, class_weight='balanced', random_state=42)
svm.fit(X_train_scaled, y_train)
y_pred_svm = svm.predict(X_test_scaled)

print("=== EVALUASI SVM ===")
print(f"Accuracy: {accuracy_score(y_test, y_pred_svm):.4f}")
print(classification_report(y_test, y_pred_svm))''')

add_md("## 5. Feature Importance (Analisis Variabel Paling Berpengaruh)\n"
       "Melihat variabel mana yang paling berkorelasi dengan risiko burnout mahasiswa.")

add_code('''importances = rf.feature_importances_
feature_names = X.columns
df_imp = pd.DataFrame({'Feature': feature_names, 'Importance': importances}).sort_values(by='Importance', ascending=False)

print("=== VARIABEL PALING BERPENGARUH ===")
print(df_imp.to_string(index=False))

# Plot Feature Importance
plt.figure(figsize=(8, 5))
plt.barh(df_imp['Feature'], df_imp['Importance'], color='skyblue')
plt.xlabel('Importance Score')
plt.title('Faktor Sensor Pasif Paling Mempengaruhi Burnout')
plt.gca().invert_yaxis()
plt.show()''')

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
print("Notebook berhasil diperbarui untuk membaca dataset_baru!")
