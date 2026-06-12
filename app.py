import streamlit as st
from veritabani import Veritabani
from hesaplamalar import Hesaplamalar

# --- Sayfa Ayarları ---
st.set_page_config(
    page_title="Modern Banka Uygulaması",
    page_icon="🏦",
    layout="centered"
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
    div[data-testid="stForm"], div[data-testid="stVerticalBlock"] > div > div > div {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="stForm"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
    }

    /* Başlıklar ve Metinler */
    h1, h2, h3, p, label {
        color: #ffffff !important;
    }
    
    /* Input Alanları */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: rgba(0, 0, 0, 0.2);
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #00d2ff;
        box-shadow: 0 0 8px rgba(0, 210, 255, 0.6);
    }

    /* Butonlar */
    .stButton>button, .stFormSubmitButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 12px 28px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.4);
    }
    .stButton>button:hover, .stFormSubmitButton>button:hover {
        background: linear-gradient(90deg, #3a7bd5 0%, #00d2ff 100%);
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0, 210, 255, 0.6);
        color: white;
    }
    
    /* Bakiye Göstergesi */
    .metric-value {
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    /* Tablar */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px 10px 0 0;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.2) !important;
        border-bottom: 3px solid #00d2ff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Veritabanı ve Hesaplamalar Sınıfı ---
@st.cache_resource
def get_db():
    return Veritabani()

@st.cache_resource
def get_hesaplamalar():
    return Hesaplamalar()

db = get_db()
hesap = get_hesaplamalar()

