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

        # 2. Ayeti Oku ve Sırayı Belirle
        with open("meal.txt", "r", encoding="utf-8") as f:
            ayetler = f.readlines()

        if os.path.exists("index.txt"):
            with open("index.txt", "r") as f:
                index = int(f.read().strip())
        else:
            index = 0

        # Eğer dosya bittiyse başa dön
        if index >= len(ayetler):
            index = 0

        ayet_metni = ayetler[index].strip()

        # 3. Tweet At
        if ayet_metni:
            print(f"Sıradaki ayet (No: {index}) gönderiliyor...")
            client.create_tweet(text=ayet_metni)
            
            # 4. İndeksi Güncelle
            with open("index.txt", "w") as f:
                f.write(str(index + 1))
            
            print("BAŞARILI: Ayet paylaşıldı!")
        else:
            print("HATA: Boş satıra denk gelindi.")

    except Exception as e:
        print(f"HATA OLUŞTU: {e}")

if __name__ == "__main__":
    run_bot()
