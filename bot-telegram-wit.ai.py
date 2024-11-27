import os
import requests
import speech_recognition as sr
from telegram import Update
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackContext

import subprocess
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# token bot Telegram Anda
TOKEN = '6751900243:AAHP4XVpxSzjEge_GOBbfJFyuoU4u0SzjGQ'

# token API Wit.ai Anda
WIT_AI_TOKEN = 'ONW4F5XP2UOUNYGV7Q35PWV4ULY5PZGX'

# Path ke ffmpeg
FFMPEG_PATH = 'C:\\FFmpeg\\ffmpeg.exe'


# Fungsi untuk menangani pesan teks dari pengguna
def handle_text_message(update: Update, context: CallbackContext):
    message_text = update.message.text
    wit_url = f'https://api.wit.ai/message?v=20220101&q={message_text}'
    headers = {'Authorization': f'Bearer {WIT_AI_TOKEN}'}
    response = requests.get(wit_url, headers=headers)
    wit_data = response.json()

    # Lakukan sesuatu dengan hasil dari Wit.ai
    # Misalnya, dapatkan intent atau entity tertentu
    intent = wit_data['intents'][0]['name'] if wit_data['intents'] else None
    entities = wit_data['entities']

    if entities:
        # Konversikan entitas ke kamus dengan nilainya untuk akses yang lebih mudah
        entities = {key: value[0]['value'] for key, value in entities.items()}

    # Tentukan respon bot berdasarkan hasil Wit.ai
    response_text = generate_response(intent, entities)
    # Kirim respon ke pengguna
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=response_text)
    
    # Print respons JSON dan chat id pengguna telegram ke terminal Visual Studio Code
    print(f"ID_Pengguna : {chat_id}")
    print(wit_data)

    
# Fungsi untuk mengonversi audio menjadi teks menggunakan SpeechRecognition
def convert_audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  # Merekam audio dari file
    try:
        # Gunakan recognizer untuk mengonversi audio menjadi teks
        audio_text = recognizer.recognize_google(audio_data, language="id-ID")  # Ubah ke bahasa Indonesia jika diperlukan
        return audio_text
    except sr.UnknownValueError:
        return "Maaf, tidak dapat mengenali suara."
    except sr.RequestError:
        return "Maaf, terjadi masalah dengan layanan pengenalan suara."


# Fungsi untuk menangani pesan suara dari pengguna
def handle_voice(update: Update, context: CallbackContext) -> None:
    voice_file = update.message.voice.get_file()
    voice_file_path = 'voice_message.ogg'
    voice_file.download(voice_file_path)

    # Konversi file suara ke format WAV untuk digunakan oleh SpeechRecognition
    wav_file_path = 'voice_message.wav'
    subprocess.run([FFMPEG_PATH, '-i', voice_file_path, wav_file_path], check=True)

    audio_text = convert_audio_to_text(wav_file_path)

    # Kirim teks hasil konversi ke chat Telegram
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=f"[Input Suara] : {audio_text}")

    wit_url = f'https://api.wit.ai/message?v=20220101&q={audio_text}'
    headers = {'Authorization': f'Bearer {WIT_AI_TOKEN}'}
    response = requests.get(wit_url, headers=headers)
    wit_data = response.json()

    # Misalnya, dapatkan intent atau entity tertentu
    intent = wit_data['intents'][0]['name'] if wit_data['intents'] else None
    entities = wit_data['entities']

    if entities:
        # Konversikan entitas ke kamus dengan nilainya untuk akses yang lebih mudah
        entities = {key: value[0]['value'] for key, value in entities.items()}

    # Tentukan respon bot berdasarkan hasil Wit.ai
    response_text = generate_response(intent, entities)
    
    # Kirim respon ke pengguna
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=response_text)
    
    # Print respons JSON dan chat id pengguna telegram ke terminal Visual Studio Code
    print(f"ID_Pengguna : {chat_id}")
    print(wit_data)
    
    # Pastikan file tidak digunakan sebelum mencoba menghapusnya
    try:
        os.remove(voice_file_path)
    except PermissionError as e:
        print(f"Error removing {voice_file_path}: {e}")

    try:
        os.remove(wav_file_path)
    except PermissionError as e:
        print(f"Error removing {wav_file_path}: {e}")


# Fungsi untuk menangani perintah /start dari pengguna
def start_command(update: Update, context: CallbackContext):
    welcome_message = "Selamat datang! Saya adalah bot Informasi Akademik Fakultas Vokasi. Anda bisa bertanya tentang KKN, magang, pengajuan UKT, dan tugas akhir. Silakan ketik pertanyaan Anda."
    context.bot.send_message(chat_id=update.message.chat_id, text=welcome_message)