# --- Session State Başlatma ---
if "aktif_hesap" not in st.session_state:
    st.session_state["aktif_hesap"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"

def change_page(page_name):
    st.session_state["page"] = page_name

def logout():
    st.session_state["aktif_hesap"] = None
    change_page("login")

# --- Sayfalar ---
def login_page():
    st.title("🏦 Banka Uygulaması")
    st.write("Lütfen hesabınıza giriş yapın.")
    
    with st.form("login_form"):
        hesap_no = st.text_input("Hesap Numarası")
        sifre = st.text_input("Şifre", type="password")
        submit = st.form_submit_button("Giriş Yap")
        
        if submit:
            if not hesap_no or not sifre:
                st.error("Lütfen tüm alanları doldurun.")
            else:
                user = db.userkontrol(hesap_no, sifre)
                if user:
                    st.session_state["aktif_hesap"] = user[3] # hesap_no
                    st.success("Giriş başarılı! Yönlendiriliyorsunuz...")
                    change_page("dashboard")
                    st.rerun()
                else:
                    st.error("Hesap No veya Şifre yanlış!")
                    
    st.button("Hesabın yok mu? Kayıt Ol", on_click=change_page, args=("register",))

def register_page():
    st.title("📝 Yeni Hesap Oluştur")
    
    with st.form("register_form"):
        isim = st.text_input("İsim")
        soyisim = st.text_input("Soyisim")
        sifre = st.text_input("Şifre", type="password")
        submit = st.form_submit_button("Kayıt Ol")
        
        if submit:
            if not isim or not soyisim or not sifre:
                st.error("Alanlar boş bırakılamaz!")
            else:
                hesap_no = db.userekle(isim, soyisim, sifre)
                st.success(f"Kayıt başarılı! Hesap Numaranız: **{hesap_no}**\n\nLütfen bunu not alın.")
    
    st.button("Zaten hesabın var mı? Giriş Yap", on_click=change_page, args=("login",))

def dashboard_page():
    aktif_hesap = st.session_state["aktif_hesap"]
    user = db.hesapbul(aktif_hesap)
    bakiye = db.paracekv(aktif_hesap)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"Merhaba, {user[1]} {user[2]}")
    with col2:
        st.button("Çıkış Yap", on_click=logout, type="secondary")
        
    st.markdown("<p style='text-align: center; font-size: 1.2rem; margin-top: 2rem;'>Güncel Bakiye</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;' class='metric-value'>{bakiye} TL</p>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Para Yatır", "💵 Para Çek", "💸 Havale/EFT", "📊 Kredi Hesapla"])
    
    with tab1:
        st.write("### Para Yatırma İşlemi")
        with st.form("deposit_form"):
            miktar_yatir = st.number_input("Yatırılacak Miktar (TL)", min_value=1.0, step=10.0)
            if st.form_submit_button("Onayla"):
                mevcut = db.paracekv(aktif_hesap)
                db.moneyreset(aktif_hesap, mevcut + miktar_yatir)
                db.logtut(aktif_hesap, "Para Yatırma", miktar_yatir)
                st.success(f"{miktar_yatir} TL hesabınıza yatırıldı!")
                st.rerun()

    with tab2:
        st.write("### Para Çekme İşlemi")
        with st.form("withdraw_form"):
            miktar_cek = st.number_input("Çekilecek Miktar (TL)", min_value=1.0, step=10.0)
            if st.form_submit_button("Onayla"):
                mevcut = db.paracekv(aktif_hesap)
                if hesap.para_kontrol(mevcut, miktar_cek):
                    db.moneyreset(aktif_hesap, mevcut - miktar_cek)
                    db.logtut(aktif_hesap, "Para Çekme", miktar_cek)
                    st.success(f"{miktar_cek} TL başarıyla çekildi!")
                    st.rerun()
                else:
                    st.error("Yetersiz bakiye!")

    with tab3:
        st.write("### Başka Bir Hesaba Para Gönder")
        with st.form("transfer_form"):
            hedef_hesap = st.text_input("Alıcı Hesap No")
            miktar_gonder = st.number_input("Gönderilecek Miktar (TL)", min_value=1.0, step=10.0)
            if st.form_submit_button("Gönder"):
                if hedef_hesap == aktif_hesap:
                    st.error("Kendi hesabınıza para gönderemezsiniz!")
                else:
                    alici = db.hesapbul(hedef_hesap)
                    if not alici:
                        st.error("Alıcı hesap numarası bulunamadı!")
                    else:
                        komisyon = hesap.komisyon(miktar_gonder)
                        toplam_gerekli = miktar_gonder + komisyon
                        mevcut = db.paracekv(aktif_hesap)
                        
                        if hesap.para_kontrol(mevcut, toplam_gerekli):
                            db.moneyreset(aktif_hesap, mevcut - toplam_gerekli)
                            db.moneyreset(hedef_hesap, db.paracekv(hedef_hesap) + miktar_gonder)
                            db.logtut(aktif_hesap, "Gönderilen Havale", miktar_gonder)
                            db.logtut(hedef_hesap, "Gelen Havale", miktar_gonder)
                            st.success(f"Havale yapıldı! Kesilen komisyon: {komisyon} TL")
                            st.rerun()
                        else:
                            st.error(f"Yetersiz bakiye! (Komisyon dahil gerekli tutar: {toplam_gerekli} TL)")

    with tab4:
        st.write("### Kredi Hesaplama")
        with st.form("loan_form"):
            ana_para = st.number_input("Kredi Tutarı (Ana Para - TL)", min_value=100.0, step=500.0)
            vade = st.number_input("Vade (Ay)", min_value=1, max_value=120, step=1)
            if st.form_submit_button("Hesapla"):
                toplam_odeme, aylik_taksit = hesap.faizhesap(ana_para, vade)
                st.info(f"**Kredi Tutarı:** {ana_para} TL\n\n**Vade:** {vade} Ay")
                st.success(f"**Toplam Geri Ödeme:** {toplam_odeme} TL\n\n**Aylık Taksit:** {aylik_taksit} TL")


# --- Ana Akış (Routing) ---
if st.session_state["page"] == "login":
    login_page()
elif st.session_state["page"] == "register":
    register_page()
elif st.session_state["page"] == "dashboard":
    if st.session_state["aktif_hesap"]:
        dashboard_page()
    else:
        st.session_state["page"] = "login"
        st.rerun()
