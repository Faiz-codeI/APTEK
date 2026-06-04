# Panduan Langkah Analisis Data: Deteksi Dini Burnout & Kesehatan Mental

Dokumen ini menjelaskan alur analisis data secara taktis menggunakan **StudentLife Dataset** yang telah diunduh, mulai dari prapemrosesan hingga pemodelan *Machine Learning*.

---

## 1. Alur Kerja Analisis (Data Pipeline)

```
[ Data Mentah Pasif (Time-Series) ] ➔ [ Agregasi Fitur per Mahasiswa (UID) ] 
                                                                 ↓ (Join on UID)
[ Data Kuesioner (Surveys/Labels) ] ➔ [ Penentuan Label Target (0 / 1) ] 
                                                                 ↓
                                     [ Matriks Data Akhir (X & y) ]
                                                                 ↓
                                     [ Split Data & Pemodelan ML ]
```

---

## 2. Prapemrosesan & *Feature Engineering* (Python/Pandas)

Data pasif (seperti `phonelock.Rds` dan `dark.Rds`) berbentuk catatan timestamp log kejadian. Kita harus mengubahnya menjadi metrik agregat per individu (`uid`) selama rentang waktu studi (misalnya: rata-rata per hari).

### Langkah A: Menghitung Rata-Rata Screen Time & Unlock Frequency
Tabel `phonelock` mencatat kapan layar dikunci dan dibuka.
*   **Fitur yang diekstrak:** 
    1. Durasi penggunaan layar per hari (dalam jam).
    2. Frekuensi membuka kunci (*unlock frequency*) per hari.

```python
import pandas as pd
import pyreadr

# Baca data
df_lock = pyreadr.read_r("dataset_studentlife/dataset_rds/sensing/phonelock.Rds")[None]

# Konversi timestamp ke tipe datetime
df_lock['start'] = pd.to_datetime(df_lock['start'])
df_lock['end'] = pd.to_datetime(df_lock['end'])

# Hitung durasi setiap kali layar menyala (dalam jam)
df_lock['duration_hours'] = (df_lock['end'] - df_lock['start']).dt.total_seconds() / 3600.0

# Kelompokkan per UID dan Tanggal untuk mendapatkan rata-rata harian
df_lock['date'] = df_lock['start'].dt.date
daily_lock = df_lock.groupby(['uid', 'date']).agg(
    daily_screentime=('duration_hours', 'sum'),
    daily_unlocks=('start', 'count')
).reset_index()

# Dapatkan rata-rata akhir per mahasiswa (UID)
student_sensing_features = daily_lock.groupby('uid').agg(
    avg_screentime=('daily_screentime', 'mean'),
    avg_unlocks=('daily_unlocks', 'mean')
).reset_index()
```

### Langkah B: Ekstraksi Durasi Tidur Pasif (Malam Hari)
Tabel `dark` mencatat durasi gawai berada dalam kegelapan (kondisi terkunci, layar mati, dan diletakkan telungkup/di kantong saat malam hari).
*   **Fitur yang diekstrak:** Rata-rata durasi tidur malam (diambil dari log jam 22.00 - 06.00).

```python
df_dark = pyreadr.read_r("dataset_studentlife/dataset_rds/sensing/dark.Rds")[None]
df_dark['start'] = pd.to_datetime(df_dark['start'])
df_dark['end'] = pd.to_datetime(df_dark['end'])
df_dark['duration_hours'] = (df_dark['end'] - df_dark['start']).dt.total_seconds() / 3600.0

# Filter log yang terjadi pada malam hari (22:00 - 06:00)
df_dark['hour'] = df_dark['start'].dt.hour
df_night_dark = df_dark[(df_dark['hour'] >= 22) | (df_dark['hour'] <= 6)]

# Agregasikan harian dan rata-ratakan per mahasiswa
daily_dark = df_night_dark.groupby(['uid', df_night_dark['start'].dt.date])['duration_hours'].sum().reset_index()
student_sleep_features = daily_dark.groupby('uid')['duration_hours'].mean().reset_name('avg_sleep_duration')
```

