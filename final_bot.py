import tweepy
import os
import sys

# --- 1. GitHub Secrets'tan Anahtarları Çekme ---
# ÖNEMLİ: Bu isimler GitHub Settings > Secrets kısmındaki isimlerle aynı olmalıdır.
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# --- 2. Dosya Tanımlamaları ---
# GitHub Actions dosyaları projenin ana klasöründe arar.
INDEX_FILE = "index.txt"
VERSE_FILE = "meal.txt"

def connect_to_api():
    try:
        # Ücretsiz plan için en kararlı yöntem v2 Client kullanımıdır.
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_KEY_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
        print("Twitter API v2 Bağlantısı Hazır.")
        return client
    except Exception as e:
        print(f"HATA: API bağlantı hatası (401 mi?): {e}")
        return None

def run_bot():
    # 1. API'ye bağlan
    client = connect_to_api()
    if not client:
        return

    # 2. Ayetleri ve İndeksi Oku
    try:
        if not os.path.exists(INDEX_FILE):
            with open(INDEX_FILE, "w") as f: f.write("0")
        
        with open(INDEX_FILE, "r") as f:
            index = int(f.read().strip())
        
        with open(VERSE_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        
        if not lines:
            print("HATA: meal.txt dosyası boş!")
            return

        # İndeks dosya boyutunu aşarsa başa dön
        if index >= len(lines):
            index = 0
        
        ayet_metni = lines[index]

        # 3. Tweet At
        print(f"Sıradaki ayet (No: {index}) gönderiliyor...")
        client.create_tweet(text=ayet_metni)
        print(f"BAŞARILI: Tweet atıldı!")

        # 4. İndeksi Bir Sonraki İçin Güncelle
        with open(INDEX_FILE, "w") as f:
            f.write(str(index + 1))
            
    except Exception as e:
        print(f"HATA: Bir sorun oluştu: {e}")

if __name__ == "__main__":
    run_bot()
