import sqlite3

# veriler.db isimli bir veritabanı yarat
baglanti = sqlite3.connect("veriler.db")

# tablo yaratma, silme ve diğer işlemler için cursor nesnesi yarat
imlec = baglanti.cursor()
sorgu = "CREATE TABLE IF NOT EXISTS kullanicilar (ad TEXT, email TEXT, sifre TEXT)"
# sql sorgusunu çalıştır
imlec.execute(sorgu)
# tüm veritabanı işlemlerini uygula, kaydet
baglanti.commit()

#tabloya veri kaydet
sorgu = "INSERT INTO kullanicilar VALUES('ali', 'a@gmail.com', '1234')"
imlec.execute(sorgu)

baglanti.commit()
sorgu = """CREATE TABLE IF NOT EXISTS urunler (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                               isbn TEXT, 
                                               isim TEXT,
                                               tur text,
                                               yazar text,
                                               fiyat real,
                                               resim TEXT)"""
# sql sorgusunu çalıştır
imlec.execute(sorgu)
# tüm veritabanı işlemlerini uygula, kaydet
baglanti.commit()

#tabloya veri kaydet
import random
semboller= "0123456789abcdefghijklmnoprstABCDEFGHJKLMNPRST"
urun_kodu = "".join(random.choices(semboller, k=5))

#sorgu = f"INSERT INTO urunler (kod, kitapad, yazar,tur, resim) VALUES ('{urun_kodu}', 'Peygamberin Hayatı', 'Salih Suruç','Din', 'indir.jpg')"
#imlec.execute(sorgu)

baglanti.commit()






