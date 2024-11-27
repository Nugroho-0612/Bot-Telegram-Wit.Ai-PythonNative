import os
import requests
import speech_recognition as sr
# from pydub import AudioSegment
from telegram import Update
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackContext
#import telegram.ext.filters as filters
import subprocess

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
# Ganti dengan token bot Telegram Anda
TOKEN = '6751900243:AAHP4XVpxSzjEge_GOBbfJFyuoU4u0SzjGQ'
# Ganti dengan token API Wit.ai Anda
WIT_AI_TOKEN = 'ONW4F5XP2UOUNYGV7Q35PWV4ULY5PZGX'
#'4S2NRESVIL4U2QMBE7FYBZISSXVDJUU5'
# Path ke ffmpeg
FFMPEG_PATH = os.getenv('FFMPEG_PATH', 'C:\FFmpeg')

# Daftar state untuk ConversationHandler
VOICE_MESSAGE = 0

# # Set path FFmpeg
# AudioSegment.ffmpeg = r"D:\Bot_Telegram\ffmpeg\ffmpeg.exe"

# Fungsi untuk menangani pesan teks dari pengguna
def handle_text_message(update: Update, context: CallbackContext):
    message_text = update.message.text
    wit_url = f'https://api.wit.ai/message?v=20220101&q={message_text}'
    headers = {'Authorization': f'Bearer {WIT_AI_TOKEN}'}
    response = requests.get(wit_url, headers=headers)
    wit_data = response.json()

    # Print respons JSON ke terminal Visual Studio Code
    # print(wit_data)

    # Lakukan sesuatu dengan hasil dari Wit.ai
    # Misalnya, dapatkan intent atau entity tertentu
    intent = wit_data['intents'][0]['name'] if wit_data['intents'] else None
    entities = wit_data['entities']
    print(wit_data)

    # data = intent,entities
    # print(data)
    if entities:
        # Convert entities to a dictionary with their values for easier access
        entities = {key: value[0]['value'] for key, value in entities.items()}

    # Tentukan respon bot berdasarkan hasil Wit.ai
    response_text = generate_response(intent, entities)
    # Kirim respon ke pengguna
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=response_text)
    
# Fungsi untuk menangani pesan dari pengguna
def generate_response(intent, entities):
    
    # kkn = """
    # Berikut adalah informasi kkn
    # 1. Tema KKN
    # 2. Konversi KKN
    # 3. Syarat Konversi KKN
    # 4. Pendaftaran KKN
    # 5. KKN Tematik Reguler
    # """
    # print(kkn)
    response_text = "Maaf, saya tidak mengerti permintaan Anda"
    print(f"Intent: {intent}")
    print(f"Entities: {entities}")
    # Logika untuk menghasilkan respon berdasarkan intent dan entities dari Wit.ai
    # Gantilah dengan logika khusus Anda
    if intent == 'intents_list_informasi_bot':
            response_text = """
Berikut adalah informasi yang bisa anda akses di dalam bot ini :
1. KKN
2. Magang
3. Pengajuan UKT
4. Tugas Akhir
        """
    elif intent == 'intents_informasi_kkn':
            response_text = """
Berikut adalah informasi KKN :
1. Tema KKN
2. Konversi KKN
3. Syarat Konversi KKN
4. Pendaftaran KKN
5. KKN Tematik Reguler
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
    • Program Mahasiswa Wirausaha (PMW)
- Proyek Kemanusiaan Tanggap Bencana
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
1. Pembebasan Biaya UKT
2. Penurunan UKT 50%
        """
    elif intent == 'intents_pembebasan_biaya_ukt':
            response_text = """
Pembebasan UKT diberikan kepada mahasiswa yang telah menyelesaikan Seluruh Pembelajaran pada semester Gasal namun belum lulus dan tinggal mengurus Surat Penetapan Kelulusan (SPK):
• Persyaratan
-	Mahasiswa yang sudah tidak mem-program mata kuliah dan tinggal mengurus SPK
-	Nilai Skripsi sudah masuk di transkip 
    Nilai
-	Minimal lulus 144 SKS
-	Upload Buku Rekening BTN yang aktif
• Dokument
-	Transkip sudah ada nilai skripsi
-	BA Ujian Skripsi/Lembar Pengesahan Skripsi yang sudah ditanda tangani
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
1. Persyaratan
2. Alur Pendaftaran Seminar Hasil Tugas Akhir
3. Persyaratan Ujian Tugas Akhir
        """
    elif intent == 'intents_persyaratan':
            response_text = """
Berikut adalah Persyaratan Tugas Akhir:
1.	Mengumpulkan 5 Bab yang sudah di acc dosen pembimbing
2.	Buku Bimbingan di tandatangan dosen pembimbing 10 kali pertemuan
3.	Artikel
4.	Bebas Pinjaman
5.	Terbit Bukti Jurnal
6.	Pendadaran
        """
    elif intent == 'intents_alur_pendaftaran_seminar_hasil_ta':
            response_text = """
Berikut adalah Alur Pendaftaran Seminar Hasil Tugas Akhir:
1.	Alur Pendaftaran Seminar Hasil
2.	Mengisi Google Form
3.	Daftar Ke Sekertaris Prodi
4.	Verifikasi Prodi
5.	Pembayaran
6.	Jadwal Seminar 
        """
    elif intent == 'intents_persyaratan_ujian_ta':
            response_text = """
Berikut adalah Persyaratan Ujian Tugas Akhir:
1.	Mengumpulkan revisi seminar hasil
2.	Buku bimbingan di tandatangan dosen pembimbing 10 kali pertemuan
3.	Artikel
4.	Bebas Pinjaman
5.	Terbit Bukti Jurnal
6.	Pendadaran
        """

    # Contoh respon sederhana
    return response_text

