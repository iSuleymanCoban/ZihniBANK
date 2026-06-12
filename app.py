import streamlit as st
from veritabani import Veritabani
from hesaplamalar import Hesaplamalar

# --- Sayfa Ayarları ---
st.set_page_config(
    page_title="Modern Banka Uygulaması",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Özel CSS (Gelişmiş Modern Tema) ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #f1f2f6;
        font-family: 'Inter', sans-serif;
    }
    
    /* Kart/Konteyner Görünümü (Glassmorphism) */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
    }
    div[data-testid="stForm"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
    }

    /* Başlıklar ve Metinler */
    h1, h2, h3, h4, p, label {
        color: #ffffff !important;
    }
    
    /* Input Alanları - Daha Büyük ve Şık */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: rgba(0, 0, 0, 0.25);
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 16px !important;
        font-size: 1.15rem !important;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #00d2ff;
        background-color: rgba(0, 0, 0, 0.4);
        box-shadow: 0 0 12px rgba(0, 210, 255, 0.5);
    }

    /* Butonlar */
    .stButton>button, .stFormSubmitButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white !important;
        border-radius: 30px;
        border: none;
        padding: 12px 30px;
        font-weight: 700;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.3);
        width: 100%;
        margin-top: 15px;
    }
    .stButton>button:hover, .stFormSubmitButton>button:hover {
        background: linear-gradient(90deg, #3a7bd5 0%, #00d2ff 100%);
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(0, 210, 255, 0.6);
    }
    
    /* Bakiye Göstergesi */
    .metric-value {
        font-size: 4rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        text-align: center;
        text-shadow: 2px 4px 6px rgba(0,0,0,0.2);
        line-height: 1.2;
    }

    /* Tablar */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 12px 12px 0 0;
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0 20px;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.2) !important;
        border-bottom: 4px solid #00d2ff !important;
        color: #00d2ff !important;
    }
    
    /* Hata/Başarı Mesajları Kutusu */
    div[data-testid="stAlert"] {
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Veritabanı ve Hesaplamalar Sınıfı ---
# Veritabanını önbelleklemiyoruz ki her thread (kullanıcı) kendi bağlantısını açsın
def get_db():
    return Veritabani()

@st.cache_resource
def get_hesaplamalar():
    return Hesaplamalar()

try:
    db = get_db()
except Exception as e:
    st.error("Veritabanı bağlantısı sağlanamadı. Lütfen daha sonra tekrar deneyin.")
    st.stop()
    
hesap = get_hesaplamalar()

# --- Session State Başlatma (Güvenli Kontrol) ---
if "aktif_hesap" not in st.session_state:
    st.session_state["aktif_hesap"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"

def change_page(page_name):
    st.session_state["page"] = page_name

def logout():
    st.session_state["aktif_hesap"] = None
    st.session_state["page"] = "login"

# --- Sayfa: GİRİŞ ---
def login_page():
    # Sayfayı yatayda ortalamak için boşluklu kolon yapısı kullanıyoruz
    _, col, _ = st.columns([1, 2, 1])
    
    with col:
        st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🏦 Banka Girişi</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #aaa; margin-bottom: 2rem;'>Hesabınıza güvenle giriş yapın.</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            hesap_no = st.text_input("Hesap Numarası", placeholder="Örn: 12345678")
            sifre = st.text_input("Şifre", type="password", placeholder="Şifrenizi giriniz")
            submit = st.form_submit_button("Giriş Yap")
            
            if submit:
                if not hesap_no.strip() or not sifre.strip():
                    st.warning("Lütfen tüm alanları doldurun.")
                else:
                    user = db.userkontrol(hesap_no, sifre)
                    if user:
                        st.session_state["aktif_hesap"] = user[3] # 3. index hesap_no
                        st.session_state["page"] = "dashboard"
                        st.rerun()
                    else:
                        st.error("Hesap Numarası veya Şifre hatalı!")
                        
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Hesabın yok mu? Yeni Kayıt Oluştur", on_click=change_page, args=("register",))

# --- Sayfa: KAYIT ---
def register_page():
    _, col, _ = st.columns([1, 2, 1])
    
    with col:
        st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>📝 Kayıt Ol</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #aaa; margin-bottom: 2rem;'>Saniyeler içinde yeni bir hesap açın.</p>", unsafe_allow_html=True)
        
        with st.form("register_form"):
            isim = st.text_input("İsim", placeholder="Adınız")
            soyisim = st.text_input("Soyisim", placeholder="Soyadınız")
            sifre = st.text_input("Şifre Belirleyin", type="password", placeholder="Güçlü bir şifre seçin")
            submit = st.form_submit_button("Hesap Oluştur")
            
            if submit:
                if not isim.strip() or not soyisim.strip() or not sifre.strip():
                    st.warning("Hiçbir alan boş bırakılamaz!")
                else:
                    try:
                        yeni_hesap_no = db.userekle(isim, soyisim, sifre)
                        st.success(f"Kayıt Başarılı! Hesap Numaranız: **{yeni_hesap_no}**")
                        st.info("Lütfen hesap numaranızı not alıp giriş sayfasına ilerleyin.")
                    except Exception as e:
                        st.error(f"Kayıt sırasında beklenmedik bir hata oluştu: {str(e)}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Zaten hesabın var mı? Giriş Yap", on_click=change_page, args=("login",))

# --- Sayfa: ANA PANEL ---
def dashboard_page():
    aktif_hesap = st.session_state.get("aktif_hesap")
    
    # Güvenlik kontrolü
    if not aktif_hesap:
        change_page("login")
        st.rerun()
        
    user = db.hesapbul(aktif_hesap)
    bakiye = db.paracekv(aktif_hesap)
    
    # Üst Bilgi (Header) Alanı
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.markdown(f"<h2>Hoş Geldiniz, <span style='color:#00d2ff'>{user[1]} {user[2]}</span></h2>", unsafe_allow_html=True)
    with header_col2:
        # Çıkış butonunu sağa ve aşağıya hizalamak için küçük bir boşluk eklendi
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        st.button("🚪 Çıkış Yap", on_click=logout, type="primary")
        
    st.divider()
        
    # Bakiye Gösterimi
    st.markdown("<p style='text-align: center; font-size: 1.4rem; margin-top: 1rem; color: #ccc;'>Güncel Bakiyeniz</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='metric-value'>{bakiye:,.2f} TL</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # İşlemler (Tablar)
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Para Yatır", "💵 Para Çek", "💸 Havale/EFT", "📊 Kredi Hesapla"])
    
    with tab1:
        st.markdown("### 📥 Hesabınıza Para Ekleyin")
        _, form_col, _ = st.columns([1, 4, 1])
        with form_col:
            with st.form("deposit_form", clear_on_submit=True):
                miktar_yatir = st.number_input("Yatırılacak Miktar (TL)", min_value=1.0, step=50.0, format="%.2f")
                if st.form_submit_button("Onayla ve Yatır"):
                    try:
                        mevcut = db.paracekv(aktif_hesap)
                        db.moneyreset(aktif_hesap, mevcut + miktar_yatir)
                        db.logtut(aktif_hesap, "Para Yatırma", miktar_yatir)
                        st.success(f"{miktar_yatir:,.2f} TL başarıyla yatırıldı!")
                        st.rerun()
                    except:
                        st.error("İşlem sırasında bir hata oluştu.")

    with tab2:
        st.markdown("### 📤 Hesabınızdan Para Çekin")
        _, form_col, _ = st.columns([1, 4, 1])
        with form_col:
            with st.form("withdraw_form", clear_on_submit=True):
                miktar_cek = st.number_input("Çekilecek Miktar (TL)", min_value=1.0, step=50.0, format="%.2f")
                if st.form_submit_button("Onayla ve Çek"):
                    mevcut = db.paracekv(aktif_hesap)
                    if hesap.para_kontrol(mevcut, miktar_cek):
                        try:
                            db.moneyreset(aktif_hesap, mevcut - miktar_cek)
                            db.logtut(aktif_hesap, "Para Çekme", miktar_cek)
                            st.success(f"{miktar_cek:,.2f} TL çekildi!")
                            st.rerun()
                        except:
                            st.error("Veritabanı hatası!")
                    else:
                        st.error("❌ Yetersiz bakiye! İşlem gerçekleştirilemedi.")

    with tab3:
        st.markdown("### 🔄 Başka Bir Hesaba Para Transferi")
        _, form_col, _ = st.columns([1, 4, 1])
        with form_col:
            with st.form("transfer_form", clear_on_submit=True):
                hedef_hesap = st.text_input("Alıcı Hesap No (8 Haneli)", placeholder="Örn: 87654321")
                miktar_gonder = st.number_input("Gönderilecek Miktar (TL)", min_value=1.0, step=50.0, format="%.2f")
                
                st.info("Not: %1 oranında havale komisyonu kesilir (Maksimum 50 TL).")
                
                if st.form_submit_button("Gönder"):
                    if not hedef_hesap.strip():
                        st.warning("Lütfen alıcı hesap numarasını girin.")
                    elif hedef_hesap == aktif_hesap:
                        st.error("Kendi hesabınıza para gönderemezsiniz!")
                    else:
                        alici = db.hesapbul(hedef_hesap)
                        if not alici:
                            st.error("Alıcı hesap numarası bulunamadı! Lütfen kontrol edin.")
                        else:
                            komisyon = hesap.komisyon(miktar_gonder)
                            toplam_gerekli = miktar_gonder + komisyon
                            mevcut = db.paracekv(aktif_hesap)
                            
                            if hesap.para_kontrol(mevcut, toplam_gerekli):
                                try:
                                    db.moneyreset(aktif_hesap, mevcut - toplam_gerekli)
                                    db.moneyreset(hedef_hesap, db.paracekv(hedef_hesap) + miktar_gonder)
                                    db.logtut(aktif_hesap, f"Gönderilen Havale ({hedef_hesap})", miktar_gonder)
                                    db.logtut(hedef_hesap, f"Gelen Havale ({aktif_hesap})", miktar_gonder)
                                    st.success(f"Transfer Başarılı! Kesilen komisyon: {komisyon:,.2f} TL")
                                    st.rerun()
                                except:
                                    st.error("Transfer sırasında ağ/veritabanı hatası oluştu.")
                            else:
                                st.error(f"❌ Yetersiz bakiye! (Gönderim + Komisyon için gerekli tutar: {toplam_gerekli:,.2f} TL)")

    with tab4:
        st.markdown("### 📈 İhtiyaç Kredisi Hesaplama Modülü")
        _, form_col, _ = st.columns([1, 4, 1])
        with form_col:
            with st.form("loan_form"):
                ana_para = st.number_input("Kredi Tutarı (Ana Para - TL)", min_value=1000.0, step=1000.0, format="%.2f")
                vade = st.number_input("Vade Süresi (Ay)", min_value=1, max_value=120, step=12)
                
                if st.form_submit_button("Hesapla"):
                    toplam_odeme, aylik_taksit = hesap.faizhesap(ana_para, vade)
                    
                    st.markdown(f"""
                        <div style="background-color:rgba(0,0,0,0.3); padding: 20px; border-radius: 12px; margin-top:10px;">
                            <h4 style="color:#00d2ff; text-align:center; margin-bottom:15px;">Ödeme Planı Özeti</h4>
                            <p><b>Kredi Tutarı:</b> {ana_para:,.2f} TL</p>
                            <p><b>Vade:</b> {vade} Ay</p>
                            <hr style="border-color: rgba(255,255,255,0.1)">
                            <p style="font-size: 1.2rem;"><b>Aylık Taksit:</b> <span style="color:#10B981">{aylik_taksit:,.2f} TL</span></p>
                            <p style="font-size: 1.2rem;"><b>Toplam Geri Ödeme:</b> <span style="color:#EF4444">{toplam_odeme:,.2f} TL</span></p>
                        </div>
                    """, unsafe_allow_html=True)


# --- Ana Akış (Routing) Yönlendiricisi ---
try:
    if st.session_state["page"] == "login":
        login_page()
    elif st.session_state["page"] == "register":
        register_page()
    elif st.session_state["page"] == "dashboard":
        dashboard_page()
except Exception as e:
    st.error("Uygulama çalışırken beklenmedik bir hata oluştu. Lütfen sayfayı yenileyin.")
