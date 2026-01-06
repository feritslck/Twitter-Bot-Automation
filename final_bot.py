import tweepy
import os

# Anahtarlar
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

def run_bot():
    try:
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_KEY_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
        
        # TEST TWEETİ (İndexle uğraşmadan direkt deniyoruz)
        test_mesaj = "Sistem kontrolü. Test No: 1"
        print(f"Deneme yapılıyor: {test_mesaj}")
        
        response = client.create_tweet(text=test_mesaj)
        print(f"BAŞARILI! Tweet ID: {response.data['id']}")

    except Exception as e:
        print("\n--- TWITTER'IN GÖNDERDİĞİ GERÇEK HATA ---")
        print(e)
        print("----------------------------------------\n")

if __name__ == "__main__":
    run_bot()
