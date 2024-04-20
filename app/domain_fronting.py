import random
import socket
import select
import threading
from .app import *  # Mengimpor file atau modul bernama 'app'

class domain_fronting(threading.Thread):
    def __init__(self, socket_client, frontend_domains):
        super(domain_fronting, self).__init__()

        self.frontend_domains = frontend_domains  # Daftar domain frontend yang akan digunakan
        self.socket_tunnel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Membuat socket untuk terowongan
        self.socket_client = socket_client  # Socket klien
        self.buffer_size = 65535  # Ukuran buffer untuk pembacaan data
        self.daemon = True  # Menandai thread sebagai daemon untuk mengakhiri otomatis saat program utama selesai

    def log(self, value, status='INFO', color='[G1]'):
        log(value, status=status, color=color)  # Fungsi untuk mencatat pesan dengan status dan warna tertentu

    def handler(self, socket_tunnel, socket_client, buffer_size):
        sockets = [socket_tunnel, socket_client]  # Daftar socket yang akan dimonitor
        timeout = 0  # Inisialisasi waktu timeout
        while True:
            timeout += 1  # Menambah waktu timeout
            socket_io, _, errors = select.select(sockets, [], sockets, 3)  # Memilih socket yang siap untuk I/O atau memiliki kesalahan
            if errors: break  # Jika ada kesalahan pada socket, keluar dari loop
            if socket_io:
                for sock in socket_io:
                    try:
                        data = sock.recv(buffer_size)  # Menerima data dari socket
                        if not data: break  # Jika tidak ada data, keluar dari loop
                        # Meneruskan data dari satu socket ke socket lainnya
                        elif sock is socket_client:
                            socket_tunnel.sendall(data)
                        elif sock is socket_tunnel:
                            socket_client.sendall(data)
                        timeout = 0  # Mengatur ulang waktu timeout
                    except: break  # Jika terjadi kesalahan, keluar dari loop
            if timeout == 30: break  # Jika waktu timeout mencapai 30, keluar dari loop

    def run(self):
        try:
            self.proxy_host_port = random.choice(self.frontend_domains).split(':')  # Memilih secara acak domain frontend dan memisahkan host dan port
            self.proxy_host = self.proxy_host_port[0]  # Host proxy
            self.proxy_port = self.proxy_host_port[1] if len(self.proxy_host_port) >= 2 and self.proxy_host_port[1] else '80'  # Port proxy, default 80 jika tidak tersedia
            self.socket_tunnel.connect((str(self.proxy_host), int(self.proxy_port)))  # Membuat koneksi ke host dan port proxy
            self.socket_client.sendall(b'HTTP/1.1 200 OK\r\n\r\n')  # Mengirim respons HTTP ke klien
            self.handler(self.socket_tunnel, self.socket_client, self.buffer_size)  # Memanggil handler untuk menangani koneksi
            self.socket_client.close()  # Menutup koneksi klien
            self.socket_tunnel.close()  # Menutup koneksi terowongan
        except OSError:
            self.log('Kesalahan koneksi', color='[R1]')  # Menampilkan pesan kesalahan koneksi
        except TimeoutError:
            self.log('{} tidak merespons'.format(self.proxy_host), color='[R1]')  # Menampilkan pesan jika host proxy tidak merespons
