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
