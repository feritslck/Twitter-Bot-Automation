import tweepy
import os
import sys

# GitHub Secrets'tan anahtarları çekiyoruz
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

INDEX_FILE = "index.txt"
VERSE_FILE = "meal.txt"

def connect_to_api():
    try:
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_KEY_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
        return client
    except Exception as e:
        print(f"Bağlantı Hatası: {e}")
        return None

def get_sequential_verse():
    if not os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "w") as f: f.write("0")
    
    with open(INDEX_FILE, "r") as f:
        index = int(f.read().strip())
    
    with open(VERSE_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    if index >= len(lines): index = 0
    
    tweet_text = lines[index]
    
    # İndeksi bir artır ve kaydet
    with open(INDEX_FILE, "w") as f:
        f.write(str(index + 1))
        
    return tweet_text

def run_bot():
    client = connect_to_api()
    if client:
        tweet = get_sequential_verse()
        if tweet:
            try:
                client.create_tweet(text=tweet)
                print(f"Başarılı: {tweet[:30]}...")
            except Exception as e:
                print(f"Tweet Atılamadı: {e}")

if __name__ == "__main__":
    run_bot()
