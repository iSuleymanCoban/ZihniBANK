import tkinter as tk
from tkinter import messagebox
from veritabani import Veritabani
from hesaplamalar import Hesaplamalar
import arayuz

class BankaController:
    # Program ilk açıldığında çalışan ana ayarlar
    def __init__(self, root):
        self.root = root
        
        # Veritabanı ve hesaplama sınıflarımızı çağırıyoruz
        self.db = Veritabani()
        self.hesap_math = Hesaplamalar()
        
        # Henüz giriş yapan kimse yok
        self.aktif_kullanici = None 

        # Arayüzü başlatıyoruz ve ilk ekran olarak giriş ekranını açıyoruz
        self.view = arayuz.BankaArayuz(self.root, self)
        self.view.girisekran()

    # Çıkış yap butonuna basıldığında çalışır
    def exit(self):
        self.aktif_kullanici = None
        self.view.girisekran()

    # Giriş yap butonuna basıldığında çalışır
    def giriskontrol(self, hesap_no, sifre):
        # Eğer boş bırakılan yer varsa uyarı ver
        if hesap_no == "" or sifre == "":
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        # Veritabanında böyle biri var mı diye bakıyoruz
        kullanici = self.db.userkontrol(hesap_no, sifre)
        
        # Eğer kullanıcı bulunduysa
        if kullanici != None:
            self.aktif_kullanici = hesap_no
            self.view.anamenu() # Ana menüye geç
            messagebox.showinfo("Başarılı", f"Hoşgeldiniz, {kullanici[1]} {kullanici[2]}!")
        else:
            messagebox.showerror("Hata", "Hatalı Hesap No veya Şifre!")

    # Yeni kayıt ol butonuna basıldığında çalışır
    def kayıtol(self, isim, soyisim, sifre):
        if isim == "" or soyisim == "" or sifre == "":
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        # Veritabanına yeni kişiyi ekle
        yeni_hesap_no = self.db.userekle(isim, soyisim, sifre)
        messagebox.showinfo("Başarılı", f"Hesabınız oluşturuldu!\nHesap Numaranız: {yeni_hesap_no}\nLütfen kaybetmeyin.")
        
        # Kayıt olduktan sonra giriş ekranına geri dön
        self.view.girisekran()

    # Para yatır butonuna basıldığında çalışır
    def parayatir(self, miktar_str):
        # Girilen yazıyı sayıya (float) çevirmeyi deniyoruz
        try:
            miktar = float(miktar_str)
            if miktar <= 0:
                # 0 veya eksi bir değerse hata verdiriyoruz
                raise ValueError 
        except ValueError:
            messagebox.showerror("Hata", "Lütfen düzgün bir sayı giriniz.")
            return

        # Mevcut paramızı veritabanından öğreniyoruz
        mevcut_bakiye = self.db.paracekv(self.aktif_kullanici)
        yeni_bakiye = mevcut_bakiye + miktar
        
        # Yeni paramızı veritabanına yazdırıyoruz
        self.db.moneyreset(self.aktif_kullanici, yeni_bakiye)
        self.db.logtut(self.aktif_kullanici, "Para Yatırma", miktar)
        
        messagebox.showinfo("Başarılı", f"{miktar} TL başarıyla yatırıldı.\nYeni Bakiyeniz: {yeni_bakiye} TL")
        self.view.anamenu() # İşlem bitince ana menüye dön

    # Para çek butonuna basıldığında çalışır
    def paracek(self, miktar_str):
        try:
            miktar = float(miktar_str)
            if miktar <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Hata", "Lütfen düzgün bir sayı giriniz.")
            return

        mevcut_bakiye = self.db.paracekv(self.aktif_kullanici)
        
        # Paramız yetiyor mu diye kontrol ediyoruz
        if self.hesap_math.para_kontrol(mevcut_bakiye, miktar) == True:
            yeni_bakiye = mevcut_bakiye - miktar
            self.db.moneyreset(self.aktif_kullanici, yeni_bakiye)
            self.db.logtut(self.aktif_kullanici, "Para Çekme", -miktar)
            messagebox.showinfo("Başarılı", f"{miktar} TL başarıyla çekildi.\nYeni Bakiyeniz: {yeni_bakiye} TL")
            self.view.anamenu()
        else:
            messagebox.showerror("Hata", "Hesabınızda bu kadar para yok!")

    # Para gönder butonuna basıldığında çalışır
    def paragönder(self, hedef_hesap, miktar_str):
        if hedef_hesap == "" or miktar_str == "":
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        if hedef_hesap == self.aktif_kullanici:
            messagebox.showerror("Hata", "Kendinize para gönderemezsiniz.")
            return

        # Parayı göndereceğimiz kişi gerçekten var mı diye bakıyoruz
        alici = self.db.hesapbul(hedef_hesap)
        if alici == None:
            messagebox.showerror("Hata", "Böyle bir hesap numarası bulunamadı.")
            return

        try:
            miktar = float(miktar_str)
            if miktar <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Hata", "Lütfen düzgün bir sayı giriniz.")
            return

        # Komisyonu hesaplıyoruz
        komisyon = self.hesap_math.komisyon(miktar)
        toplam_kesilecek = miktar + komisyon
        mevcut_bakiye = self.db.paracekv(self.aktif_kullanici)

        # Paramız komisyonla birlikte yetiyor mu diye bakıyoruz
        if self.hesap_math.para_kontrol(mevcut_bakiye, toplam_kesilecek) == True:
            
            # 1. Kendi hesabımdan parayı düşüyorum
            self.db.moneyreset(self.aktif_kullanici, mevcut_bakiye - toplam_kesilecek)
            self.db.logtut(self.aktif_kullanici, f"Transfer: {hedef_hesap}", -toplam_kesilecek)
            
            # 2. Karşı tarafın hesabına parayı ekliyorum
            alici_bakiye = self.db.paracekv(hedef_hesap)
            self.db.moneyreset(hedef_hesap, alici_bakiye + miktar)
            self.db.logtut(hedef_hesap, f"Gelen: {self.aktif_kullanici}", miktar)
            
            messagebox.showinfo("Başarılı", f"İşlem başarılı!\nGönderilen: {miktar} TL\nKesilen Komisyon: {komisyon} TL")
            self.view.anamenu()
        else:
            messagebox.showerror("Hata", f"Yetersiz bakiye! Bu işlem için hesabınızda en az {toplam_kesilecek} TL olmalıdır.")

    # Kredi hesapla ve onayla butonuna basıldığında çalışır
    def kredicek(self, miktar_str, vade_str):
        try:
            miktar = float(miktar_str)
            vade = int(vade_str)
            if miktar <= 0 or vade <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Hata", "Lütfen miktar ve vadeyi düzgün giriniz.")
            return

        # Geri ne kadar ödeyeceğimizi hesaplıyoruz
        toplam_odenecek, aylik_taksit = self.hesap_math.faizhesap(miktar, vade)
        
        # Kullanıcıya bir soru kutucuğu çıkarıyoruz
        soru = f"Kredi Tutarı: {miktar} TL\nVade: {vade} Ay\nToplam Geri Ödeme: {toplam_odenecek} TL\nAylık Taksit: {aylik_taksit} TL\n\nKrediyi onaylıyor musunuz?"
        onay = messagebox.askyesno("Kredi Onayı", soru)
        
        if onay == True:
            mevcut_bakiye = self.db.paracekv(self.aktif_kullanici)
            yeni_bakiye = mevcut_bakiye + miktar
            
            self.db.moneyreset(self.aktif_kullanici, yeni_bakiye)
            self.db.logtut(self.aktif_kullanici, "Kredi Kullanımı", miktar)
            
            messagebox.showinfo("Başarılı", f"{miktar} TL kredi hesabınıza yatırıldı.")
            self.view.anamenu()

    # Ekrandaki bakiyeyi göstermek için gereken fonksiyon
    def guncelpara(self):
        if self.aktif_kullanici != None:
            return self.db.paracekv(self.aktif_kullanici)
        else:
            return 0.0

    # Ekrandaki "Merhaba, İsim" yazısı için gereken fonksiyon
    def isim(self):
        if self.aktif_kullanici != None:
            kullanici = self.db.hesapbul(self.aktif_kullanici)
            return f"{kullanici[1]} {kullanici[2]}" 
        else:
            return ""
