import os
import json
import threading
import subprocess
from .app import *

class client(threading.Thread):
    def __init__(self, command, port, kuota_data_limit):
        super(client, self).__init__()

        # Batas kuota data yang diizinkan
        self.kuota_data_limit = kuota_data_limit
        # Command yang akan dijalankan dengan port yang ditentukan
        self.command = command.format(port=port)
        self.port = port

        # Inisialisasi kuota data
        self.kuota_data = 0
        self.force_stop = False
        self.connected = False
        self.daemon = True

    def log(self, value, color='[G1]'):
        # Fungsi untuk mencatat log dengan warna tertentu
        log(value, status=self.port, color=color)

    def log_replace(self, value, color='[G1]'):
        # Fungsi untuk mengganti log dengan warna tertentu
        log_replace(value, status=self.port, color=color)

    def size(self, bytes, suffixes=['B', 'KB', 'MB', 'GB'], i=0):
        # Mengkonversi ukuran dalam bytes menjadi format yang lebih mudah dibaca
        while bytes >= 1000 and i < len(suffixes) - 1:
            bytes /= 1000; i += 1
        return '{:.3f} {}'.format(bytes, suffixes[i])

    def http_ping(self):
        # Melakukan ping ke server HTTP
        with open(os.devnull, 'w') as devnull:
            process = subprocess.Popen('storage\\http-ping\\http-ping.exe 141.0.11.241 -n 1 -w 1 -i 0', stdout=devnull, stderr=devnull)
            process.communicate()

    def check_kuota_data(self, received, sent):
        # Memeriksa kuota data yang digunakan
        self.kuota_data += received + sent
        if self.kuota_data_limit > 0 and self.kuota_data >= self.kuota_data_limit and sent == 0 and received <= 20000:
            return False
        return True

    def run(self):
        # Fungsi yang dijalankan saat thread dimulai
        self.log('Menghubungkan')
        while True:
            try:
                self.kuota_data = 0
                process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for line in process.stdout:
                    line = json.loads(line.decode().strip() + '\r')
                    info = line['noticeType']
                    if info in ['Info', 'Alert']: message = line['data']['message']

                    if info == 'BytesTransferred':
                        if not self.check_kuota_data(line['data']['received'], line['data']['sent']):
                            self.log_replace(self.size(self.kuota_data), color='[R1]')
                            break
                        self.log_replace(self.size(self.kuota_data))

                    elif info == 'ActiveTunnel':
                        self.connected = True
                        self.log('Terhubung', color='[Y1]')

                    elif info == 'Info':
                        if 'Tidak dapat melakukan koneksi karena mesin tujuan menolak secara aktif.' in message or \
                         'Metrik memori di psiphon' in message or \
                         'meek connection is closed' in message or \
                         'meek connection has closed' in message or \
                         'no such host' in message:
                            continue

                    elif info == 'Alert':
                        if 'SOCKS proxy accept error' in message:
                            if not self.connected: break

                        elif 'meek round trip failed' in message:
                            if self.connected:
                                self.log('Pertukaran data gagal', color='[R1]')
                                break

                        elif 'Upaya koneksi gagal karena pihak yang terhubung tidak merespons dengan benar setelah jangka waktu tertentu' in message or \
                         'Tidak dapat melakukan koneksi karena mesin tujuan menolak secara aktif.' in message or \
                         'dibatalkan konteks' in message or \
                         'Permintaan API ditolak' in message or \
                         'close tunnel ssh error' in message or \
                         'tactics request failed' in message or \
                         'unexpected status code:' in message or \
                         'meek connection is closed' in message or \
                         'meek connection has closed' in message or \
                         'psiphon.(*MeekConn).relay#787:' in message or \
                         'no such host' in message:
                            continue

                        elif 'psiphon.(*Tunnel).sendSshKeepAlive#1295:' in message or \
                         'psiphon.(*Tunnel).SendAPIRequest#342:' in message or \
                         'psiphon.(*Tunnel).Activate#225:' in message or \
                         'meek read payload failed' in message or \
                         'underlying conn is closed' in message or \
                         'tunnel failed:' in message:
                            self.log('Koneksi ditutup', color='[R1]')
                            break

                        else: self.log(line, color='[R1]')
            except json.decoder.JSONDecodeError:
                self.force_stop = True
                self.log('Proses lain sedang berjalan!', color='[R1]')
            except KeyboardInterrupt:
                pass
            finally:
                if self.force_stop: break
                try:
                    process.kill()
                    if self.connected == True:
                        self.connected = False
                        self.http_ping()
                    self.log('Menghubungkan kembali ({})'.format(self.size(self.kuota_data)))
                except Exception as exception:
                    self.log('Exception: {}'.format(exception), color='[R1]')
                    self.log('Berhenti', color='[R1]')
                    break
