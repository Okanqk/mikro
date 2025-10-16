import matplotlib.pyplot as plt
import numpy as np

def butce_egrisi_ciz(R1=100, R2=80, j12=0.1, C1_opt=60):
    C1_max = R1 + R2/(1+j12)
    C1_degerleri = np.linspace(0, C1_max, 100)
    C2_degerleri = R1*(1+j12) + R2 - (1+j12)*C1_degerleri
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(C1_degerleri, C2_degerleri, 'b-', linewidth=2, label='Bütçe Doğrusu (AB)')
    C2_opt = R1*(1+j12) + R2 - (1+j12)*C1_opt
    ax.scatter(C1_opt, C2_opt, color='red', s=100, label='Optimum Nokta (P)', zorder=5)
    ax.set_xlabel('C₁ - Birinci Dönem Tüketimi', fontsize=12)
    ax.set_ylabel('C₂ - İkinci Dönem Tüketimi', fontsize=12)
    ax.set_title('İki Dönemli Tüketici Modeli', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig

def arz_talep_grafigi(arz_esneklik=1.0, talep_esneklik=-1.0, denge_fiyat=10):
    fiyatlar = np.linspace(0, 20, 100)
    talep_miktar = 100 + talep_esneklik * (fiyatlar - denge_fiyat) * 10
    arz_miktar = 50 + arz_esneklik * (fiyatlar - denge_fiyat) * 10
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(talep_miktar, fiyatlar, 'r-', linewidth=2, label='Talep Eğrisi')
    ax.plot(arz_miktar, fiyatlar, 'g-', linewidth=2, label='Arz Eğrisi')
    ax.scatter(75, denge_fiyat, color='blue', s=100, label='Denge Noktası', zorder=5)
    ax.set_xlabel('Miktar (Q)', fontsize=12)
    ax.set_ylabel('Fiyat (P)', fontsize=12)
    ax.set_title('Arz-Talep Dengesi', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig