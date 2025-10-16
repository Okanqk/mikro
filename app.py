import streamlit as st
import json
from datetime import datetime

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

# Demo veri yükleme
if len(st.session_state.lessons) == 0:
    st.session_state.lessons = [
        {
            "id": 1,
            "title": "Ünite 1: İki Dönemli Tüketici Modeli",
            "content": {
                "sections": [
                    {
                        "id": "s1",
                        "type": "text",
                        "content": "İki dönemli tüketici modeli, tüketicilerin bugün ve gelecekte tüketim kararlarını nasıl verdiklerini analiz eder."
                    },
                    {
                        "id": "s2",
                        "type": "formula",
                        "content": r"C_2 = R_1(1+j_{12}) + R_2 - (1+j_{12})C_1"
                    },
                    {
                        "id": "s3",
                        "type": "text",
                        "content": "Bu modelde tüketici iki dönem için optimizasyon yapar. Birinci dönem geliri R₁, ikinci dönem geliri R₂'dir."
                    }
                ]
            }
        },
        {
            "id": 2,
            "title": "Ünite 2: Arz ve Talep Analizi",
            "content": {
                "sections": [
                    {
                        "id": "s1",
                        "type": "text",
                        "content": "Arz ve talep, piyasa ekonomisinin temel dinamiklerini açıklar."
                    }
                ]
            }
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
                },
                {
                    "id": "q2",
                    "type": "classic",
                    "question": "İki dönemli tüketici modelinde optimum noktanın şartlarını açıklayın."
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
            if st.button("➕ Yeni Ünite Ekle", type="primary"):
                st.info("JSON formatında ünite verisi ekleyin (Ayarlar sayfasından)")
        
        st.markdown("---")
        
        for lesson in st.session_state.lessons:
            with st.container():
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.subheader(lesson['title'])
                    st.caption(f"{len(lesson['content']['sections'])} bölüm")
                with col2:
                    if st.button("Aç", key=f"open_{lesson['id']}"):
                        st.session_state.selected_lesson = lesson
                        st.rerun()
                st.markdown("---")
    
    else:
        # Ders detay sayfası
        lesson = st.session_state.selected_lesson
        
        if st.button("⬅️ Derslere Dön"):
            st.session_state.selected_lesson = None
            st.rerun()
        
        st.header(lesson['title'])
        st.markdown("---")
        
        # Her bölüm için
        for idx, section in enumerate(lesson['content']['sections']):
            note_key = f"{lesson['id']}-{section['id']}"
            section_notes = st.session_state.notes.get(note_key, [])
            
            # Bölüm içeriği
            col1, col2 = st.columns([12, 1])
            
            with col1:
                if section['type'] == 'text':
                    st.markdown(f"**{section['content']}**")
                
                elif section['type'] == 'formula':
                    st.latex(section['content'])
                
                elif section['type'] == 'graph':
                    st.info(f"📊 **{section['content'].get('title', 'Grafik')}**")
                    st.caption(section['content'].get('description', ''))
            
            with col2:
                # Not butonu
                note_count = len(section_notes)
                if note_count > 0:
                    button_label = f"📌 {note_count}"
                else:
                    button_label = "📝"
                
                if st.button(button_label, key=f"note_btn_{note_key}"):
                    st.session_state[f"show_note_{note_key}"] = not st.session_state.get(f"show_note_{note_key}", False)
            
            # Not paneli
            if st.session_state.get(f"show_note_{note_key}", False):
                with st.expander("💡 Notlar", expanded=True):
                    # Mevcut notları göster
                    for note in section_notes:
                        st.info(f"**{note['date']}**\n\n{note['text']}")
                    
                    # Yeni not ekle
                    with st.form(key=f"note_form_{note_key}"):
                        new_note = st.text_area("Yeni not ekle:", key=f"note_input_{note_key}")
                        submitted = st.form_submit_button("💾 Kaydet")
                        
                        if submitted and new_note.strip():
                            if note_key not in st.session_state.notes:
                                st.session_state.notes[note_key] = []
                            
                            st.session_state.notes[note_key].append({
                                "id": datetime.now().timestamp(),
                                "text": new_note,
                                "date": datetime.now().strftime("%d.%m.%Y %H:%M")
                            })
                            st.success("Not eklendi!")
                            st.rerun()
            
            st.markdown("---")

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
        
        # Sorular
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
        
        # Cevapları göster butonu
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
        lesson_id, section_id = key.split('-')
        lesson = next((l for l in st.session_state.lessons if l['id'] == int(lesson_id)), None)
        
        for note in note_list:
            all_notes.append({
                **note,
                "lesson_title": lesson['title'] if lesson else "Bilinmeyen",
                "section_id": section_id
            })
    
    if len(all_notes) == 0:
        st.info("Henüz not eklenmemiş. Dersler sayfasından not ekleyebilirsiniz.")
    else:
        for note in sorted(all_notes, key=lambda x: x['id'], reverse=True):
            with st.container():
                st.markdown(f"**{note['lesson_title']}** • {note['date']}")
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
    
    # Özetleri göster
    for summary in st.session_state.summaries:
        with st.expander(summary.get('unit', 'Özet')):
            st.write(summary.get('summary', ''))

# ========================
# AYARLAR SAYFASI
# ========================
elif menu == "⚙️ Ayarlar":
    st.header("⚙️ Ayarlar")
    
    tab1, tab2, tab3 = st.tabs(["📥 Veri Yükleme", "💾 Veri Yedekleme", "➕ Yeni Veri Ekle"])
    
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
        
        st.info(f"📊 İstatistikler:\n- {len(st.session_state.lessons)} Ünite\n- {len(st.session_state.tests)} Test\n- {len(st.session_state.notes)} Not Grubu\n- {len(st.session_state.summaries)} Özet")
    
    with tab3:
        st.subheader("➕ Yeni Ünite/Test Ekle")
        
        data_type = st.radio("Veri Tipi:", ["Ünite", "Test"])
        
        json_input = st.text_area(
            "JSON verisi girin:",
            height=300,
            placeholder='{"id": 3, "title": "Ünite 3: ...", "content": {...}}'
        )
        
        if st.button("Ekle", type="primary"):
            try:
                new_data = json.loads(json_input)
                
                if data_type == "Ünite":
                    st.session_state.lessons.append(new_data)
                    st.success("✅ Ünite eklendi!")
                else:
                    st.session_state.tests.append(new_data)
                    st.success("✅ Test eklendi!")
                
                st.rerun()
            except:
                st.error("❌ Geçersiz JSON formatı!")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
**📈 Mikro Ekonomi Lab v2.0**  
Gelişmiş çalışma platformu
""")
