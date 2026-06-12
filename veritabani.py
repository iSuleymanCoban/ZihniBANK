import sqlite3
import random

class Veritabani:
    
    def __init__(self):
        # check_same_thread=False allows Streamlit's multiple threads to use the same connection
        self.baglanti = sqlite3.connect("banka.db", check_same_thread=False)
        # Tabloları oluştur
        self.kurtablo()

    def kurtablo(self):
        cursor = self.baglanti.cursor()
        # Kullanıcıların bilgilerini tutacağımız tablo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kullanicilar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT,
                soyisim TEXT,
                hesap_no TEXT,
                sifre TEXT,
                bakiye REAL DEFAULT 0.0
            )
        ''')
        
        # İşlem geçmişini tutacağımız tablo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS islemler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hesap_no TEXT,
                islem_tipi TEXT,
                miktar REAL
            )
        ''')

        self.baglanti.commit()

    # Rastgele hesap numarası üreten fonksiyon
    def hesapnocreate(self):
        cursor = self.baglanti.cursor()
        while True:
            rastgele_sayi = str(random.randint(10000000, 99999999))
            cursor.execute("SELECT * FROM kullanicilar WHERE hesap_no=?", (rastgele_sayi,))
            sonuc = cursor.fetchone()
    
            if sonuc == None:
                return rastgele_sayi

    # Para yatırma/çekme gibi işlemleri kaydeden fonksiyon
    def logtut(self, hesap_no, islem_tipi, miktar):
        cursor = self.baglanti.cursor()
        cursor.execute(
            "INSERT INTO islemler (hesap_no, islem_tipi, miktar) VALUES (?, ?, ?)",
            (hesap_no, islem_tipi, miktar)
        )
        self.baglanti.commit()

    # Yeni bir kullanıcı ekleyen fonksiyon
    def userekle(self, isim, soyisim, sifre):
        cursor = self.baglanti.cursor()
        # Önce rastgele bir hesap numarası alıyoruz
        yeni_hesap_no = self.hesapnocreate()
        
        cursor.execute(
            "INSERT INTO kullanicilar (isim, soyisim, hesap_no, sifre) VALUES (?, ?, ?, ?)",
            (isim, soyisim, yeni_hesap_no, sifre)
        )
        self.baglanti.commit()
        
        return yeni_hesap_no

    # Giriş yaparken hesap no ve şifre doğru mu diye kontrol eden fonksiyon
    def userkontrol(self, hesap_no, sifre):
        cursor = self.baglanti.cursor()
        cursor.execute(
            "SELECT * FROM kullanicilar WHERE hesap_no=? AND sifre=?",
            (hesap_no, sifre)
        )
        # Eğer doğruysa kullanıcının bilgilerini, yanlışsa None döndürür
        return cursor.fetchone()

    # Hesaptaki parayı getiren fonksiyon
    def paracekv(self, hesap_no):
        cursor = self.baglanti.cursor()
        cursor.execute("SELECT bakiye FROM kullanicilar WHERE hesap_no=?", (hesap_no,))
        sonuc = cursor.fetchone()
        
        if sonuc != None:
            return sonuc[0] # sonucun içindeki ilk veri bakiyedir
        else:
            return 0.0

    # Para yatırma/çekme işlemi sonrası yeni bakiyeyi güncelleyen fonksiyon
    def moneyreset(self, hesap_no, yeni_bakiye):
        cursor = self.baglanti.cursor()
        cursor.execute(
            "UPDATE kullanicilar SET bakiye=? WHERE hesap_no=?",
            (yeni_bakiye, hesap_no)
        )
        self.baglanti.commit()

    # Sadece hesap numarasını kullanarak kullanıcının adını/soyadını bulduğumuz fonksiyon
    def hesapbul(self, hesap_no):
        cursor = self.baglanti.cursor()
        cursor.execute("SELECT * FROM kullanicilar WHERE hesap_no=?", (hesap_no,))
        return cursor.fetchone()

    # Program kapanırken veritabanı bağlantısını kapatan fonksiyon
    def sistemi_kapat(self):
        self.baglanti.close()
