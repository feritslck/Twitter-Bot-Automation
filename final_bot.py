import tweepy
import os

# GitHub Secrets
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

def split_text(text, limit=280):
    """Metni kelimeleri bölmeden belirtilen sınıra göre parçalara ayırır."""
    words = text.split()
    chunks = []
    current_chunk = ""

    for word in words:
        # Kelimeyi eklediğimizde sınırı aşıyor mu kontrol et (+1 boşluk için)
        if len(current_chunk) + len(word) + 1 <= limit:
            current_chunk += (word + " ")
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def run_bot():
    try:
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_KEY_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

        if not os.path.exists("meal.txt"):
            print("HATA: meal.txt bulunamadı.")
            return

        with open("meal.txt", "r", encoding="utf-8") as f:
            ayetler = [line.strip() for line in f.readlines() if line.strip()]

        # İndeks oku
        if os.path.exists("index.txt"):
            with open("index.txt", "r") as f:
                content = f.read().strip()
                index = int(content) if content else 0
        else:
            index = 0

        if index >= len(ayetler):
            index = 0

        tam_metin = ayetler[index]
        
        # 1. Metni parçalara ayır (Flood hazırlığı)
        parcalar = split_text(tam_metin)

        # 2. İlk Tweeti At
        print(f"Ana tweet gönderiliyor (İndeks: {index})...")
        son_tweet = client.create_tweet(text=parcalar[0])
        ana_tweet_id = son_tweet.data['id']

        # 3. Eğer kalan parça varsa zincir yap (Reply olarak ekle)
        for i in range(1, len(parcalar)):
            print(f"Zincir parçası {i} ekleniyor...")
            son_tweet = client.create_tweet(
                text=parcalar[i],
                in_reply_to_tweet_id=ana_tweet_id
            )

        # 4. İndeksi Güncelle
        with open("index.txt", "w") as f:
            f.write(str(index + 1))
        
        print(f"BAŞARILI: Toplam {len(parcalar)} tweetlik zincir paylaşıldı!")

    except Exception as e:
        print(f"BEKLENMEDİK HATA: {e}")

if __name__ == "__main__":
    run_bot()
