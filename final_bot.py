import tweepy
import os

# GitHub Secrets'tan anahtarları çekiyoruz
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

def run_bot():
    try:
        # 1. Twitter'a Bağlan (v2)
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_KEY_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

        # ... (Önceki bağlantı kodları aynı kalacak)

        # 2. Ayeti Oku ve Temizle
        with open("meal.txt", "r", encoding="utf-8") as f:
            # Sadece içi dolu olan satırları listeye al
            ayetler = [line.strip() for line in f.readlines() if line.strip()]

        if os.path.exists("index.txt"):
            with open("index.txt", "r") as f:
                content = f.read().strip()
                index = int(content) if content else 0
        else:
            index = 0

        # Başa dönme kontrolü
        if index >= len(ayetler):
            index = 0

        ayet_metni = ayetler[index]

        # 3. Tweet At
        print(f"Sıradaki ayet (No: {index}) gönderiliyor...")
        client.create_tweet(text=ayet_metni)
        
        # 4. İndeksi Güncelle
        with open("index.txt", "w") as f:
            f.write(str(index + 1))
        
        print(f"BAŞARILI: '{ayet_metni[:30]}...' paylaşıldı!")
