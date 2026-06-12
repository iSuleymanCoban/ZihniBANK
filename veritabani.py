import sqlite3
import random

class Veritabani:
    
    def __init__(self):
        self.baglanti = sqlite3.connect("banka.db")
        self.imlec = self.baglanti.cursor()
        self.kurtablo()

    def kurtablo(self):
        # Kullanıcıların bilgilerini tutacağımız tablo
        self.imlec.execute('''
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
        self.imlec.execute('''
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
        while True:
            rastgele_sayi = str(random.randint(10000000, 99999999))
            self.imlec.execute("SELECT * FROM kullanicilar WHERE hesap_no=?", (rastgele_sayi,))
            sonuc = self.imlec.fetchone()
    
            if sonuc == None:
                return rastgele_sayi

    # Para yatırma/çekme gibi işlemleri kaydeden fonksiyon
    def logtut(self, hesap_no, islem_tipi, miktar):
        self.imlec.execute(
            "INSERT INTO islemler (hesap_no, islem_tipi, miktar) VALUES (?, ?, ?)",
            (hesap_no, islem_tipi, miktar)
        )
        self.baglanti.commit()

    # Yeni bir kullanıcı ekleyen fonksiyon
    def userekle(self, isim, soyisim, sifre):
        # Önce rastgele bir hesap numarası alıyoruz
        yeni_hesap_no = self.hesapnocreate()
        
        self.imlec.execute(
            "INSERT INTO kullanicilar (isim, soyisim, hesap_no, sifre) VALUES (?, ?, ?, ?)",
            (isim, soyisim, yeni_hesap_no, sifre)
        )
        self.baglanti.commit()
        
        
        return yeni_hesap_no

    # Giriş yaparken hesap no ve şifre doğru mu diye kontrol eden fonksiyon
    def userkontrol(self, hesap_no, sifre):
        self.imlec.execute(
            "SELECT * FROM kullanicilar WHERE hesap_no=? AND sifre=?",
            (hesap_no, sifre)
        )
        # Eğer doğruysa kullanıcının bilgilerini, yanlışsa None döndürür
        return self.imlec.fetchone()

    # Hesaptaki parayı getiren fonksiyon
    def paracekv(self, hesap_no):
        self.imlec.execute("SELECT bakiye FROM kullanicilar WHERE hesap_no=?", (hesap_no,))
        sonuc = self.imlec.fetchone()
        
        if sonuc != None:
            return sonuc[0] # sonucun içindeki ilk veri bakiyedir
        else:
            return 0.0

    # Para yatırma/çekme işlemi sonrası yeni bakiyeyi güncelleyen fonksiyon
    def moneyreset(self, hesap_no, yeni_bakiye):
        self.imlec.execute(
            "UPDATE kullanicilar SET bakiye=? WHERE hesap_no=?",
            (yeni_bakiye, hesap_no)
        )
        self.baglanti.commit()

    # Sadece hesap numarasını kullanarak kullanıcının adını/soyadını bulduğumuz fonksiyon
    def hesapbul(self, hesap_no):
        self.imlec.execute("SELECT * FROM kullanicilar WHERE hesap_no=?", (hesap_no,))
        return self.imlec.fetchone()

    # Program kapanırken veritabanı bağlantısını kapatan fonksiyon
    def sistemi_kapat(self):
        self.baglanti.close()
