import tkinter as tk
from ana_dongu import BankaController

# Uygulamanın çalışmaya başladığı ana fonksiyon
def main():
    root = tk.Tk()
    root.geometry("400x600")
    root.resizable(False, False)  
    # Ana döngü dosyamızdaki denetleyiciyi başlatıyoruz
    # Bu sayede arayüz ve veritabanı birbirine bağlanıyor
    app = BankaController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
