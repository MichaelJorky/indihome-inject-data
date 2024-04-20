import os
import app
import time
import json
from subprocess import Popen

# Fungsi untuk mendapatkan path sebenarnya dari suatu file
def real_path(nama_file):
    return os.path.dirname(os.path.abspath(__file__)) + nama_file

def main():
    try:
        app.default_settings()  # Mengatur pengaturan default dari aplikasi
        config = json.loads(open(real_path('/config/config.json')).read())  # Membaca file konfigurasi
        config_core = config['core']  # Mendapatkan konfigurasi inti
        config_kuota_data_limit = config['kuota_data_limit']  # Mendapatkan batas kuota data
    except:
        app.log('Kesalahan konfigurasi, silakan jalankan reset.py terlebih dahulu!', color='[R1]')  # Log kesalahan jika terjadi
        return

    app.inject('127.0.0.1', '8080').start()  # Menjalankan aplikasi
    time.sleep(1.500)  # Memberi jeda 1.5 detik

    try:
        command = 'storage\\psiphon\\{port}\\psiphon-tunnel-core.exe -config storage/psiphon/{port}/config/psiphon-tunnel-core.json'
        for core in range(config_core):
            port = 3080 + core
            app.client(command, port, config_kuota_data_limit).start()  # Menjalankan klien aplikasi dengan port yang berbeda-beda
            time.sleep(0.200)  # Memberi jeda 0.2 detik setiap iterasi
        with open(os.devnull, 'w') as devnull:
            process = Popen('ping.exe 141.0.11.241 -t', stdout=devnull, stderr=devnull)  # Menjalankan ping ke alamat tertentu
            process.communicate()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()  # Memanggil fungsi main jika file ini dijalankan langsung sebagai program utama
