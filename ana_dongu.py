import tkinter as tk
from tkinter import messagebox
from veritabani import Veritabani
from hesaplamalar import Hesaplamalar

class BankaController:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Banka Uygulaması")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # --- Yeşil Tema Renk Paleti ---
        self.bg_color = "#022C22"       # Koyu Orman Yeşili (Arkaplan)
        self.fg_color = "#ECFDF5"       # Açık Yeşil/Beyaz (Metin)
        self.primary_color = "#10B981"  # Zümrüt Yeşili (Butonlar/Vurgu)
        self.active_color = "#059669"   # Koyu Zümrüt Yeşili (Buton Tıklama)
        self.entry_bg = "#064E3B"       # Girdi Alanı Arkaplanı
        self.danger_color = "#EF4444"   # Kırmızı (Çıkış)
        
        self.root.configure(bg=self.bg_color)

        self.db = Veritabani()
        self.hesap = Hesaplamalar()
        self.aktif_hesap = None
        
        # Fontlar
        self.font_title = ("Helvetica", 20, "bold")
        self.font_label = ("Helvetica", 11)
        self.font_btn = ("Helvetica", 12, "bold")
        
        self.frames = {}
        self.create_frames()
        self.show_frame("login")

    def create_frames(self):
        # --- 1. GİRİŞ EKRANI ---
        f_login = tk.Frame(self.root, bg=self.bg_color)
        self.frames["login"] = f_login
        
        tk.Label(f_login, text="Banka Uygulaması", font=self.font_title, bg=self.bg_color, fg=self.primary_color).pack(pady=40)
        
        tk.Label(f_login, text="Hesap Numarası:", font=self.font_label, bg=self.bg_color, fg=self.fg_color).pack(pady=5)
        self.e_login_hesap = tk.Entry(f_login, font=self.font_label, bg=self.entry_bg, fg="white", insertbackground="white", relief="flat")
        self.e_login_hesap.pack(pady=5, ipady=8, ipadx=10)
        
        tk.Label(f_login, text="Şifre:", font=self.font_label, bg=self.bg_color, fg=self.fg_color).pack(pady=5)
        self.e_login_sifre = tk.Entry(f_login, font=self.font_label, bg=self.entry_bg, fg="white", show="*", insertbackground="white", relief="flat")
        self.e_login_sifre.pack(pady=5, ipady=8, ipadx=10)
        
        tk.Button(f_login, text="Giriş Yap", font=self.font_btn, bg=self.primary_color, fg="white", activebackground=self.active_color, activeforeground="white", command=self.login, relief="flat", cursor="hand2").pack(pady=20, ipadx=40, ipady=8)
        tk.Button(f_login, text="Hesabın yok mu? Kayıt Ol", font=("Helvetica", 10, "underline"), bg=self.bg_color, fg=self.primary_color, activebackground=self.bg_color, activeforeground="white", command=lambda: self.show_frame("register"), relief="flat", cursor="hand2", bd=0).pack()

        # --- 2. KAYIT EKRANI ---
        f_reg = tk.Frame(self.root, bg=self.bg_color)
        self.frames["register"] = f_reg
        
        tk.Label(f_reg, text="Yeni Hesap Oluştur", font=self.font_title, bg=self.bg_color, fg=self.primary_color).pack(pady=30)
        
        tk.Label(f_reg, text="İsim:", font=self.font_label, bg=self.bg_color, fg=self.fg_color).pack(pady=5)
        self.e_reg_isim = tk.Entry(f_reg, font=self.font_label, bg=self.entry_bg, fg="white", insertbackground="white", relief="flat")
        self.e_reg_isim.pack(pady=5, ipady=6, ipadx=10)
        
        tk.Label(f_reg, text="Soyisim:", font=self.font_label, bg=self.bg_color, fg=self.fg_color).pack(pady=5)
        self.e_reg_soyisim = tk.Entry(f_reg, font=self.font_label, bg=self.entry_bg, fg="white", insertbackground="white", relief="flat")
        self.e_reg_soyisim.pack(pady=5, ipady=6, ipadx=10)
        
        tk.Label(f_reg, text="Şifre:", font=self.font_label, bg=self.bg_color, fg=self.fg_color).pack(pady=5)
        self.e_reg_sifre = tk.Entry(f_reg, font=self.font_label, bg=self.entry_bg, fg="white", show="*", insertbackground="white", relief="flat")
        self.e_reg_sifre.pack(pady=5, ipady=6, ipadx=10)
        
        tk.Button(f_reg, text="Kayıt Ol", font=self.font_btn, bg=self.primary_color, fg="white", activebackground=self.active_color, activeforeground="white", command=self.register, relief="flat", cursor="hand2").pack(pady=20, ipadx=40, ipady=8)
        tk.Button(f_reg, text="Zaten hesabın var mı? Giriş Yap", font=("Helvetica", 10, "underline"), bg=self.bg_color, fg=self.primary_color, activebackground=self.bg_color, activeforeground="white", command=lambda: self.show_frame("login"), relief="flat", cursor="hand2", bd=0).pack()

        # --- 3. ANA PANEL (DASHBOARD) ---
        f_dash = tk.Frame(self.root, bg=self.bg_color)
        self.frames["dashboard"] = f_dash
        
        self.l_welcome = tk.Label(f_dash, text="", font=("Helvetica", 14), bg=self.bg_color, fg=self.primary_color)
        self.l_welcome.pack(pady=(20, 5))
        
        tk.Label(f_dash, text="Güncel Bakiye", font=("Helvetica", 10), bg=self.bg_color, fg=self.fg_color).pack()
        self.l_bakiye = tk.Label(f_dash, text="0.0 TL", font=("Helvetica", 32, "bold"), bg=self.bg_color, fg="white")
        self.l_bakiye.pack(pady=(0, 20))
        
        btn_frame = tk.Frame(f_dash, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Para Yatır", font=self.font_btn, bg=self.primary_color, fg="white", activebackground=self.active_color, activeforeground="white", width=14, command=self.show_deposit, relief="flat").grid(row=0, column=0, padx=10, pady=10, ipady=8)
        tk.Button(btn_frame, text="Para Çek", font=self.font_btn, bg=self.primary_color, fg="white", activebackground=self.active_color, activeforeground="white", width=14, command=self.show_withdraw, relief="flat").grid(row=0, column=1, padx=10, pady=10, ipady=8)
        tk.Button(btn_frame, text="Havale/EFT", font=self.font_btn, bg=self.primary_color, fg="white", activebackground=self.active_color, activeforeground="white", width=14, command=self.show_transfer, relief="flat").grid(row=1, column=0, padx=10, pady=10, ipady=8)
        tk.Button(btn_frame, text="Kredi Hesapla", font=self.font_btn, bg=self.primary_color, fg="white", activebackground=self.active_color, activeforeground="white", width=14, command=self.show_loan, relief="flat").grid(row=1, column=1, padx=10, pady=10, ipady=8)
        
        tk.Button(f_dash, text="Çıkış Yap", font=self.font_btn, bg=self.danger_color, fg="white", activebackground="#DC2626", activeforeground="white", command=self.logout, relief="flat", cursor="hand2").pack(pady=30, ipadx=30, ipady=8)

    def show_frame(self, name):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def login(self):
        hesap = self.e_login_hesap.get()
        sifre = self.e_login_sifre.get()
        user = self.db.userkontrol(hesap, sifre)
        if user:
            self.aktif_hesap = user[3] # 3. index hesap_no
            self.e_login_hesap.delete(0, tk.END)
            self.e_login_sifre.delete(0, tk.END)
            self.update_dashboard()
            self.show_frame("dashboard")
        else:
            messagebox.showerror("Hata", "Hesap No veya Şifre yanlış!")

    def register(self):
        isim = self.e_reg_isim.get()
        soy = self.e_reg_soyisim.get()
        sifre = self.e_reg_sifre.get()
        if not isim or not soy or not sifre:
            messagebox.showerror("Hata", "Alanlar boş bırakılamaz!")
            return
        hesap_no = self.db.userekle(isim, soy, sifre)
        messagebox.showinfo("Başarılı", f"Kayıt başarılı! Hesap Numaranız: {hesap_no}\nLütfen giriş yapın.")
        self.show_frame("login")
        self.e_login_hesap.insert(0, hesap_no)

    def logout(self):
        self.aktif_hesap = None
        self.show_frame("login")

    def update_dashboard(self):
        if not self.aktif_hesap: return
        user = self.db.hesapbul(self.aktif_hesap)
        bakiye = self.db.paracekv(self.aktif_hesap)
        self.l_welcome.config(text=f"Merhaba, {user[1]} {user[2]}")
        self.l_bakiye.config(text=f"{bakiye} TL")

    def show_deposit(self):
        self._action_window("Para Yatır", "Yatırılacak Miktar:", self.do_deposit)

    def show_withdraw(self):
        self._action_window("Para Çek", "Çekilecek Miktar:", self.do_withdraw)

    def _action_window(self, title, label, command):
        top = tk.Toplevel(self.root)
        top.title(title)
        top.geometry("280x180")
        top.configure(bg=self.bg_color)
        tk.Label(top, text=label, bg=self.bg_color, fg=self.fg_color, font=self.font_label).pack(pady=15)
        e = tk.Entry(top, font=self.font_label, bg=self.entry_bg, fg="white", insertbackground="white", relief="flat")
        e.pack(pady=5, ipady=5, ipadx=5)
        tk.Button(top, text="Onayla", font=self.font_btn, bg=self.primary_color, fg="white", activebackground=self.active_color, activeforeground="white", command=lambda: command(top, e.get()), relief="flat").pack(pady=15, ipadx=20)

    def do_deposit(self, top, miktar):
        try:
            m = float(miktar)
            if m <= 0: raise ValueError
            mevcut = self.db.paracekv(self.aktif_hesap)
            self.db.moneyreset(self.aktif_hesap, mevcut + m)
            self.db.logtut(self.aktif_hesap, "Para Yatırma", m)
            messagebox.showinfo("Başarılı", "Para yatırma işlemi gerçekleşti!")
            top.destroy()
            self.update_dashboard()
        except:
            messagebox.showerror("Hata", "Geçersiz miktar!")

    def do_withdraw(self, top, miktar):
        try:
            m = float(miktar)
            if m <= 0: raise ValueError
            mevcut = self.db.paracekv(self.aktif_hesap)
            if self.hesap.para_kontrol(mevcut, m):
                self.db.moneyreset(self.aktif_hesap, mevcut - m)
                self.db.logtut(self.aktif_hesap, "Para Çekme", m)
                messagebox.showinfo("Başarılı", "Para çekme işlemi gerçekleşti!")
                top.destroy()
                self.update_dashboard()
            else:
                messagebox.showerror("Hata", "Yetersiz bakiye!")
        except:
            messagebox.showerror("Hata", "Geçersiz miktar!")

    def show_transfer(self):
        top = tk.Toplevel(self.root)
        top.title("Havale / EFT")
        top.geometry("300x250")
        top.configure(bg=self.bg_color)
        
        tk.Label(top, text="Alıcı Hesap No:", bg=self.bg_color, fg=self.fg_color, font=self.font_label).pack(pady=5)
        e_hedef = tk.Entry(top, font=self.font_label, bg=self.entry_bg, fg="white", insertbackground="white", relief="flat")
        e_hedef.pack(ipady=5, ipadx=5)
        
        tk.Label(top, text="Miktar:", bg=self.bg_color, fg=self.fg_color, font=self.font_label).pack(pady=5)
        e_mik = tk.Entry(top, font=self.font_label, bg=self.entry_bg, fg="white", insertbackground="white", relief="flat")
        e_mik.pack(ipady=5, ipadx=5)
        
        tk.Button(top, text="Gönder", font=self.font_btn, bg=self.primary_color, fg="white", activebackground=self.active_color, activeforeground="white", command=lambda: self.do_transfer(top, e_hedef.get(), e_mik.get()), relief="flat").pack(pady=15, ipadx=20)

    def do_transfer(self, top, hedef, miktar):
        try:
            m = float(miktar)
            if m <= 0 or hedef == self.aktif_hesap: raise ValueError
            alici = self.db.hesapbul(hedef)
            if not alici:
                messagebox.showerror("Hata", "Alıcı hesap numarası bulunamadı!")
                return
            
            komisyon = self.hesap.komisyon(m)
            toplam = m + komisyon
            mevcut = self.db.paracekv(self.aktif_hesap)
            
            if self.hesap.para_kontrol(mevcut, toplam):
                self.db.moneyreset(self.aktif_hesap, mevcut - toplam)
                self.db.moneyreset(hedef, self.db.paracekv(hedef) + m)
                self.db.logtut(self.aktif_hesap, "Gönderilen Havale", m)
                self.db.logtut(hedef, "Gelen Havale", m)
                messagebox.showinfo("Başarılı", f"Havale yapıldı.\nKesilen komisyon: {komisyon} TL")
                top.destroy()
                self.update_dashboard()
            else:
                messagebox.showerror("Hata", f"Yetersiz bakiye! (Komisyon dahil gerekli: {toplam} TL)")
        except:
            messagebox.showerror("Hata", "Geçersiz miktar veya hesap no!")

    def show_loan(self):
        top = tk.Toplevel(self.root)
        top.title("Kredi Hesaplama")
        top.geometry("300x250")
        top.configure(bg=self.bg_color)
        
        tk.Label(top, text="Kredi Tutarı (Ana Para):", bg=self.bg_color, fg=self.fg_color, font=self.font_label).pack(pady=5)
        e_ana = tk.Entry(top, font=self.font_label, bg=self.entry_bg, fg="white", insertbackground="white", relief="flat")
        e_ana.pack(ipady=5, ipadx=5)
        
        tk.Label(top, text="Vade (Ay):", bg=self.bg_color, fg=self.fg_color, font=self.font_label).pack(pady=5)
        e_vade = tk.Entry(top, font=self.font_label, bg=self.entry_bg, fg="white", insertbackground="white", relief="flat")
        e_vade.pack(ipady=5, ipadx=5)
        
        tk.Button(top, text="Hesapla", font=self.font_btn, bg=self.primary_color, fg="white", activebackground=self.active_color, activeforeground="white", command=lambda: self.do_loan(e_ana.get(), e_vade.get()), relief="flat").pack(pady=15, ipadx=20)

    def do_loan(self, ana, vade):
        try:
            a = float(ana)
            v = int(vade)
            if a <= 0 or v <= 0: raise ValueError
            toplam_geri_odeme, aylik_taksit = self.hesap.faizhesap(a, v)
            messagebox.showinfo("Kredi Sonucu", f"Kredi Tutarı: {a} TL\nVade: {v} Ay\n\nToplam Geri Ödeme: {toplam_geri_odeme} TL\nAylık Taksit: {aylik_taksit} TL")
        except:
            messagebox.showerror("Hata", "Lütfen geçerli sayılar girin!")
