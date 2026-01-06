import tweepy
import os

# Anahtarlar
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

def run_bot():
    try:
        # v1.1 AUTH (Yetkilendirme için v1.1 kullanıp v2 üzerinden tweet atacağız)
        auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api_v1 = tweepy.API(auth)
        
        # v2 Client
        client = tweepy.Client(
            consumer_key=API_KEY, consumer_secret=API_KEY_SECRET,
            access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET
        )

        print("Bağlantı deneniyor...")
        # Bu yöntem bazen 403 engelini aşar
        client.create_tweet(text="Sistem doğrulama testi.")
        print("BAŞARILI: Tweet gönderildi!")

    except Exception as e:
        print(f"HATA DETAYI: {e}")

if __name__ == "__main__":
    run_bot()