---

## 3. Penentuan Label Target (Ground Truth)

Kita menggunakan data survei depresi (PHQ-9) atau stress (PSS) untuk menentukan label target klasifikasi.
*   **PHQ-9 Score:** Total skor berkisar antara 0 - 27.
    *   Skor 0-9: Depresi Ringan/Normal (Label `0`).
    *   Skor >= 10: Depresi Sedang hingga Berat / Berisiko (Label `1`).

```python
df_phq = pyreadr.read_r("dataset_studentlife/dataset_rds/survey/PHQ-9.Rds")[None]

# Hitung total skor PHQ-9 (survey dilakukan sebelum [pre] dan sesudah [post] semester)
# Kita bisa ambil rata-rata skor atau fokus pada skor 'post' (akhir semester)
df_phq_post = df_phq[df_phq['type'] == 'post'] # Mengambil kondisi akhir semester

# Tentukan label biner
df_phq_post['label_depresi'] = (df_phq_post['score'] >= 10).astype(int)
df_labels = df_phq_post[['uid', 'label_depresi']]
```

---

## 4. Penggabungan Data (*Dataset Merging*)

Gabungkan fitur sensor pasif (`X`) dengan label target kesehatan mental (`y`) berdasarkan kolom `uid` (User ID).

```python
# Join seluruh tabel fitur dan label
df_final = student_sensing_features.merge(student_sleep_features, on='uid', how='inner')
df_final = df_final.merge(df_labels, on='uid', how='inner')

# Tentukan matriks fitur (X) dan target (y)
X = df_final[['avg_screentime', 'avg_unlocks', 'avg_sleep_duration']]
y = df_final['label_depresi']
```

---

## 5. Pemodelan Machine Learning & Evaluasi

Sebagai mahasiswa Statistika, Anda perlu melatih model klasifikasi dan membandingkan kinerjanya.

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE

# 1. Split Data (Training 80%, Testing 20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 2. Penanganan Class Imbalance menggunakan SMOTE
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# 3. Standardisasi Fitur (Sangat penting terutama untuk SVM)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_res)
X_test_scaled = scaler.transform(X_test)

# 4. Pelatihan Model SVM
svm_model = SVC(kernel='rbf', probability=True, random_state=42)
svm_model.fit(X_train_scaled, y_train_res)
y_pred_svm = svm_model.predict(X_test_scaled)

# 5. Pelatihan Model Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_res, y_train_res) # Random Forest tidak wajib scaling
y_pred_rf = rf_model.predict(X_test)

# 6. Evaluasi Hasil
print("=== PERFORMA SVM ===")
print(classification_report(y_test, y_pred_svm))
print("AUC-ROC SVM:", roc_auc_score(y_test, svm_model.predict_proba(X_test_scaled)[:, 1]))

print("\n=== PERFORMA RANDOM FOREST ===")
print(classification_report(y_test, y_pred_rf))
print("AUC-ROC RF:", roc_auc_score(y_test, rf_model.predict_proba(X_test)[:, 1]))
```

---

## 6. Penafsiran & Analisis Statistika (Interpretability)

Setelah model selesai, lakukan analisis signifikansi fitur untuk menjawab rumusan masalah Anda:
1.  **Feature Importance (Random Forest):** 
    Gunakan `rf_model.feature_importances_` untuk mengekstrak variabel apa yang paling berkontribusi pada risiko burnout (misalnya: apakah durasi layar lebih penting daripada kurang tidur).
2.  **Korelasi Korelatif (Statistika Non-Parametrik):**
    Karena data perilaku gawai sering kali tidak berdistribusi normal, gunakan **Korelasi Rank Spearman** antara variabel sensor pasif (misal: rata-rata aktivitas malam hari) dengan skor kuesioner stres (PSS-10) mahasiswa.
