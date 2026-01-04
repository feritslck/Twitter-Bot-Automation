import tweepy
import time
import os
import sys

# --- 1. API Kimlik Bilgileri (TWITTER) ---
# ÖNEMLİ: Developer Portal'dan "Read and Write" iznini aldıktan sonra 
# Access Token'ları "Regenerate" edip buraya yapıştırdığından emin ol.
CONSUMER_KEY = "tkMd8lx8p9fpToycU3qzsrm7f"
CONSUMER_SECRET = "TttXuIOp8bzu3M3jiDyZ8bUukendiei0btoVbrwEBoPIic5ytu"
ACCESS_TOKEN = "1999944941955608576-5bVrMCDobyRwGyyvKOPP1BN5xr7aJf"
ACCESS_TOKEN_SECRET = "2B0o3oRaxzz2Bv6hNFxTTeL2LOFIbGXSimovcLXD5htE8"

# --- 2. İndeks ve Dosya Tanımlamaları ---
# PythonAnywhere için dosya yollarını tam yol olarak tanımlamak daha güvenlidir.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(BASE_DIR, "index.txt")
VERSE_FILE = os.path.join(BASE_DIR, "meal.txt")

def read_index():
    if not os.path.exists(INDEX_FILE):
        return 0
    try:
        with open(INDEX_FILE, 'r') as f:
            return int(f.read().strip())
    except:
        return 0

def write_index(index):
    try:
        with open(INDEX_FILE, 'w') as f:
            f.write(str(index))
    except Exception as e:
        print(f"HATA: İndeks dosyasına yazılırken sorun oluştu: {e}", flush=True)

# --- 3. Twitter API Bağlantısı (Tamamen v2) ---
def connect_to_api():
    try:
        # Ücretsiz planlar için sadece tweepy.Client yeterlidir.
        # verify_credentials (v1.1) ücretsiz planlarda 403 hatası verir, o yüzden kaldırıldı.
        client = tweepy.Client(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
        print("Twitter API v2 Bağlantısı Kuruldu.", flush=True)
        return client
    except Exception as e:
        print(f"HATA: Twitter API bağlantı hatası: {e}", flush=True)
        return None

# --- 4. Lokal TXT Dosyasından Sıradaki Ayeti Çekme ---
def get_sequential_verse(dosya_adi=VERSE_FILE):
    try:
        with open(dosya_adi, 'r', encoding='utf-8') as f:
            ayetler = [line.strip() for line in f if line.strip()] 
        
        if not ayetler:
            print(f"HATA: '{dosya_adi}' dosyası boş.", flush=True)
            return None
        
        current_index = read_index()
        total_verses = len(ayetler)
        
        if current_index >= total_verses or current_index < 0:
            current_index = 0
        
        sequential_ayet = ayetler[current_index]
        next_index = (current_index + 1) % total_verses
        write_index(next_index)
        
        # Twitter 280 karakter sınırı kontrolü
        if len(sequential_ayet) > 280:
            sequential_ayet = sequential_ayet[:277] + "..."
            
        print(f"BAŞARILI: Ayet çekildi (Sıra No: {current_index + 1}/{total_verses})", flush=True)
        return sequential_ayet
        
    except Exception as e:
        print(f"HATA: Dosya okuma sorunu: {e}", flush=True)
        return None

# --- 5. Twit Atma Fonksiyonu (v2) ---
def twit_at(api_client, twit_metni):
    try:
        # v2 tweet atma metodu
        api_client.create_tweet(text=twit_metni)
        print(f"BAŞARILI: Twit atıldı: {twit_metni[:50]}...", flush=True)
    except Exception as e:
        print(f"HATA: Twit atılamadı. Detay: {e}", flush=True)
        print("İPUCU: 403 alıyorsan Developer Portal'da 'Read and Write' iznini kontrol et.", flush=True)

# --- 6. Ana İşlev ---
def sequential_ayet_twitle():
    print(f"\n[{time.strftime('%H:%M:%S')}] İşlem başlatılıyor...", flush=True)
    api_client = connect_to_api()
    if api_client:
        ayet = get_sequential_verse()
        if ayet:
            twit_at(api_client, ayet)
        else:
            print("Ayet bulunamadı.", flush=True)

# --- 7. Botu Başlatma ve Döngü ---
if __name__ == "__main__":
    print("Bot başlatıldı. İlk twit hemen atılıyor...", flush=True)
    sequential_ayet_twitle()

    while True:
        print("Bekleniyor (1 saat)...", flush=True)
        sys.stdout.flush() # PythonAnywhere konsolunda yazıları anında görmek için
        time.sleep(3600)
        sequential_ayet_twitle()
