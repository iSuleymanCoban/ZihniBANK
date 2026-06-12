import sqlite3
import random

class Veritabani:
    def __init__(self):
        self.db_path = "banka.db"
        self.kurtablo()

    # Her işlem için yeni bir bağlantı açıp, işlem bitince otomatik kapatacağız.
    # timeout=10 ekleyerek "database is locked" sorununu çözüyoruz.
    def get_conn(self):
        return sqlite3.connect(self.db_path, timeout=10.0, check_same_thread=False)

    def kurtablo(self):
        with self.get_conn() as conn:
            cursor = conn.cursor()
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
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS islemler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hesap_no TEXT,
                    islem_tipi TEXT,
                    miktar REAL
                )
            ''')
            conn.commit()

    def hesapnocreate(self):
        while True:
            rastgele_sayi = str(random.randint(10000000, 99999999))
            with self.get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM kullanicilar WHERE hesap_no=?", (rastgele_sayi,))
                sonuc = cursor.fetchone()
                if sonuc is None:
                    return rastgele_sayi

    def logtut(self, hesap_no, islem_tipi, miktar):
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO islemler (hesap_no, islem_tipi, miktar) VALUES (?, ?, ?)",
                (hesap_no, islem_tipi, miktar)
            )
            conn.commit()

    def userekle(self, isim, soyisim, sifre):
        yeni_hesap_no = self.hesapnocreate()
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO kullanicilar (isim, soyisim, hesap_no, sifre) VALUES (?, ?, ?, ?)",
                (isim, soyisim, yeni_hesap_no, sifre)
            )
            conn.commit()
        return yeni_hesap_no

    def userkontrol(self, hesap_no, sifre):
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM kullanicilar WHERE hesap_no=? AND sifre=?",
                (hesap_no, sifre)
            )
            return cursor.fetchone()

    def paracekv(self, hesap_no):
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT bakiye FROM kullanicilar WHERE hesap_no=?", (hesap_no,))
            sonuc = cursor.fetchone()
            if sonuc is not None:
                return sonuc[0]
            return 0.0

    def moneyreset(self, hesap_no, yeni_bakiye):
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE kullanicilar SET bakiye=? WHERE hesap_no=?",
                (yeni_bakiye, hesap_no)
            )
            conn.commit()

    def hesapbul(self, hesap_no):
        with self.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM kullanicilar WHERE hesap_no=?", (hesap_no,))
            return cursor.fetchone()

    def sistemi_kapat(self):
        # Artık bağlantıları açık tutmadığımız için buna gerek yok
        pass
