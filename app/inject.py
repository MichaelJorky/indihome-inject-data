import socket
import threading
from .app import *
from .domain_fronting import *

class inject(threading.Thread):
    def __init__(self, inject_host, inject_port):
        super(inject, self).__init__()

        self.inject_host = str(inject_host)
        self.inject_port = int(inject_port)

    def log(self, value, color='[G1]'):
        log(value, color=color)

    def run(self):
        try:
            # Membuat socket server
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Mengikat socket ke alamat dan port yang ditentukan
            socket_server.bind((self.inject_host, self.inject_port))
            # Mendengarkan koneksi masuk, dengan maksimal 1 koneksi dalam antrian
            socket_server.listen(1)
            # Membaca daftar domain frontend dari file frontend-domains.txt
            frontend_domains = open(real_path('/../config/frontend-domains.txt')).readlines()
            # Membersihkan daftar domain dari spasi atau karakter newline
            frontend_domains = filter_array(frontend_domains)
            # Jika tidak ada domain frontend yang ditemukan, memberikan pesan kesalahan
            if len(frontend_domains) == 0:
                self.log('Domain Frontend tidak ditemukan. Silakan periksa config/frontend-domains.txt', color='[R1]')
                self.log('Aturan Proksifikasi Psiphon berubah menjadi langsung', color='[R1]')
                return
            # Memberitahu bahwa Domain Fronting sedang berjalan pada host dan port tertentu
            self.log('Domain Fronting berjalan pada {} port {}'.format(self.inject_host, self.inject_port))
            # Menghandle koneksi masuk secara terus menerus
            while True:
                # Menerima koneksi dari client
                socket_client, _ = socket_server.accept()
                # Menerima data dari client (maksimal 65535 byte) tapi tidak digunakan
                socket_client.recv(65535)
                # Memulai proses domain fronting untuk koneksi client
                domain_fronting(socket_client, frontend_domains).start()
        except Exception as exception:
            # Memberitahu bahwa Domain Fronting tidak berjalan pada host dan port tertentu karena terjadi exception
            self.log('Domain Fronting tidak berjalan pada {} port {}'.format(self.inject_host, self.inject_port), color='[R1]')
            # Menampilkan informasi tentang exception yang terjadi
            self.log('Exception: {}'.format(exception), color='[R1]')
