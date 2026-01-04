import tweepy
import time
import os

# --- 1. API Bilgileri (Burayı Yeni Regenerate Edilenlerle Doldur) ---
API_KEY = "tkMd8lx8p9fpToycU3qzsrm7f"
API_KEY_SECRET = "TttXuIOp8bzu3M3jiDyZ8bUukendiei0btoVbrwEBoPIic5ytu"
ACCESS_TOKEN = "1999944941955608576-5bVrMCDobyRwGyyvKOPP1BN5xr7aJf"
ACCESS_TOKEN_SECRET = "2B0o3oRaxzz2Bv6hNFxTTeL2LOFIbGXSimovcLXD5htE8"

# --- 2. Dosya Yolları ---
# PythonAnywhere üzerinde çalıştığı için tam yol belirtmek en sağlıklısıdır.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEAL_FILE = os.path.join(BASE_DIR, 'meal.txt')
INDEX_FILE = os.path.join(BASE_DIR, 'index.txt')

# --- 3. Twitter API Bağlantısı (v2) ---
def connect_to_api():
    try:
        # Ücretsiz plan v2 Client kullanmalıdır
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_KEY_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
        print("Twitter API v2 Bağlantısı Başarılı.")
        return client
    except Exception as e:
        print(f"HATA: API bağlantısı kurulamadı: {e}")
        return None

# --- 4. Ayet Çekme Fonksiyonu ---
def get_sequential_verse():
    try:
        if not os.path.exists(INDEX_FILE):
            with open(INDEX_FILE, 'w') as f: f.write("0")
        
        with open(INDEX_FILE, 'r') as f:
            index = int(f.read().strip())
        
        with open(MEAL_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if index >= len(lines):
            print("Dosya bitti, başa dönülüyor.")
            index = 0
            
        tweet_text = lines[index].strip()
        
        # Eğer satır boşsa bir sonrakine geç
        if not tweet_text:
            print(f"Satır {index} boş, atlanıyor...")
            with open(INDEX_FILE, 'w') as f: f.write(str(index + 1))
            return get_sequential_verse()

        # Sırayı güncelle
        with open(INDEX_FILE, 'w') as f:
            f.write(str(index + 1))
            
        return tweet_text
    except Exception as e:
        print(f"Dosya okuma hatası: {e}")
        return None

# --- 5. Ana Çalıştırma Fonksiyonu ---
def sequential_ayet_twitle():
    print(f"\n[{time.strftime('%H:%M:%S')}] İşlem başlıyor...")
    client = connect_to_api()
    
    if client:
        ayet = get_sequential_verse()
        if ayet:
            try:
                # v2 Tweet Atma Metodu
                client.create_tweet(text=ayet)
                print(f"BAŞARILI: Tweet atıldı -> {ayet[:50]}...")
            except Exception as e:
                print(f"HATA: Tweet gönderilemedi (403 mü?): {e}")
                print("İPUCU: Developer Portal'dan 'Read and Write' iznini kontrol et!")

# --- 6. Botun Çalışma Döngüsü ---
if __name__ == "__main__":
    # İlk tweet'i hemen atar
    sequential_ayet_twitle()
    
    while True:
        # 1 saat (3600 saniye) bekle
        print("Bir sonraki saat bekleniyor...")
        time.sleep(3600)
        sequential_ayet_twitle()
