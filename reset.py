import app

def utama():
    app.log('Mereset Pengaturan Default')
    app.reset_default_settings()
    app.log('Mereset Pengaturan Default Selesai')

if __name__ == '__main__':
    utama()
