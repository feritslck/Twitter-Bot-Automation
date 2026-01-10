import tweepy
import os

# 1. Kimlik Bilgileri (GitHub Secrets)
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

def run_bot():
    try:
        # 2. Twitter v2 Bağlantısı
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_KEY_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

        # 3. Dosya Kontrolleri
        if not os.path.exists("meal.txt"):
            print("HATA: meal.txt dosyası bulunamadı!")
            return

        # 4. Ayetleri Oku (Boşlukları Temizle)
        with open("meal.txt", "r", encoding="utf-8") as f:
            ayetler = [line.strip() for line in f.readlines() if line.strip()]

        if not ayetler:
            print("HATA: meal.txt dosyası boş!")
            return

        # 5. İndeksi Oku
        if os.path.exists("index.txt"):
            with open("index.txt", "r") as f:
                icerik = f.read().strip()
                index = int(icerik) if icerik else 0
        else:
            index = 0

        # Liste sonuna gelindiyse başa dön
        if index >= len(ayetler):
            index = 0

        # 6. Tweet Metnini Hazırla
        ayet_metni = ayetler[index]
        
        # Twitter karakter sınırı (280) kontrolü
        if len(ayet_metni) > 280:
            print(f"UYARI: Ayet çok uzun, kısaltılıyor...")
            ayet_metni = ayet_metni[:277] + "..."

        # 7. Tweet At
        print(f"Gönderiliyor (Sıra: {index}): {ayet_metni[:30]}...")
        client.create_tweet(text=ayet_metni)
        
        # 8. İndeksi Bir Artır ve Kaydet
        with open("index.txt", "w") as f:
            f.write(str(index + 1))
        
        print("BAŞARILI: Tweet gönderildi!")

    except Exception as e:
        print(f"BİR HATA OLUŞTU: {e}")

if __name__ == "__main__":
    run_bot()
