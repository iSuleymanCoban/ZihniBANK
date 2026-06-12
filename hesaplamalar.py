class Hesaplamalar:
    # Kredi faizini hesaplayan fonksiyon
    def faizhesap(self, ana_para, vade_ay):
        # Aylık %1.5 faiz
        aylik_faiz = 0.015
        
        # Matematiksel hesaplama: Anapara * (1 + (faiz * ay))
        toplam_geri_odeme = ana_para * (1 + (aylik_faiz * vade_ay))
        aylik_taksit = toplam_geri_odeme / vade_ay
    
        return round(toplam_geri_odeme, 2), round(aylik_taksit, 2)

    # Paramız çekmek istediğimiz miktara yetiyor mu diye bakan fonksiyon
    def para_kontrol(self, guncel_bakiye, cekilecek_miktar):
        if guncel_bakiye >= cekilecek_miktar:
            return True
        else:
            return False

    # Para gönderirken ne kadar komisyon keseceğimizi hesaplayan fonksiyon
    def komisyon(self, miktar):
        komisyon = miktar * 0.01
        
        if komisyon > 50:
            komisyon = 50
            
        return round(komisyon, 2)
