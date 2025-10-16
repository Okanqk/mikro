import streamlit as st
import matplotlib.pyplot as plt
from modules.grafikler import butce_egrisi_ciz, arz_talep_grafigi
from modules.veri import EKONOMI_KONULARI

# Sayfa ayarı
st.set_page_config(
    page_title="Mikro Ekonomi Lab", 
    page_icon="📈", 
    layout="wide"
)

# Başlık
st.title("📈 Mikro Ekonomi Çalışma Laboratuvarı")
st.markdown("Ekonomi modellerini interaktif olarak öğren ve keşfet!")

# Sidebar - Ana menü
st.sidebar.title("🎯 Çalışma Modülleri")
secilen_konu = st.sidebar.selectbox(
    "Konu Seçin:",
    list(EKONOMI_KONULARI.keys()),
    format_func=lambda x: EKONOMI_KONULARI[x]["baslik"]
)

# Konu bilgilerini al
konu_bilgisi = EKONOMI_KONULARI[secilen_konu]

# Ana içerik
st.header(f"📖 {konu_bilgisi['baslik']}")
st.write(konu_bilgisi["aciklama"])

# İki sütunlu layout
col1, col2 = st.columns([2, 1])

with col1:
    # GRAFİK BÖLÜMÜ
    st.subheader("📈 İnteraktif Grafik")
    
    if secilen_konu == "iki_donemli_tuketici":
        # Parametre kontrolleri
        col1a, col1b, col1c, col1d = st.columns(4)
        with col1a:
            R1 = st.slider("R₁ - Gelir 1", 50, 200, 100)
        with col1b:
            R2 = st.slider("R₂ - Gelir 2", 50, 200, 80)
        with col1c:
            j12 = st.slider("j₁₂ - Faiz Oranı", 0.0, 0.5, 0.1, 0.01)
        with col1d:
            C1_opt = st.slider("C₁ - Tüketim 1", 0, 150, 60)
        
        # Grafik oluştur
        fig = butce_egrisi_ciz(R1, R2, j12, C1_opt)
        st.pyplot(fig)
        
        # Hesaplamalar
        C2_opt = R1*(1+j12) + R2 - (1+j12)*C1_opt
        st.info(f"**Hesaplanan C₂ Değeri:** {C2_opt:.2f}")
    
    elif secilen_konu == "arz_talep":
        # Arz-talep parametreleri
        col1a, col1b, col1c = st.columns(3)
        with col1a:
            arz_esnek = st.slider("Arz Esnekliği", 0.1, 2.0, 1.0, 0.1)
        with col1b:
            talep_esnek = st.slider("Talep Esnekliği", -2.0, -0.1, -1.0, 0.1)
        with col1c:
            denge_fiyat = st.slider("Denge Fiyatı", 5, 15, 10)
        
        # Grafik oluştur
        fig = arz_talep_grafigi(arz_esnek, talep_esnek, denge_fiyat)
        st.pyplot(fig)

with col2:
    # TEORİ BÖLÜMÜ
    st.subheader("📚 Teori ve Formüller")
    
    # Formül
    st.markdown("**Temel Formül:**")
    st.latex(konu_bilgisi["formul"])
    
    # Teori açıklaması
    st.markdown("**Teorik Açıklama:**")
    st.write(konu_bilgisi["teori"])
    
    # Hızlı bilgiler
    st.subheader("💡 Hızlı Bilgiler")
    
    if secilen_konu == "iki_donemli_tuketici":
        st.info("""
        **Optimum Nokta (P):**
        - Bütçe doğrusu eğimi = Fayda eğrisi eğimi
        - Zaman tercih oranı = Faiz oranı
        """)
        
    elif secilen_konu == "arz_talep":
        st.info("""
        **Denge Özellikleri:**
        - Arz = Talep
        - Piyasa temizlenir
        - Fazla arz/talep olmaz
        """)

# ALT BİLGİ
st.sidebar.markdown("---")
st.sidebar.info("""
**🐍 Mikro Ekonomi Lab v1.0**
- İnteraktif grafikler
- Gerçek zamanlı hesaplamalar
- Teori ve uygulama bir arada
""")

# Hata ayıklama için session state kontrolü
if 'sayac' not in st.session_state:
    st.session_state.sayac = 0