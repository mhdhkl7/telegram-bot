# 🤖 Telegram Customer Service Bot

Bot Telegram interaktif yang dirancang untuk mengotomatisasi layanan pelanggan dasar, ditenagai oleh Python dan database cloud MongoDB. Proyek ini dibangun sebagai portofolio untuk menunjukkan kemampuan pengembangan backend, integrasi API, dan deployment aplikasi.

![Contoh Penggunaan Bot](URL_GIF_DEMO_BOT_ANDA) 
---

## 📜 Deskripsi Proyek

Bot ini diciptakan untuk membantu pemilik bisnis kecil dan menengah dalam menangani pertanyaan yang sering diajukan (FAQ) oleh pelanggan mereka secara otomatis. Daripada menjawab pertanyaan yang sama berulang kali, bot ini menyediakan antarmuka yang bersih dan interaktif bagi pengguna untuk menemukan jawaban. Selain itu, bot ini dilengkapi dengan panel admin sederhana langsung di dalam Telegram, memungkinkan pemilik bisnis untuk mengelola konten FAQ tanpa memerlukan keahlian teknis.

---

## ✨ Fitur Utama

- **FAQ Interaktif:** Pengguna dapat melihat daftar pertanyaan dan mendapatkan jawaban dengan menekan tombol (Inline Keyboard), memberikan pengalaman pengguna yang lebih baik daripada teks biasa.
- **Manajemen Konten via Telegram:** Admin dapat menambah dan menghapus FAQ langsung melalui perintah di Telegram, tanpa perlu mengakses database secara manual.
- **Otorisasi Admin:** Perintah-perintah sensitif seperti menambah atau menghapus konten dilindungi dan hanya bisa diakses oleh admin yang sudah ditentukan User ID-nya.
- **Integrasi Database Cloud:** Semua data FAQ disimpan di MongoDB Atlas, sebuah database cloud yang memastikan data aman dan dapat diakses dari mana saja.
- **Deployment 24/7:** Bot ini di-deploy di platform cloud Railway, memastikannya selalu online dan siap melayani pengguna kapan saja.

---

## 🛠️ Teknologi yang Digunakan

- **Bahasa:** Python 3
- **Library Telegram:** `python-telegram-bot`
- **Database:** MongoDB
- **Hosting Database:** MongoDB Atlas (Cloud)
- **Library Database:** `pymongo`
- **Platform Deployment:** Railway
- **Version Control:** Git & GitHub

---

## 🚀 Cara Menjalankan Proyek Ini Secara Lokal

Untuk menjalankan bot ini di komputermu sendiri, ikuti langkah-langkah berikut:

1.  **Clone repositori ini:**
    ```bash
    git clone [https://github.com/mhdhkl7/telegram-bot.git](https://github.com/mhdhkl7/telegram-bot.git)
    cd telegram-bot
    ```

2.  **Buat dan aktifkan virtual environment:**
    ```bash
    # Untuk Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Untuk macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install semua library yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Siapkan Database:**
    - Buat akun gratis di [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
    - Buat sebuah cluster gratis (M0).
    - Buat user database dan izinkan akses jaringan dari semua IP (`0.0.0.0/0`).
    - Dapatkan *Connection String (URI)*.

5.  **Atur Environment Variables:**
    - Bot ini membutuhkan 3 variabel rahasia. Kamu bisa mengaturnya langsung di terminalmu sebelum menjalankan bot.
    ```bash
    # Contoh di Windows (Command Prompt)
    set TELEGRAM_TOKEN="TOKEN_BOT_ANDA"
    set ADMIN_USER_ID="ID_ADMIN_ANDA"
    set MONGO_URI="URI_MONGODB_ATLAS_ANDA"

    # Contoh di macOS/Linux
    export TELEGRAM_TOKEN="TOKEN_BOT_ANDA"
    export ADMIN_USER_ID="ID_ADMIN_ANDA"
    export MONGO_URI="URI_MONGODB_ATLAS_ANDA"
    ```

6.  **Jalankan Bot:**
    ```bash
    python main.py
    ```

---

## ⚙️ Konfigurasi dan Penggunaan Bot

Bot ini memiliki dua jenis perintah: untuk pengguna biasa dan untuk admin.

#### Perintah Pengguna
- `/start` - Memulai percakapan dengan bot.
- `/help` - Menampilkan daftar perintah yang tersedia.
- `/faq` - Menampilkan daftar pertanyaan yang sering diajukan dalam bentuk tombol interaktif.

#### Perintah Admin
- `/tambah_faq` - Memulai alur percakapan untuk menambahkan pertanyaan dan jawaban baru.
- `/hapus_faq` - Menampilkan daftar FAQ untuk dihapus.
- `/batal` - Membatalkan proses penambahan FAQ.