# Fungsi untuk menangani pesan suara dari pengguna
def handle_voice_message(update: Update, context: CallbackContext):
    file = update.message.voice.get_file()
    file_path = f"voice_message_{update.message.message_id}.ogg"
    file.download(file_path)

    # Konversi file OGG ke WAV menggunakan FFmpeg
    wav_path = f"voice_message_{update.message.message_id}.wav"
    convert_ogg_to_wav(file_path, wav_path)

    # Menggunakan SpeechRecognition untuk mengenali pesan suara
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
    try:
        recognized_text = recognizer.recognize_google(audio, language='id-ID')
        wit_url = f'https://api.wit.ai/message?v=20220101&q={recognized_text}'
        headers = {'Authorization': f'Bearer {WIT_AI_TOKEN}'}
        response = requests.get(wit_url, headers=headers)
        wit_data = response.json()

        # Lakukan sesuatu dengan hasil dari Wit.ai
        intent = wit_data['intents'][0]['name'] if wit_data['intents'] else None
        entities = wit_data['entities']
        print(wit_data)
        
        if entities:
            # Convert entities to a dictionary with their values for easier access
            entities = {key: value[0]['value'] for key, value in entities.items()}

        # Tentukan respon bot berdasarkan hasil Wit.ai
        response_text = generate_response(intent, entities)
        # Kirim respon ke pengguna
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=response_text)
    except sr.UnknownValueError:
        context.bot.send_message(chat_id=update.message.chat_id, text="Maaf, saya tidak dapat memahami pesan suara Anda.")
    except sr.RequestError as e:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Terjadi kesalahan pada layanan pengenalan suara: {e}")

def convert_ogg_to_wav(ogg_path, wav_path):
    command = [FFMPEG_PATH, '-i', ogg_path, wav_path]
    subprocess.run(command, check=True)

# Fungsi untuk menangani perintah /start
def start_command(update: Update, context: CallbackContext):
    welcome_message = "Selamat datang! Saya adalah bot informasi akademik. Anda bisa bertanya tentang KKN, magang, pengajuan UKT, dan tugas akhir. Silakan ketik pertanyaan Anda."
    context.bot.send_message(chat_id=update.message.chat_id, text=welcome_message)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Tambahkan handler untuk perintah /start
    dp.add_handler(CommandHandler('start', start_command))

    # Handler untuk pesan teks
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_message))

    # Handler untuk pesan suara
    dp.add_handler(MessageHandler(Filters.voice, handle_voice_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
