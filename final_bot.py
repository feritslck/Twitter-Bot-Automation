import tweepy
import os

# 1. Kimlik Bilgilerini GitHub Secrets'tan Alıyoruz
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

def run_bot():
    try:
        # 2. Twitter v2 Bağlantısını Kur
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_KEY_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

        # 3. Metin Dosyasını Oku ve Boş Satırları Filtrele
        if not os.path.exists("meal.txt"):
            print("HATA: meal.txt dosyası bulunamadı!")
            return

        with open("meal.txt", "r", encoding="utf-8") as f:
            # Sadece içeriği olan satırları al, kenar boşluklarını temizle
            ayetler = [line.strip() for line in f.readlines() if line.strip()]

        if not ayetler:
            print("HATA: meal.txt dosyasının içi boş!")
            return

        # 4. Mevcut İndeksi Oku
        if os.path.exists("index.txt"):
            with open("index.txt", "r") as f:
                content = f.read().strip()
                index = int(content) if content else 0
        else:
            index = 0

        # Eğer indeks liste boyutunu aşmışsa başa dön
        if index >= len(ayetler):
            index = 0

        # 5. Tweet Atılacak Metni Seç
        ayet_metni = ayetler[index]
        
        # Karakter sınırı kontrolü (Twitter 280 karakter sınırı)
        if len(ayet_metni) > 280:
            print(f"UYARI: {index}. satırdaki ayet çok uzun ({len(ayet_metni)} karakter). Kesiliyor...")
            ayet_metni = ayet_metni[:277] + "..."

        # 6. Tweeti Gönder
        print(f"Sıradaki ayet (İndeks: {index}) gönderiliyor...")
        response = client.create_tweet(text=ayet_metni)
        
        # 7. Bir Sonraki Çalışma İçin İndeksi Güncelle
        with open
