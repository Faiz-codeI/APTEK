import os
import urllib.request
import zipfile
import ssl

def download_and_extract():
    # Bypass SSL verification for python urlopen
    ssl._create_default_https_context = ssl._create_unverified_context

    url = "https://zenodo.org/records/3529253/files/dataset_rds.zip?download=1"
    zip_path = "dataset_rds.zip"
    extract_dir = "dataset_studentlife"

    print("=== Mendownload StudentLife Dataset dari Zenodo ===")
    print(f"URL: {url}")
    print("Mengunduh file (ini mungkin memakan waktu beberapa menit)...")
    
    try:
        # Download file
        urllib.request.urlretrieve(url, zip_path)
        print("Unduhan selesai!")
        
        # Extract file
        print(f"Mengekstrak file ke folder '{extract_dir}'...")
        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)
            
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
        print("Ekstraksi selesai!")
        
        # Hapus file zip setelah diekstrak
        os.remove(zip_path)
        print("File zip sementara telah dihapus.")
        print(f"\nSukses! Data tersimpan di folder '{extract_dir}/'.")
        
        # List files in the folder
        files = os.listdir(extract_dir)
        print("\nBerkas yang berhasil diunduh:")
        for file in files:
            print(f"- {file}")
            
    except Exception as e:
        print(f"\nTerjadi kesalahan: {e}")

if __name__ == "__main__":
    download_and_extract()
