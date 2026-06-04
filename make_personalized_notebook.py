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

add_md("# 🧠 Analisis Klasifikasi Risiko Burnout Mahasiswa (Personalized Passive Sensing)\n"
       "Notebook ini menggunakan teknik **Standardisasi Relatif Individu (Personalized Scaling)**. "
       "Setiap mahasiswa memiliki kebiasaan dasar (*baseline*) yang unik (misal: durasi tidur normal orang berbeda-beda). "
       "Dengan menstandardisasi sensor terhadap rata-rata historis mahasiswa itu sendiri, kita dapat mendeteksi penyimpangan perilaku harian secara akurat.")

add_code('''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')''')

add_md("## 1. Memuat Dataset Harian")
add_code('''df = pd.read_excel('dataset_baru/daily_panel_data.xlsx')
print("Ukuran Data:", df.shape)
df.head()''')

add_md("## 2. Personalized Feature Engineering\n"
       "Kita menstandardisasi fitur sensor harian per individu mahasiswa (UID). Rumusnya:\n"
       "$$X_{norm} = \\frac{X_{harian} - \\mu_{UID}}{\\sigma_{UID}}$$")

add_code('''features = ['screentime_hours', 'unlock_frequency', 'sleep_hours', 'conversation_minutes']

for f in features:
    # Hitung rata-rata dan standar deviasi per UID mahasiswa
    mean_val = df.groupby('uid')[f].transform('mean')
    std_val = df.groupby('uid')[f].transform('std')
    
    # Standardisasi relatif individu (tambahkan epsilon 1e-5 untuk mencegah pembagian dengan nol)
    df[f + '_norm'] = (df[f] - mean_val) / (std_val + 1e-5)

print("Fitur Hasil Standardisasi Relatif:")
df[[col for col in df.columns if '_norm' in col or col == 'uid']].head()''')

add_md("## 3. Pembagian Data (Train-Test Split)")
add_code('''# Gunakan fitur yang sudah dinormalisasi secara personal
X = df[[f + '_norm' for f in features]]
y = df['is_burnout']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Jumlah Sampel Training:", X_train.shape[0])
print("Jumlah Sampel Testing:", X_test.shape[0])''')

add_md("## 4. Pelatihan Model ML")

add_code('''# A. Random Forest Classifier dengan Parameter Ter-Tuning
rf = RandomForestClassifier(
    n_estimators=200, 
    max_depth=10, 
    min_samples_split=5, 
    class_weight='balanced', 
    random_state=42
)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print("=== EVALUASI RANDOM FOREST ===")
print(f"Accuracy: {accuracy_score(y_test, y_pred_rf):.4f}")
print(classification_report(y_test, y_pred_rf))''')

add_code('''# B. Support Vector Machine (SVM)
# SVM menggunakan data berskala personal
svm = SVC(kernel='rbf', C=1.5, class_weight='balanced', random_state=42)
svm.fit(X_train, y_train)
y_pred_svm = svm.predict(X_test)

print("=== EVALUASI SVM ===")
print(f"Accuracy: {accuracy_score(y_test, y_pred_svm):.4f}")
print(classification_report(y_test, y_pred_svm))''')

add_md("## 5. Visualisasi Faktor Paling Mempengaruhi Burnout (Random Forest)")
add_code('''importances = rf.feature_importances_
df_imp = pd.DataFrame({
    'Sensor': ['Screen-time', 'Unlock Frequency', 'Sleep Duration', 'Conversation Duration'],
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print("=== FEATURE IMPORTANCE ===")
print(df_imp.to_string(index=False))

# Plot
plt.figure(figsize=(8, 5))
plt.barh(df_imp['Sensor'], df_imp['Importance'], color='teal')
plt.xlabel('Importance Score')
plt.title('Faktor Sensor Pasif Paling Mempengaruhi Burnout Mahasiswa')
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
print("Notebook berhasil diperbarui dengan metode Personalized Normalization!")
