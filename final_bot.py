import tweepy
import time
import os
# random kütüphanesine artık gerek yok, sıralı ilerleyeceğiz.

# --- 1. API Kimlik Bilgileri (TWITTER) ---
CONSUMER_KEY = "39z5TI0sAh69M6kqHw4sUZhbi"
CONSUMER_SECRET = "AJ5mhmSYgMIhIT7Us7itCPGpOxkFGsH6qJleNQTbI2gbekJkDW"
ACCESS_TOKEN = "1999944941955608576-IeMBm0l0gIihagFyh6mnnQ2ERhkWeb"
ACCESS_TOKEN_SECRET = "gGLfqXtdsJKJboeFdOL5K6G6MhC2BDDKzWFXS7mnLE7yL"

# --- 2. İndeks ve Dosya Tanımlamaları ---
INDEX_FILE = "index.txt"
VERSE_FILE = "meal.txt"

# --- YARDIMCI İNDEKS FONKSİYONLARI ---
def read_index():
    """index.txt dosyasından son kalınan ayetin numarasını okur."""
    if not os.path.exists(INDEX_FILE):
        return 0
    try:
        with open(INDEX_FILE, 'r') as f:
            # Okunan değeri tamsayıya çevirir
            return int(f.read().strip())
    except:
        return 0

def write_index(index):
    """Sıradaki ayetin numarasını index.txt dosyasına yazar."""
    try:
        with open(INDEX_FILE, 'w') as f:
            f.write(str(index))
    except Exception as e:
        print(f"HATA: İndeks dosyasına yazılırken sorun oluştu: {e}")

# --- 3. Twitter API Bağlantısı Kurma Fonksiyonu (Değişmedi) ---
def connect_to_api():
    try:
        api_client = tweepy.Client(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api_v1 = tweepy.API(auth)
        api_v1.verify_credentials()
        
        print("Twitter API Bağlantısı Başarılı.")
        return api_client
    
    except Exception as e:
        print(f"HATA: Twitter API bağlantı hatası: {e}")
        return None

# --- 4. Lokal TXT Dosyasından Sıradaki Ayeti Çekme Fonksiyonu ---
def get_sequential_verse(dosya_adi=VERSE_FILE):
    """
    Yerel TXT dosyasını okur, sıradaki ayeti seçer ve indeksi bir sonraki ayete günceller.
    """
    try:
        # 1. Tüm ayetleri oku
        with open(dosya_adi, 'r', encoding='utf-8') as f:
            # Boş satırları atlayarak her satırı ayet olarak listeye ekle
            ayetler = [line.strip() for line in f if line.strip()] 
        
        if not ayetler:
            print(f"HATA: '{dosya_adi}' dosyası boş. Lütfen içeriği kontrol edin.")
            return None
        
        # 2. Güncel indeksi al ve geçerliliğini kontrol et
        current_index = read_index()
        total_verses = len(ayetler)
        
        # İndeks listeyi aştıysa başa dön
        if current_index >= total_verses or current_index < 0:
            current_index = 0
        
        # Ayeti al
        sequential_ayet = ayetler[current_index]
        
        # 3. Sonraki indeksi hesapla (Başa dönme dahil)
        next_index = (current_index + 1) % total_verses
        
        # 4. Yeni indeksi kaydet
        write_index(next_index)
        
        # Twit metnini 280 karakter limitine göre kesme
        if len(sequential_ayet) > 280:
            sequential_ayet = sequential_ayet[:277] + "..."
            
        print(f"BAŞARILI: Ayet çekildi (Sıra No: {current_index + 1}/{total_verses}): {sequential_ayet[:30]}...")
        return sequential_ayet
        
    except FileNotFoundError:
        print(f"KRİTİK HATA: '{dosya_adi}' dosyası bulunamadı! Lütfen kontrol edin.")
        return None
    except Exception as e:
        print(f"HATA: TXT dosya okuma sorunu: {e}")
        return None


# --- 5. Twit Atma Fonksiyonu (Değişmedi) ---
def twit_at(api_client, twit_metni):
    try:
        # Twit atma işlemi
        api_client.create_tweet(text=twit_metni)
        print(f"BAŞARILI: Twit atıldı: {twit_metni[:50]}...")
    except tweepy.TweepyException as e:
        print(f"HATA: Twit atılamadı (Tweepy Hatası): {e}")

# --- 6. Ana İşlevi Çağırma ve Kontrol ---
def sequential_ayet_twitle():
    api_client = connect_to_api()
    if api_client:
        ayet = get_sequential_verse() # Sıralı ayet çekme fonksiyonunu çağır
        
        if not ayet:
            print("Ayet metni çekilemediği için twit atılmadı.")
            return

        twit_at(api_client, ayet)
        # Yeni değeri hesapla
yeni_index = mevcut_index + 1

# index.txt dosyasını yeni değerle güncelle ve kaydet
with open("index.txt", "w") as f:
    f.write(str(yeni_index))

print(f"BAŞARILI: Index değeri {mevcut_index} -> {yeni_index} olarak güncellendi.")

# --- 7. Botu Başlatma ve Zamanlama ---

print("Hemen bağlantı testi yapılıyor...")
sequential_ayet_twitle()

print("Bot çalışmaya başladı. Twitler saat başı sırayla atılacaktır.")
print("Çıkmak için Ctrl+C'ye basın.")