# Fungsi untuk menangani pesan dari pengguna dan menghasilkan respon
def generate_response(intent, entities):    
    response_text = "Maaf, saya tidak mengerti permintaan Anda"
    print(f"Intent: {intent}")
    print(f"Entities: {entities}")
    
    # Logika untuk menghasilkan respon berdasarkan intent dan entities dari Wit.ai
    if intent == 'intents_list_informasi_bot':
        response_text = """
Berikut adalah informasi yang bisa anda akses di dalam bot ini :
• KKN (Kuliah Kerja Nyata)
• Magang
• Pengajuan UKT
• TA (Tugas Akhir)
    """
    elif intent == 'intents_informasi_kkn':
        response_text = """
Berikut adalah informasi KKN :
• Tema KKN
• Konversi KKN
• Syarat Konversi KKN
• Pendaftaran KKN
• KKN Tematik Reguler
    """
    elif intent == 'intents_tema_kkn':
        if 'entity_tema_kkn' in entities:
            jenis_tema = entities['entity_tema_kkn'][0]['value']
            if jenis_tema in ['Proyek Studi Independen', 'Proyek Kemanusiaan', 'Kewirausahaan', 'Proyek Desa', 'Asisten Mengajar']:
                response_text = f"Anda memilih tema KKN: {jenis_tema}"
            else:
                response_text = "Maaf, tema KKN yang Anda pilih tidak valid."
        else:
            response_text = """
Berikut adalah tema KKN:
- Asisten Mengajar
- Proyek Desa
- Kewirausahaan
- Proyek Kemanusiaan
- Proyek Studi Independen 
- Proyek Sekolah     
        """
    elif intent == 'intents_konversi_kkn':
        if 'entity_konversi_kkn' in entities:
            konversi = entities['entity_konversi_kkn'][0]['value']
            if konversi in ['Kampus Mengajar (KM)', 'Program Surabaya Mengajar (PSM)']:
                response_text = f"Anda memilih Konversi KKN: {konversi}"
            else:
                response_text = "Maaf, konversi KKN yang Anda pilih tidak valid."
        else:
            response_text = """
Berikut adalah konversi KKN:
- Asisten Mengajar
    • Kampus Mengajar (KM)
    • Program Surabaya Mengajar (PSM)
- Proyek Desa
    • KKN Kebangsaan
- Kewirausahaan
    • Wirausaha Merdeka
    • UMKM Merdeka
    • Program Mahasiswa Wirausaha
      (PMW)
- Proyek Kemanusiaan Tanggap 
  Bencana
- Proyek/Studi Independen
    • SIB (Studi Independen Bersertifikat)
    • Internasional
    • Prestasi
    • PPK Ormawa
            """
    elif intent == 'intents_syarat_konversi_kkn':
            response_text = """
Berikut ini syarat konversi KKN :
•	Kegiatan Kementrian (KM, SIB, WM, UMKM Merdeka, KKN 
    Kebangsaan, PPK Ormawa)
•	Kegiatan Kerjasama (Program Surabaya Mengajar)
•	Kegiatan Di Bawah Penyelenggaraan Prodi
•	Kegiatan Di Bawah Kegiatan Dosen (PKM Dosen, DLL
•	Kegiatan Pada Semester Pemrograman KKN
•	Temukan KKN Mandiri Ke Perusahaan >> Magang
        """
    elif intent == 'intents_pendaftaran_kkn':
            response_text = """
Pendaftaran KKN dilakukan melalui :
• Melisa
• Sim KKN
• Pilih Tema
• Pilih Kelompok Sesuai Tema Dan Kegiatan 

Misalnya :
- Kampus Mengajar (AM)
- KKN Kebangsaan (Proyek Desa)
- Kewirausahaa_Wirausaha Merdeka
- Studi Independen_PPK Orma

NB: Tema yang sudah dipilih tidak dapat diubah 
kecuali diajukan tertulis.
        """
    elif intent == 'intents_kkn_tematik_reguler':
            response_text = """
KKN Tematik Reguler:
• Terdapat 5 Tema Kegiatan
• Tempat Kegiatan Kabupaten Magetan
• Tema Kegiatan 4 Bulan (20 SKS)
• Kegiatan Dibawah Dinas Terkait (UPD)
• Kegiatan Oleh Seksi KKN
• Pembukaan Di Desa Masing-Masing/Kecamatan
        """
    elif intent == 'intents_pengajuan_ukt':
            response_text = """
Berikut adalah informasi Pengajuan UKT :
• Pembebasan Biaya UKT
• Penurunan UKT 50%
    """
    elif intent == 'intents_pembebasan_biaya_ukt':
            response_text = """
Pembebasan UKT diberikan kepada mahasiswa yang telah menyelesaikan Seluruh Pembelajaran pada semester Gasal namun belum lulus dan tinggal mengurus Surat Penetapan Kelulusan (SPK):

• Persyaratan
-	Mahasiswa yang sudah tidak mem-
    program mata kuliah dan tinggal 
    mengurus SPK
-	Nilai Skripsi sudah masuk di transkip 
    Nilai
-	Minimal lulus 144 SKS
-	Upload Buku Rekening BTN yang aktif

• Dokument
-	Transkip sudah ada nilai skripsi
-	BA Ujian Skripsi/Lembar Pengesahan 
    Skripsi yang sudah ditanda tangani
"""
    elif intent == 'intents_penurunan_ukt':
            response_text = """
Penurunan UKT 50% diberikan kepada mahasiswa pada mhasiswa semester 9 dan seterusnya yang hanya memprogram Skripsi atau memprogram < 6 SKS:

• Persyaratan
-	Sudah menempuh minimal 138 SKS LULUS
-	Diketahui dan disetujui oleh DPA
-	Upload Buku Rekening BTN yang Aktif

• Dokument
-	Transkip
-	Surat Persetujuan dari DPA
    """
    elif intent == 'intents_tugas_akhir':
            response_text = """
Berikut adalah informasi Tugas Akhir:
• Persyaratan Pendaftaran Tugas Akhir
• Alur Pendaftaran Seminar Hasil Tugas Akhir
• Persyaratan Ujian Tugas Akhir
        """
    elif intent == 'intents_persyaratan':
            response_text = """
Syarat Mengikuti Tugas Akhir :

Persyaratan Akademik Pemrograman Tugas Akhir
1)	Telah mengumpulkan satuan kredit semester sekurang-kurangnya 150 SKS (dibuktikan dengan KHS);
2)	Telah lulus mata kuliah Metodologi Penelitian dengan nilai minimal C;
3)	Memiliki IPK minimal 3,00;

Persyaratan Administrator Pemrograman Tugas Akhir
1)	Tercatat sebagai mahasiswa aktif Unesa;
2)	Memprogram mata kuliah tugas akhir.
3)	Berkas pengajuan proposal/halaman persetujuan judul tugas akhir yang sudah disetujui oleh pembimbing (Lampiran 7)
4)	Lembar revisi setelah pelaksanaan seminar proposal yang sudah disetujui oleh pembimbing dan penguji/berkas rangkuman hasil penilaian judul (Lampiran 9)
        """
    elif intent == 'intents_alur_pendaftaran_seminar_hasil_tugas_akhir':
            response_text = """
Berikut Adalah Alur Pendaftaran Seminar Hasil Tugas Akhir :

-	Melihat jadwal yang tersedia di Google Calender dengan menggunakan akun UNESA.

-	Mahasiwa menghubungi dosen penguji dan pembimbing untuk pelaksanaan seminar proposal/seminar hasil tugas akhir.

-	Tetap dengan akun gmail UNESA, mengisi form pendaftaran sidang akhir dengan data yang diperlukan:

1)	Nama Mahasiswa.
2)	NIM Mahasiswa.
3)	Tanggal seminar hasil/sidang akhir.
4)	Jam seminar hasil/sidang akhir.
5)	Kesepakatan penguji dan pembina untuk seminar hasil/sidang akhir diadakan secara luring/daring.
6)	Laporan akhir yang sudah ditandatangani halaman persetujuannya oleh dosen pembimbing.
7)	Nama lengkap dan gelar dosen penguji 1.
8)	Nama lengkap dan gelar dosen penguji 2.
9)	Nama lengkap dan gelar dosen pembimbing.
10)	Bukti tangkapan layar (PNG/PDF) bahwa telah mengunggah laporan akhir di SIMONTASI
11)	Laporan Akhir (PDF) yang sudah ditandatangani lembar persetujuannya oleh dosen pembimbing.
    
-	Konfirmasi pengisian data ke google calendar kepada koordinator tugas akhir.

-	Koordinator tugas akhir akan mengisikan jadwal seminar hasil mahasiswa ke google calendar.

-	Koordinator tugas akhir akan mengkonfirmasikan jadwal seminar ke koordinator prodi.

-	Koordinator prodi akan membuat undangan seminar tugas hasil di SIMONTASI.

-	Mahasiswa mengunduh undangan seminar tugas akhir dari SIMONTASI (Mahasiswa dilarang membuat undangan seminar tugas akhir sendiri).

-	Mahasiswa menghubungi TU prodi untuk mendapatkan nomor surat undangan dan tanda tangan koordinator prodi.

-	Tigas hari sebelum pelaksanaan mahasiswa wajib memberikan berkas-berkas ujian seminar hasil sidang tugas akhir kepada para penguji.

1)	Laporan tugas akhir
2)	Lembar persetujuan dari pembimbing 
    untuk melaksanakan seminar hasil 
    sidang tugas akhir
3)	Lembar penilaian tugas akhir
4)	Lembar revisi tugas akhir
5)	Berita acara tugas akhir
    
-	Melaksanakan seminar hasil sidang tugas akhir sesuai dengan jadwal yang tertera di undangan.

-	Jika para penguji atau pembimbing tidak dapat hadir pada hari H maka akan dilakukan penjadwalan kembali sesuai kesepakatan antara mahasiswa, pembimbing dan penguji.
        """
    elif intent == 'intents_persyaratan_ujian_tugas_akhir':
            response_text = """
Persyaratan Ujian Tugas Akhir:
-	Tugas akhir yang akan diajukan dalam ujian harus sudah mendapat persetujuan dari dosen pembimbing.

-	Mahasiswa mendaftarkan diri ke jurusan/prodi/koordinator (biro) tugas akhir di jurusan/prodi masing-masing dengan membawa :

1)	KRS sebagai bukti pemrograman tugas akhir,
2)	Draf naskah tugas akhir, rangkap tiga, yang diserahkan kepada jurusan/program studi masing-masing selambat-lambatnya satu minggu sebelum periode/jangka waktu pelaksanaan ujian.
3)	Menyerahkan fotokopi sertifikat TEP/ TOEFL ITP dengan skor minimal 425 yang dilegalisasi oleh Pusat Bahasa Unesa.
4)	Beberapa persyaratan khusus dapat dirumuskan oleh prodi.
    """    
    elif intent == 'intents_magang':
            response_text = """
Berikut adalah informasi Magang:
• MSIB (Magang dan Studi Independen 
  Bersertifikat)
• Magang Reguler
"""
    elif intent == 'intents_magang_msib':
            response_text = """
Program persiapan karier yang komprehensif dan memberikan kesempatan bagi Mahasiswa untuk belajar di luar program studi dengan jaminan konversi SKS yang diakui perguruan tinggi.
        
Kenapa harus MSIB :
1)	Tingkat keberangkatan & kepulangan 
    gratis
2)	Golden tiket (bisa direkrut oleh 
    perusahaan yg bersangkutan)
3)	Koneksi pertemanan
4)	Pengalaman
5)	Konversi 20 SKS
6)	BBH (bantuan biaya hidup)

Rahasia lolos dalam Magang MSIB :
1)	Cari informasi sebanyak-banyaknya, perbaiki cv & portofolio, mengikuti alur pendaftaran dari awal hingga offering
2)	Lengkapi profil & dokumen, pilih perusahaan yang sesuai dgn jurusan/skill, pilih 10-15 perusahaan/posisi yang kalian prioritaskan, dan jgn mndftr diakhir periode.
"""
    elif intent == 'intents_magang_reguler':
            response_text = """
Merupakan alternatif jika tidak diterima oleh MSIB Dilaksanakan selama 6 bulan Diusahakan sesuai bidang.

-	Dokument 

1)	Proposal magang
2)	Surat peangantar izin magang
3)	Surat izin magang
4)	PKS (Perjanjian kerjasama) jika 
    perusahaan belum bekerja sama 
    dengan unesa
5)	AI (pelaksanaan kesepakatan)
    
# Link Tamplate Document "https://drive.google.com/drive/u/0/folders/1NbZMOzJRP8x5uyM_Hw1Wftc4nuIxLFon"
        """
    return response_text
  
# Fungsi untuk mengatur ConversationHandler dan Menjalakan Bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Tambahkan handler untuk perintah /start
    dp.add_handler(CommandHandler('start', start_command))

    # Menangani pesan teks dari pengguna
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_message))
    
    # Menangani pesan suara dari pengguna
    dp.add_handler(MessageHandler(Filters.voice, handle_voice))

    # Jalankan bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

