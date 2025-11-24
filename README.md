# Indihome Inject Data

> **Peringatan:** :red_circle: Alat ini dibuat khusus untuk keperluan pendidikan dan penelitian. Penulis tidak bertanggung jawab atas segala bentuk penyalahgunaan atau kerusakan yang mungkin timbul dari penggunaan skrip ini. Harap gunakan dengan bijak dan hanya di lingkungan di mana Anda memiliki izin eksplisit.

**Indihome Inject Data** adalah tool yang dirancang khusus untuk kebutuhan *testing* pada jaringan WiFi Indihome. Aplikasi ini memungkinkan pengguna melakukan injeksi data secara terkontrol untuk keperluan uji coba, analisis jaringan, atau kebutuhan darurat ketika akses internet mengalami gangguan. Tool ini **tidak ditujukan untuk penggunaan sehari-hari**, tetapi lebih sebagai solusi teknis bagi pengguna yang memahami risiko dan ingin melakukan pemeriksaan koneksi secara mendalam.

Sebagai versi *stable*, rilis ini membawa peningkatan pada performa sistem, stabilitas API Windows, serta kompatibilitas yang lebih baik dengan proses multi-core. Indihome Inject Data memungkinkan pengguna memilih jumlah core, menentukan paket data untuk reset (mulai dari 4MB hingga 2GB), serta menjalankan proses injeksi melalui engine berbasis Python yang telah dioptimalkan.

Aplikasi ini sangat bermanfaat untuk aktivitas seperti *testing download*, streaming file berukuran besar, hingga membuka situs yang diblokir atau terkena Internet Positif. Untuk menjaga keamanan, disarankan agar tool hanya digunakan pada jaringan milik sendiri dan tidak digunakan untuk login ke akun pribadi seperti Facebook, Gmail, YouTube, atau akun media sosial lainnya.

#
<b>[ Cara Install Indihome Inject Data ]</b>

1. Download dan instal python3 (minimum python 3.5): https://www.python.org/downloads/
2. Download dan instal Git: https://git-scm.com/downloads
```
git clone https://github.com/MichaelJorky/indihome-inject-data.git .ijd-tunnel
```
```
cd .ijd-tunnel
```
```
python -m pip install colorama
```
```
git pull
```
3. Buka aplikasi "Indihome Inject Data.exe" lalu pilih "Select Core" dari 1-10 dan disarankan tidak menggunakan core yang banyak dan sesuaikan dengan spesifikasi laptop maupun pc sobat dan untuk pengujian pilih dari core 1 atau core 2, kemudian "Select Data" untuk reset data tersedia mulai dari 4MB-2GB silahkan lakukan pengujian mulai dari reset data yang terkecil dulu.
4. Tidak disarankan digunakan untuk login akun utama seperti login akun x, login akun facebook, login akun youtube, login gmail dan lain lain.
5. Tool ini sangat cocok sekali untuk download file besar dan nonton film atau membuka situs yang terkena internet positif, dan apabila menggunakan antivirus smadav jangan lupa daftarkan foldernya ke bagian whitelist smadav (Settings -> Scanner Settings -> Manage -> Add File/Add Folder) yang terpenting adalah whitelist proxifiernya .ijd-tunnel\storage\proxifier\Proxifier.exe.
