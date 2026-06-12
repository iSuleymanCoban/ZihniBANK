import tkinter as tk

class BankaArayuz:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        # Pencere başlığı ve boyutu
        self.root.title("Mobil Bankacılık")
        self.root.geometry("400x600")
        self.root.configure(bg="#2c3e50") # Koyu mavi arka plan rengi
        
        # Hangi ekranda olduğumuzu tutacağımız değişken
        self.mevcut_frame = None

    # Eski ekranı silip yerine yeni ve boş bir ekran (frame) oluşturan fonksiyon
    def ekrantemizle(self):
        if self.mevcut_frame != None:
            self.mevcut_frame.destroy()
            
        self.mevcut_frame = tk.Frame(self.root, bg="#2c3e50")
        self.mevcut_frame.pack(fill="both", expand=True)

    # Programa ilk girdiğimizdeki giriş ekranı
    def girisekran(self):
        self.ekrantemizle()
        
        # Başlık yazısı
        baslik = tk.Label(self.mevcut_frame, text="🏦 Mobil Bankacılık", font=('Helvetica', 20, 'bold'), bg="#2c3e50", fg="#f1c40f")
        baslik.pack(pady=40)
        
        # Hesap Numarası Alanı
        tk.Label(self.mevcut_frame, text="Hesap Numarası", bg="#2c3e50", fg="white", font=('Helvetica', 10)).pack(pady=5)
        hesap_entry = tk.Entry(self.mevcut_frame, font=('Helvetica', 12), width=20)
        hesap_entry.pack(pady=5)
        
        # Şifre Alanı (show="*" sayesinde yazılar gizlenir)
        tk.Label(self.mevcut_frame, text="Şifre", bg="#2c3e50", fg="white", font=('Helvetica', 10)).pack(pady=5)
        sifre_entry = tk.Entry(self.mevcut_frame, font=('Helvetica', 12), width=20, show="*")
        sifre_entry.pack(pady=5)
        
        # Giriş Yap Butonu
        btn_giris = tk.Button(self.mevcut_frame, text="🔑 Giriş Yap", bg="#27ae60", fg="white", font=('Helvetica', 12), width=15,
                              command=lambda: self.controller.giriskontrol(hesap_entry.get(), sifre_entry.get()))
        btn_giris.pack(pady=20)
        
        # Kayıt Ol Butonu
        btn_kayit = tk.Button(self.mevcut_frame, text="📝 Yeni Hesap Aç", bg="#2980b9", fg="white", font=('Helvetica', 12), width=15,
                              command=self.kayıtol)
        btn_kayit.pack(pady=10)

    # Yeni hesap açmak isteyenlerin geldiği ekran
    def kayıtol(self):
        self.ekrantemizle()
        
        tk.Label(self.mevcut_frame, text="📝 Kayıt Ol", font=('Helvetica', 20, 'bold'), bg="#2c3e50", fg="#f1c40f").pack(pady=30)
        
        tk.Label(self.mevcut_frame, text="İsim", bg="#2c3e50", fg="white").pack(pady=5)
        isim_entry = tk.Entry(self.mevcut_frame, font=('Helvetica', 12), width=20)
        isim_entry.pack(pady=5)
        
        tk.Label(self.mevcut_frame, text="Soyisim", bg="#2c3e50", fg="white").pack(pady=5)
        soyisim_entry = tk.Entry(self.mevcut_frame, font=('Helvetica', 12), width=20)
        soyisim_entry.pack(pady=5)
        
        tk.Label(self.mevcut_frame, text="Şifre", bg="#2c3e50", fg="white").pack(pady=5)
        sifre_entry = tk.Entry(self.mevcut_frame, font=('Helvetica', 12), width=20, show="*")
        sifre_entry.pack(pady=5)
        
        btn_kaydol = tk.Button(self.mevcut_frame, text="✅ Kaydı Tamamla", bg="#27ae60", fg="white", font=('Helvetica', 12), width=15,
                               command=lambda: self.controller.kayıtol(isim_entry.get(), soyisim_entry.get(), sifre_entry.get()))
        btn_kaydol.pack(pady=20)
        
        btn_geri = tk.Button(self.mevcut_frame, text="⬅ Geri Dön", bg="#c0392b", fg="white", font=('Helvetica', 12), width=15,
                             command=self.girisekran)
        btn_geri.pack(pady=5)

    # Giriş yaptıktan sonra açılan Ana Menü
    def anamenu(self):
        self.ekrantemizle()
        
        isim = self.controller.isim()
        
        tk.Label(self.mevcut_frame, text=f"👋 Merhaba, {isim}", font=('Helvetica', 20, 'bold'), bg="#2c3e50", fg="#f1c40f").pack(pady=20)
        
        # Bakiye yazısı
        self.bakiye_label = tk.Label(self.mevcut_frame, text="", font=('Helvetica', 18, 'bold'), bg="#2c3e50", fg="white")
        self.bakiye_label.pack(pady=10)
        self.bakiyereset() # Bakiyeyi veritabanından çekip yazıya yazar
        
        tk.Label(self.mevcut_frame, text=f"Hesap No: {self.controller.aktif_kullanici}", bg="#2c3e50", fg="#bdc3c7").pack(pady=5)
        
        # İşlem butonları
        btn_para_isleri = tk.Button(self.mevcut_frame, text="💳 Para Yatır / Çek", bg="#2980b9", fg="white", font=('Helvetica', 12), width=20, pady=5,
                                    command=self.parayatcek)
        btn_para_isleri.pack(pady=10)
                                
        btn_havale = tk.Button(self.mevcut_frame, text="💸 Para Gönderme", bg="#8e44ad", fg="white", font=('Helvetica', 12), width=20, pady=5,
                               command=self.havale)
        btn_havale.pack(pady=10)
                                
        btn_kredi = tk.Button(self.mevcut_frame, text="🏦 Kredi Çekme", bg="#e67e22", fg="white", font=('Helvetica', 12), width=20, pady=5,
                              command=self.kredi)
        btn_kredi.pack(pady=10)
        
        btn_cikis = tk.Button(self.mevcut_frame, text="🚪 Çıkış Yap", bg="#c0392b", fg="white", font=('Helvetica', 12), width=20, pady=5,
                              command=self.controller.exit)
        btn_cikis.pack(pady=20)

    # Bakiyeyi güncelleyen  fonksiyon
    def bakiyereset(self):
        bakiye = self.controller.guncelpara()
        self.bakiye_label.config(text=f"Bakiye: {bakiye} TL")

    # Para Yatırma ve Çekme ekranı
    def parayatcek(self):
        self.ekrantemizle()
        tk.Label(self.mevcut_frame, text="💳 Para İşlemleri", font=('Helvetica', 20, 'bold'), bg="#2c3e50", fg="#f1c40f").pack(pady=30)
        
        tk.Label(self.mevcut_frame, text="Miktar (TL)", bg="#2c3e50", fg="white").pack(pady=5)
        miktar_entry = tk.Entry(self.mevcut_frame, font=('Helvetica', 12), width=20)
        miktar_entry.pack(pady=5)
        
        btn_yatir = tk.Button(self.mevcut_frame, text="🔽 Para Yatır", bg="#27ae60", fg="white", font=('Helvetica', 12), width=15,
                              command=lambda: self.controller.parayatir(miktar_entry.get()))
        btn_yatir.pack(pady=10)
        
        btn_cek = tk.Button(self.mevcut_frame, text="🔼 Para Çek", bg="#d35400", fg="white", font=('Helvetica', 12), width=15,
                            command=lambda: self.controller.paracek(miktar_entry.get()))
        btn_cek.pack(pady=10)
        
        btn_geri = tk.Button(self.mevcut_frame, text="⬅ Ana Menüye Dön", bg="#7f8c8d", fg="white", font=('Helvetica', 12), width=15,
                             command=self.anamenu)
        btn_geri.pack(pady=30)

    # Başkasına para gönderme ekranı
    def havale(self):
        self.ekrantemizle()
        tk.Label(self.mevcut_frame, text="💸 Para Gönderme", font=('Helvetica', 20, 'bold'), bg="#2c3e50", fg="#f1c40f").pack(pady=30)
        
        tk.Label(self.mevcut_frame, text="Alıcı Hesap No", bg="#2c3e50", fg="white").pack(pady=5)
        hedef_entry = tk.Entry(self.mevcut_frame, font=('Helvetica', 12), width=20)
        hedef_entry.pack(pady=5)
        
        tk.Label(self.mevcut_frame, text="Miktar (TL)", bg="#2c3e50", fg="white").pack(pady=5)
        miktar_entry = tk.Entry(self.mevcut_frame, font=('Helvetica', 12), width=20)
        miktar_entry.pack(pady=5)
        
        tk.Label(self.mevcut_frame, text="* %1 Komisyon kesilecektir.", bg="#2c3e50", fg="#e74c3c").pack(pady=10)
        
        btn_gonder = tk.Button(self.mevcut_frame, text="🚀 Gönder", bg="#8e44ad", fg="white", font=('Helvetica', 12), width=15,
                               command=lambda: self.controller.paragönder(hedef_entry.get(), miktar_entry.get()))
        btn_gonder.pack(pady=10)
        
        btn_geri = tk.Button(self.mevcut_frame, text="⬅ Ana Menüye Dön", bg="#7f8c8d", fg="white", font=('Helvetica', 12), width=15,
                             command=self.anamenu)
        btn_geri.pack(pady=10)

    # Kredi çekme ekranı
    def kredi(self):
        self.ekrantemizle()
        tk.Label(self.mevcut_frame, text="🏦 Kredi Çekme", font=('Helvetica', 20, 'bold'), bg="#2c3e50", fg="#f1c40f").pack(pady=30)
        
        tk.Label(self.mevcut_frame, text="Kredi Miktarı (TL)", bg="#2c3e50", fg="white").pack(pady=5)
        miktar_entry = tk.Entry(self.mevcut_frame, font=('Helvetica', 12), width=20)
        miktar_entry.pack(pady=5)
        
        tk.Label(self.mevcut_frame, text="Vade (Kaç Ay?)", bg="#2c3e50", fg="white").pack(pady=5)
        vade_entry = tk.Entry(self.mevcut_frame, font=('Helvetica', 12), width=20)
        vade_entry.pack(pady=5)
        
        tk.Label(self.mevcut_frame, text="* Aylık %1.5 Faiz Uygulanır.", bg="#2c3e50", fg="#e74c3c").pack(pady=10)
        
        btn_hesapla = tk.Button(self.mevcut_frame, text="📋 Hesapla ve Onayla", bg="#e67e22", fg="white", font=('Helvetica', 12), width=15,
                                command=lambda: self.controller.kredicek(miktar_entry.get(), vade_entry.get()))
        btn_hesapla.pack(pady=10)
        
        btn_geri = tk.Button(self.mevcut_frame, text="⬅ Ana Menüye Dön", bg="#7f8c8d", fg="white", font=('Helvetica', 12), width=15,
                             command=self.anamenu)
        btn_geri.pack(pady=10)
