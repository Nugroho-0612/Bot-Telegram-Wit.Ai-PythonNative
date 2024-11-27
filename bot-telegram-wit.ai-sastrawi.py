# Contoh penggunaan library sastrawi
# import StemmerFactory class
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()
# stemming process
sentence = 'Perekonomian Indonesia sedang dalam pertumbuhan yang membanggakan'
output   = stemmer.stem(sentence)
print(output)
# ekonomi indonesia sedang dalam tumbuh yang bangga
print(stemmer.stem('Mereka meniru-nirukannya'))
# mereka tiru

# Penerapan library steaming sastrawi di wit.ai di jalankan di bot telegram
import os
import requests
import speech_recognition as sr
from telegram import Update
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackContext
import subprocess
import logging
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

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

# Buat stemmer dari Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()
print(stemmer)

# Fungsi untuk menangani pesan teks dari pengguna
def handle_text_message(update: Update, context: CallbackContext):
    message_text = update.message.text

    # Lakukan stemming pada teks yang diterima
    stemmed_text = stemmer.stem(message_text)
    print(stemmed_text)
    wit_url = f'https://api.wit.ai/message?v=20220101&q={stemmed_text}'
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

    # Lakukan stemming pada teks yang dihasilkan dari audio
    stemmed_audio_text = stemmer.stem(audio_text)

    wit_url = f'https://api.wit.ai/message?v=20220101&q={stemmed_audio_text}'
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

