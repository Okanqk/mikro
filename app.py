import streamlit as st
import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Sayfa ayarları
st.set_page_config(
    page_title="Mikro Ekonomi Lab",
    page_icon="📈",
    layout="wide"
)

# Session state başlatma
if 'lessons' not in st.session_state:
    st.session_state.lessons = []
if 'tests' not in st.session_state:
    st.session_state.tests = []
if 'notes' not in st.session_state:
    st.session_state.notes = {}
if 'summaries' not in st.session_state:
    st.session_state.summaries = []
if 'selected_lesson' not in st.session_state:
    st.session_state.selected_lesson = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

# GRAFİK ÇİZİM FONKSİYONLARI
def draw_budget_constraint(R1=100, R2=80, j12=0.1):
    """İki dönemli bütçe kısıtı grafiği"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    C1_max = (R1 * (1 + j12) + R2) / (1 + j12)
    C2_max = R1 * (1 + j12) + R2
    
    C1_range = np.linspace(0, C1_max, 100)
    C2_budget = R1 * (1 + j12) + R2 - (1 + j12) * C1_range
    
    ax.plot(C1_range, C2_budget, 'b-', linewidth=2, label='Bütçe Doğrusu (AB)')
    
    C1_indiff = np.linspace(20, C1_max - 20, 100)
    C2_indiff1 = 3000 / C1_indiff
    ax.plot(C1_indiff, C2_indiff1, 'g--', linewidth=1.5, alpha=0.7, label='U¹')
    
    C2_indiff2 = 5000 / C1_indiff
    ax.plot(C1_indiff, C2_indiff2, 'r--', linewidth=1.5, alpha=0.7, label='U²')
    
    ax.plot(R1, R2, 'ko', markersize=10, label=f'Başlangıç (R): ({R1}, {R2})')
    ax.annotate('R', xy=(R1, R2), xytext=(R1+5, R2+5), fontsize=12, fontweight='bold')
    
    C1_opt = C1_max * 0.55
    C2_opt = R1 * (1 + j12) + R2 - (1 + j12) * C1_opt
    ax.plot(C1_opt, C2_opt, 'ro', markersize=12, label=f'Optimum (P): ({C1_opt:.1f}, {C2_opt:.1f})')
    ax.annotate('P', xy=(C1_opt, C2_opt), xytext=(C1_opt+5, C2_opt+5), 
                fontsize=12, fontweight='bold', color='red')
    
    ax.set_xlabel('C₁ (Birinci Dönem Tüketimi)', fontsize=12, fontweight='bold')
    ax.set_ylabel('C₂ (İkinci Dönem Tüketimi)', fontsize=12, fontweight='bold')
    ax.set_title('İki Dönemli Tüketici Optimumu', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    ax.set_xlim(0, C1_max * 1.1)
    ax.set_ylim(0, C2_max * 1.1)
    
    info_text = f'Faiz Oranı (j₁₂): {j12*100:.1f}%\nBütçe Eğimi: -(1+j₁₂) = -{1+j12:.2f}'
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    return fig

def draw_supply_demand(P_eq=10, Q_eq=100):
    """Arz-talep grafiği"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    P_range = np.linspace(0, 20, 100)
    Q_demand = 200 - 10 * P_range
    Q_supply = 10 * P_range
    
    ax.plot(Q_demand, P_range, 'b-', linewidth=2, label='Talep Eğrisi')
    ax.plot(Q_supply, P_range, 'r-', linewidth=2, label='Arz Eğrisi')
    
    ax.plot(Q_eq, P_eq, 'go', markersize=15, label=f'Denge: (Q={Q_eq}, P={P_eq})')
    ax.axhline(y=P_eq, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=Q_eq, color='gray', linestyle='--', alpha=0.5)
    
    ax.set_xlabel('Miktar (Q)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Fiyat (P)', fontsize=12, fontweight='bold')
    ax.set_title('Arz ve Talep Dengesi', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    ax.set_xlim(0, 220)
    ax.set_ylim(0, 22)
    
    return fig

# Demo veri yükleme
if len(st.session_state.lessons) == 0:
    st.session_state.lessons = [
        {
            "unit_number": 1,
            "unit_title": "İki Dönemli Tüketici Modeli",
            "pages": [
                {
                    "page_number": 1,
                    "sections": [
                        {
                            "id": "s1",
                            "type": "text",
                            "content": "İki dönemli tüketici modeli, tüketicinin gelir ve faiz oranları kısıtı altında, bugünkü (C₁) ve gelecekteki (C₂) tüketimi arasındaki tercihlerini eniyilemesini inceler."
                        },
                        {
                            "id": "s2",
                            "type": "formula",
                            "content": r"C_2 = R_1(1+j_{12}) + R_2 - (1+j_{12})C_1"
                        }
                    ]
                },
                {
                    "page_number": 2,
                    "sections": [
                        {
                            "id": "s1",
                            "type": "text",
                            "content": "Tüketici optimumu gösteren (P) noktasında, bütçe doğrusunun eğimi ile zaman kayıtsızlık eğrisinin eğimi birbirine eşittir."
                        },
                        {
                            "id": "s2",
                            "type": "graph",
                            "graph_type": "budget_constraint",
                            "title": "İki Dönemli Optimum Tüketim",
                            "description": "Bütçe doğrusu ve farksızlık eğrileri",
                            "params": {"R1": 100, "R2": 80, "j12": 0.1}
                        }
                    ]
                }
            ]
        },
        {
            "unit_number": 2,
            "unit_title": "Arz ve Talep Analizi",
            "pages": [
                {
                    "page_number": 1,
                    "sections": [
                        {
                            "id": "s1",
                            "type": "text",
                            "content": "Arz ve talep, piyasa ekonomisinin temel dinamiklerini açıklar. Fiyat mekanizması bu iki kuvvetin etkileşimiyle oluşur."
                        },
                        {
                            "id": "s2",
                            "type": "graph",
                            "graph_type": "supply_demand",
                            "title": "Arz ve Talep Dengesi",
                            "description": "Piyasa denge noktası",
                            "params": {"P_eq": 10, "Q_eq": 100}
                        }
                    ]
                }
            ]
        }
    ]
    
    st.session_state.tests = [
        {
            "id": 1,
            "unit": "Ünite 1",
            "questions": [
                {
                    "id": "q1",
                    "type": "multiple",
                    "question": "İki dönemli modelde faiz oranı artarsa bütçe doğrusunun eğimi nasıl değişir?",
                    "options": ["Artar (daha dik)", "Azalır (daha yatık)", "Değişmez", "Belirsiz"],
                    "correct": 0
                }
            ]
        }
    ]

# Üst başlık
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
    <h1 style='color: white; margin: 0;'>📈 Mikro Ekonomi Lab</h1>
    <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;'>İnteraktif Çalışma Platformu</p>
</div>
""", unsafe_allow_html=True)

# Sidebar menü
st.sidebar.title("🎯 Menü")
menu = st.sidebar.radio(
    "Sayfa Seçin:",
    ["📚 Dersler", "🧪 Test & Sorular", "📝 Notlarım", "📊 Özetler", "⚙️ Ayarlar"]
)

# ========================
# DERSLER SAYFASI
# ========================
if menu == "📚 Dersler":
    if st.session_state.selected_lesson is None:
        st.header("📚 Dersler")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("➕ Yeni Sayfa Ekle", type="primary"):
                st.info("JSON formatında sayfa verisi ekleyin (Ayarlar sayfasından)")
        
        st.markdown("---")
        
        # Ünite numarasına göre sırala
        sorted_lessons = sorted(st.session_state.lessons, key=lambda x: x['unit_number'])
        
        for lesson in sorted_lessons:
            with st.container():
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.subheader(f"Ünite {lesson['unit_number']}: {lesson['unit_title']}")
                    st.caption(f"📄 {len(lesson['pages'])} sayfa")
                with col2:
                    if st.button("Aç", key=f"open_unit_{lesson['unit_number']}"):
                        st.session_state.selected_lesson = lesson
                        st.session_state.current_page = 1
                        st.rerun()
                st.markdown("---")
    
    else:
        # Ders detay sayfası
        lesson = st.session_state.selected_lesson
        total_pages = len(lesson['pages'])
        current_page_num = st.session_state.current_page
        
        # Üst navigasyon
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            if st.button("⬅️ Derslere Dön"):
                st.session_state.selected_lesson = None
                st.session_state.current_page = 1
                st.rerun()
        with col2:
            st.markdown(f"### Ünite {lesson['unit_number']}: {lesson['unit_title']}")
        with col3:
            st.markdown(f"**Sayfa {current_page_num}/{total_pages}**")
        
        st.markdown("---")
        
        # Mevcut sayfayı al
        current_page = lesson['pages'][current_page_num - 1]
        
        # Sayfa içeriği
        for idx, section in enumerate(current_page['sections']):
            note_key = f"{lesson['unit_number']}-{current_page_num}-{section['id']}"
            section_notes = st.session_state.notes.get(note_key, [])
            
            # Not görünürlük durumu için unique key
            show_note_state_key = f"show_note_{note_key}"
            
            # Bölüm içeriği
            col1, col2 = st.columns([12, 1])
            
            with col1:
                if section['type'] == 'text':
                    st.markdown(f"{section['content']}")
                
                elif section['type'] == 'formula':
                    st.latex(section['content'])
                
                elif section['type'] == 'graph':
                    st.subheader(f"📊 {section.get('title', 'Grafik')}")
                    st.caption(section.get('description', ''))
                    
                    params = section.get('params', {})
                    graph_type = section.get('graph_type', 'budget_constraint')
                    
                    if graph_type == 'budget_constraint':
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            R1 = st.slider("R₁ - Gelir 1", 50, 200, params.get('R1', 100), key=f"r1_{note_key}")
                        with col_b:
                            R2 = st.slider("R₂ - Gelir 2", 50, 200, params.get('R2', 80), key=f"r2_{note_key}")
                        with col_c:
                            j12 = st.slider("j₁₂ - Faiz", 0.0, 0.5, params.get('j12', 0.1), 0.01, key=f"j12_{note_key}")
                        
                        fig = draw_budget_constraint(R1, R2, j12)
                        st.pyplot(fig)
                        plt.close()
                    
                    elif graph_type == 'supply_demand':
                        col_a, col_b = st.columns(2)
                        with col_a:
                            P_eq = st.slider("Denge Fiyatı (P)", 5, 15, params.get('P_eq', 10), key=f"p_{note_key}")
                        with col_b:
                            Q_eq = st.slider("Denge Miktarı (Q)", 50, 150, params.get('Q_eq', 100), key=f"q_{note_key}")
                        
                        fig = draw_supply_demand(P_eq, Q_eq)
                        st.pyplot(fig)
                        plt.close()
            
            with col2:
                # Not butonu
                note_count = len(section_notes)
                if note_count > 0:
                    button_label = f"📌{note_count}"
                else:
                    button_label = "📝"
                
                # Not butonuna unique key
                if st.button(button_label, key=f"note_toggle_{note_key}"):
                    # Toggle durumunu değiştir
                    if show_note_state_key in st.session_state:
                        st.session_state[show_note_state_key] = not st.session_state[show_note_state_key]
                    else:
                        st.session_state[show_note_state_key] = True
            
            # Not paneli
            if st.session_state.get(show_note_state_key, False):
                with st.container():
                    st.markdown("---")
                    st.markdown("### 💡 Notlar")
                    
                    # Mevcut notları göster
                    if len(section_notes) > 0:
                        for note_idx, note in enumerate(section_notes):
                            col_note, col_del = st.columns([10, 1])
                            with col_note:
                                st.info(f"**{note['date']}**\n\n{note['text']}")
                            with col_del:
                                if st.button("🗑️", key=f"del_note_{note_key}_{note_idx}"):
                                    st.session_state.notes[note_key].pop(note_idx)
                                    st.rerun()
                    
                    # Yeni not ekleme formu - TAM UNIQUE KEY
                    note_form_key = f"form_{note_key}_{current_page_num}_{idx}"
                    note_input_key = f"input_{note_key}_{current_page_num}_{idx}"
                    
                    new_note_text = st.text_area(
                        "Yeni not ekle:", 
                        key=note_input_key,
                        height=100
                    )
                    
                    if st.button("💾 Kaydet", key=f"save_{note_form_key}"):
                        if new_note_text and new_note_text.strip():
                            # Not ekle
                            if note_key not in st.session_state.notes:
                                st.session_state.notes[note_key] = []
                            
                            st.session_state.notes[note_key].append({
                                "id": datetime.now().timestamp(),
                                "text": new_note_text.strip(),
                                "date": datetime.now().strftime("%d.%m.%Y %H:%M")
                            })
                            
                            st.success("✅ Not eklendi!")
                            # Input'u temizlemek için rerun
                            st.rerun()
            
            st.markdown("---")
        
        # Alt navigasyon - Sayfa geçişi
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if current_page_num > 1:
                if st.button("⬅️ Önceki Sayfa", type="secondary", use_container_width=True):
                    st.session_state.current_page -= 1
                    st.rerun()
        
        with col2:
            st.markdown(f"<h4 style='text-align: center;'>Sayfa {current_page_num} / {total_pages}</h4>", unsafe_allow_html=True)
        
        with col3:
            if current_page_num < total_pages:
                if st.button("Sonraki Sayfa ➡️", type="primary", use_container_width=True):
                    st.session_state.current_page += 1
                    st.rerun()

# ========================
# TEST & SORULAR SAYFASI
# ========================
elif menu == "🧪 Test & Sorular":
    st.header("🧪 Test & Sorular")
    
    if 'selected_test' not in st.session_state:
        st.session_state.selected_test = None
    if 'test_answers' not in st.session_state:
        st.session_state.test_answers = {}
    if 'show_test_answers' not in st.session_state:
        st.session_state.show_test_answers = False
    
    if st.session_state.selected_test is None:
        for test in st.session_state.tests:
            with st.container():
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.subheader(test['unit'])
                    st.caption(f"{len(test['questions'])} soru")
                with col2:
                    if st.button("Başla", key=f"test_{test['id']}"):
                        st.session_state.selected_test = test
                        st.session_state.test_answers = {}
                        st.session_state.show_test_answers = False
                        st.rerun()
                st.markdown("---")
    
    else:
        test = st.session_state.selected_test
        
        if st.button("⬅️ Testlere Dön"):
            st.session_state.selected_test = None
            st.rerun()
        
        st.subheader(test['unit'])
        st.markdown("---")
        
        for idx, q in enumerate(test['questions']):
            st.markdown(f"### Soru {idx + 1}")
            st.write(q['question'])
            
            if q['type'] == 'multiple':
                answer = st.radio(
                    "Cevabınız:",
                    options=range(len(q['options'])),
                    format_func=lambda x: q['options'][x],
                    key=f"q_{q['id']}"
                )
                st.session_state.test_answers[q['id']] = answer
                
                if st.session_state.show_test_answers:
                    if answer == q['correct']:
                        st.success("✅ Doğru!")
                    else:
                        st.error(f"❌ Yanlış! Doğru cevap: {q['options'][q['correct']]}")
            
            elif q['type'] == 'classic':
                answer = st.text_area("Cevabınız:", key=f"q_{q['id']}", height=150)
                st.session_state.test_answers[q['id']] = answer
            
            st.markdown("---")
        
        if st.button("👁️ Cevaplara Bak" if not st.session_state.show_test_answers else "🙈 Cevapları Gizle", type="primary"):
            st.session_state.show_test_answers = not st.session_state.show_test_answers
            st.rerun()

# ========================
# NOTLARIM SAYFASI
# ========================
elif menu == "📝 Notlarım":
    st.header("📝 Tüm Notlarım")
    
    all_notes = []
    for key, note_list in st.session_state.notes.items():
        parts = key.split('-')
        unit_num = int(parts[0])
        page_num = int(parts[1])
        
        lesson = next((l for l in st.session_state.lessons if l['unit_number'] == unit_num), None)
        
        for note in note_list:
            all_notes.append({
                **note,
                "unit_title": f"Ünite {unit_num}: {lesson['unit_title']}" if lesson else "Bilinmeyen",
                "page_num": page_num,
                "unit_num": unit_num
            })
    
    if len(all_notes) == 0:
        st.info("Henüz not eklenmemiş. Dersler sayfasından not ekleyebilirsiniz.")
    else:
        # Ünite ve sayfaya göre sırala
        all_notes_sorted = sorted(all_notes, key=lambda x: (x['unit_num'], x['page_num'], -x['id']))
        
        for note in all_notes_sorted:
            with st.container():
                st.markdown(f"**{note['unit_title']} - Sayfa {note['page_num']}** • {note['date']}")
                st.write(note['text'])
                st.markdown("---")

# ========================
# ÖZETLER SAYFASI
# ========================
elif menu == "📊 Özetler":
    st.header("📊 Özetler")
    
    st.info("💡 Claude AI ile oluşturduğunuz özetleri JSON formatında ekleyebilirsiniz.")
    
    json_input = st.text_area(
        "JSON formatında özet ekleyin:",
        height=200,
        placeholder='{"unit": "Ünite 1", "summary": "Özet içeriği..."}'
    )
    
    if st.button("➕ Özet Ekle", type="primary"):
        try:
            summary_data = json.loads(json_input)
            st.session_state.summaries.append(summary_data)
            st.success("Özet başarıyla eklendi!")
            st.rerun()
        except:
            st.error("Hata: Geçerli bir JSON formatı girin.")
    
    st.markdown("---")
    
    for summary in st.session_state.summaries:
        with st.expander(summary.get('unit', 'Özet')):
            st.write(summary.get('summary', ''))

# ========================
# AYARLAR SAYFASI
# ========================
elif menu == "⚙️ Ayarlar":
    st.header("⚙️ Ayarlar")
    
    tab1, tab2, tab3 = st.tabs(["📥 Veri Yükleme", "💾 Veri Yedekleme", "➕ Yeni Sayfa Ekle"])
    
    with tab1:
        st.subheader("📥 JSON Verisi Yükle")
        uploaded_file = st.file_uploader("JSON dosyası seçin:", type=['json'])
        
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                
                if st.button("Verileri Yükle", type="primary"):
                    if 'lessons' in data:
                        st.session_state.lessons = data['lessons']
                    if 'tests' in data:
                        st.session_state.tests = data['tests']
                    if 'notes' in data:
                        st.session_state.notes = data['notes']
                    if 'summaries' in data:
                        st.session_state.summaries = data['summaries']
                    
                    st.success("✅ Veriler başarıyla yüklendi!")
                    st.rerun()
            except:
                st.error("❌ Hata: Geçersiz JSON dosyası!")
    
    with tab2:
        st.subheader("💾 Verileri Yedekle")
        
        backup_data = {
            "lessons": st.session_state.lessons,
            "tests": st.session_state.tests,
            "notes": st.session_state.notes,
            "summaries": st.session_state.summaries,
            "export_date": datetime.now().isoformat()
        }
        
        json_str = json.dumps(backup_data, ensure_ascii=False, indent=2)
        
        st.download_button(
            label="📥 JSON İndir",
            data=json_str,
            file_name=f"mikro_econ_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            type="primary"
        )
        
        total_notes = sum(len(notes) for notes in st.session_state.notes.values())
        st.info(f"📊 İstatistikler:\n- {len(st.session_state.lessons)} Ünite\n- {len(st.session_state.tests)} Test\n- {total_notes} Not\n- {len(st.session_state.summaries)} Özet")
    
    with tab3:
        st.subheader("➕ Yeni Sayfa Ekle")
        
        st.markdown("""
        **JSON Formatı:**
        ```json
        {
          "unit_number": 1,
          "unit_title": "İki Dönemli Tüketici Modeli",
          "page_number": 3,
          "sections": [
            {
              "id": "s1",
              "type": "text",
              "content": "Metin içeriği..."
            }
          ]
        }
        ```
        
        **Not:** Aynı ünite başlığı varsa sayfa o üniteye eklenir, yoksa yeni ünite oluşturulur.
        """)
        
        json_input = st.text_area(
            "JSON verisi girin:",
            height=300,
            placeholder='{"unit_number": 1, "unit_title": "...", "page_number": 2, "sections": [...]}'
        )
        
        if st.button("Sayfa Ekle", type="primary"):
            try:
                new_page_data = json.loads(json_input)
                
                unit_num = new_page_data['unit_number']
                unit_title = new_page_data['unit_title']
                page_num = new_page_data['page_number']
                sections = new_page_data['sections']
                
                # Ünite var mı kontrol et
                existing_unit = next((l for l in st.session_state.lessons if l['unit_number'] == unit_num), None)
                
                if existing_unit:
                    # Mevcut üniteye sayfa ekle
                    existing_unit['pages'].append({
                        "page_number": page_num,
                        "sections": sections
                    })
                    # Sayfa numarasına göre sırala
                    existing_unit['pages'].sort(key=lambda x: x['page_number'])
                    st.success(f"✅ Sayfa {page_num}, Ünite {unit_num}'e eklendi!")
                else:
                    # Yeni ünite oluştur
                    st.session_state.lessons.append({
                        "unit_number": unit_num,
                        "unit_title": unit_title,
                        "pages": [
                            {
                                "page_number": page_num,
                                "sections": sections
                            }
                        ]
                    })
                    st.success(f"✅ Yeni ünite ({unit_num}) ve sayfa ({page_num}) eklendi!")
                
                st.rerun()
            except Exception as e:
                st.error(f"❌ Geçersiz JSON formatı! Hata: {str(e)}")

# Footer
st.sidebar.markdown("---")
total_pages = sum(len(lesson['pages']) for lesson in st.session_state.lessons)
total_notes = sum(len(notes) for notes in st.session_state.notes.values())
st.sidebar.info(f"""
**📈 Mikro Ekonomi Lab v3.0**  
✅ {len(st.session_state.lessons)} Ünite  
✅ {total_pages} Sayfa  
✅ {total_notes} Not
""")
