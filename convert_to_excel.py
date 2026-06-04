import os
import sys
import pyreadr
import pandas as pd

def convert_rds_to_excel():
    base_dir = "dataset_studentlife/dataset_rds"
    output_dir = "dataset_studentlife_excel"
    
    if not os.path.exists(base_dir):
        print(f"Error: Direktori data {base_dir} tidak ditemukan!")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("\n=== Proses Konversi data .Rds ke Excel (.xlsx) ===")
    
    # 1. Konversi data survey (PHQ-9, PSS, dll.) ke satu file Excel dengan beberapa sheet
    survey_dir = os.path.join(base_dir, "survey")
    survey_excel_path = os.path.join(output_dir, "surveys.xlsx")
    
    if os.path.exists(survey_dir):
        print("\nMembuat surveys.xlsx...")
        with pd.ExcelWriter(survey_excel_path, engine='openpyxl') as writer:
            for file in os.listdir(survey_dir):
                if file.endswith(".Rds"):
                    name = file.replace(".Rds", "")
                    # Excel sheet name limit is 31 characters
                    sheet_name = name[:30]
                    file_path = os.path.join(survey_dir, file)
                    try:
                        print(f"- Mengonversi survey: {file}")
                        rdata = pyreadr.read_r(file_path)
                        df = rdata[None]
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                    except Exception as e:
                        print(f"  Gagal mengonversi {file}: {e}")
        print(f"Sukses menyimpan: {survey_excel_path}")

    # 2. Konversi data EMA (Stress, Sleep, dll.) ke satu file Excel dengan beberapa sheet
    ema_dir = os.path.join(base_dir, "EMA")
    ema_excel_path = os.path.join(output_dir, "ema_responses.xlsx")
    
    if os.path.exists(ema_dir):
        print("\nMembuat ema_responses.xlsx...")
        with pd.ExcelWriter(ema_excel_path, engine='openpyxl') as writer:
            for file in os.listdir(ema_dir):
                if file.endswith(".Rds"):
                    name = file.replace(".Rds", "")
                    sheet_name = name[:30]
                    file_path = os.path.join(ema_dir, file)
                    try:
                        print(f"- Mengonversi EMA: {file}")
                        rdata = pyreadr.read_r(file_path)
                        df = rdata[None]
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                    except Exception as e:
                        print(f"  Gagal mengonversi {file}: {e}")
        print(f"Sukses menyimpan: {ema_excel_path}")

    # 3. Konversi beberapa data sensing utama (yang berukuran wajar/tidak terlalu besar)
    sensing_dir = os.path.join(base_dir, "sensing")
    if os.path.exists(sensing_dir):
        print("\nMemproses data sensing...")
        
        # File-file yang wajar ukurannya untuk Excel (phonelock, dark, phonecharge, conversation)
        safe_sensing_files = ["phonelock.Rds", "dark.Rds", "phonecharge.Rds", "conversation.Rds"]
        
        for file in safe_sensing_files:
            file_path = os.path.join(sensing_dir, file)
            if os.path.exists(file_path):
                name = file.replace(".Rds", "")
                excel_path = os.path.join(output_dir, f"sensing_{name}.xlsx")
                try:
                    print(f"- Mengonversi sensing: {file}...")
                    rdata = pyreadr.read_r(file_path)
                    df = rdata[None]
                    
                    # Jika data terlalu besar (misal lebih dari 1 juta baris), batasi atau infokan
                    if len(df) > 1048500:
                        csv_path = os.path.join(output_dir, f"sensing_{name}.csv")
                        print(f"  Data terlalu besar untuk Excel ({len(df)} baris). Menyimpan ke CSV...")
                        df.to_csv(csv_path, index=False)
                        print(f"  Sukses menyimpan CSV: {csv_path}")
                    else:
                        df.to_excel(excel_path, index=False)
                        print(f"  Sukses menyimpan: {excel_path}")
                except Exception as e:
                    print(f"  Gagal mengonversi {file}: {e}")

        # Catatan untuk file sensing raksasa (activity, audio, wifi)
        print("\nInfo: File sensing besar (seperti activity.Rds, audio.Rds, wifi.Rds) sengaja tidak dikonversi ke Excel karena ukurannya yang mencapai ratusan megabytes (dapat menyebabkan Excel crash). Disarankan membacanya langsung via Python/R.")

    # 4. Konversi data "other" (app usage, call logs, sms, dll.)
    other_dir = os.path.join(base_dir, "other")
    if os.path.exists(other_dir):
        print("\nMemproses data kategori 'other' (app usage, calls, sms, dll.)...")
        for file in os.listdir(other_dir):
            if file.endswith(".Rds"):
                name = file.replace(".Rds", "")
                file_path = os.path.join(other_dir, file)
                try:
                    print(f"- Mengonversi other: {file}...")
                    rdata = pyreadr.read_r(file_path)
                    df = rdata[None]
                    
                    if len(df) > 1048500:
                        csv_path = os.path.join(output_dir, f"other_{name}.csv")
                        print(f"  Data terlalu besar untuk Excel ({len(df)} baris). Menyimpan ke CSV...")
                        df.to_csv(csv_path, index=False)
                        print(f"  Sukses menyimpan CSV: {csv_path}")
                    else:
                        excel_path = os.path.join(output_dir, f"other_{name}.xlsx")
                        df.to_excel(excel_path, index=False)
                        print(f"  Sukses menyimpan: {excel_path}")
                except Exception as e:
                    print(f"  Gagal mengonversi {file}: {e}")

    print(f"\nSemua proses selesai! Hasil konversi tersimpan di folder '{output_dir}/'.")

if __name__ == "__main__":
    convert_rds_to_excel()
