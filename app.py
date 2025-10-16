import React, { useState, useEffect } from 'react';
import { Book, FileText, TestTube, StickyNote, FileStack, Settings, Plus, Save, Download, Upload, Eye, EyeOff, ChevronRight, Check, X, BookOpen, Zap } from 'lucide-react';

// Ana Uygulama Bileşeni
export default function MicroEconApp() {
  const [activeTab, setActiveTab] = useState('lessons');
  const [lessons, setLessons] = useState([]);
  const [tests, setTests] = useState([]);
  const [summaries, setSummaries] = useState([]);
  const [notes, setNotes] = useState({});
  const [selectedLesson, setSelectedLesson] = useState(null);
  
  // Demo veri
  useEffect(() => {
    const demoLessons = [
      {
        id: 1,
        title: "Ünite 1: İki Dönemli Tüketici Modeli",
        content: {
          sections: [
            {
              id: "s1",
              type: "text",
              content: "İki dönemli tüketici modeli, tüketicilerin bugün ve gelecekte tüketim kararlarını nasıl verdiklerini analiz eder."
            },
            {
              id: "s2",
              type: "formula",
              content: "C_2 = R_1(1+j_{12}) + R_2 - (1+j_{12})C_1"
            },
            {
              id: "s3",
              type: "text",
              content: "Bu modelde tüketici iki dönem için optimizasyon yapar. Birinci dönem geliri R₁, ikinci dönem geliri R₂'dir."
            },
            {
              id: "s4",
              type: "graph",
              content: {
                title: "Bütçe Kısıtı Eğrisi",
                description: "İki dönem arası tüketim seçeneklerini gösterir"
              }
            }
          ]
        }
      },
      {
        id: 2,
        title: "Ünite 2: Arz ve Talep Analizi",
        content: {
          sections: [
            {
              id: "s1",
              type: "text",
              content: "Arz ve talep, piyasa ekonomisinin temel dinamiklerini açıklar. Fiyat mekanizması bu iki kuvvetin etkileşimiyle oluşur."
            },
            {
              id: "s2",
              type: "formula",
              content: "Q_d = Q_s \\text{ (Denge)}"
            },
            {
              id: "s3",
              type: "text",
              content: "Talep eğrisi negatif eğimli, arz eğrisi pozitif eğimlidir. Kesişim noktası denge fiyatını belirler."
            }
          ]
        }
      }
    ];
    
    const demoTests = [
      {
        id: 1,
        unit: "Ünite 1",
        questions: [
          {
            id: "q1",
            type: "multiple",
            question: "İki dönemli modelde faiz oranı artarsa bütçe doğrusunun eğimi nasıl değişir?",
            options: ["Artar (daha dik)", "Azalır (daha yatık)", "Değişmez", "Belirsiz"],
            correct: 0
          },
          {
            id: "q2",
            type: "classic",
            question: "İki dönemli tüketici modelinde optimum noktanın şartlarını açıklayın."
          }
        ]
      }
    ];
    
    setLessons(demoLessons);
    setTests(demoTests);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Üst Başlık */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-indigo-600 p-2 rounded-lg">
                <BookOpen className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-800">Mikro Ekonomi Lab</h1>
                <p className="text-sm text-gray-600">İnteraktif Çalışma Platformu</p>
              </div>
            </div>
            <div className="flex gap-2">
              <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
                {lessons.length} Ünite
              </span>
              <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                {Object.keys(notes).length} Not
              </span>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="flex gap-6">
          {/* Sol Menü */}
          <aside className="w-64 bg-white rounded-xl shadow-md p-4 h-fit sticky top-6">
            <nav className="space-y-2">
              <NavButton icon={Book} label="Dersler" active={activeTab === 'lessons'} onClick={() => setActiveTab('lessons')} />
              <NavButton icon={TestTube} label="Test & Sorular" active={activeTab === 'tests'} onClick={() => setActiveTab('tests')} />
              <NavButton icon={StickyNote} label="Notlarım" active={activeTab === 'notes'} onClick={() => setActiveTab('notes')} />
              <NavButton icon={FileStack} label="Özetler" active={activeTab === 'summaries'} onClick={() => setActiveTab('summaries')} />
              <NavButton icon={Settings} label="Ayarlar" active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} />
            </nav>
          </aside>

          {/* Ana İçerik */}
          <main className="flex-1">
            {activeTab === 'lessons' && <LessonsPage lessons={lessons} notes={notes} setNotes={setNotes} selectedLesson={selectedLesson} setSelectedLesson={setSelectedLesson} />}
            {activeTab === 'tests' && <TestsPage tests={tests} />}
            {activeTab === 'notes' && <NotesPage notes={notes} lessons={lessons} />}
            {activeTab === 'summaries' && <SummariesPage summaries={summaries} setSummaries={setSummaries} />}
            {activeTab === 'settings' && <SettingsPage lessons={lessons} setLessons={setLessons} tests={tests} setTests={setTests} notes={notes} setNotes={setNotes} />}
          </main>
        </div>
      </div>
    </div>
  );
}

// Navigasyon Butonu
function NavButton({ icon: Icon, label, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
        active 
          ? 'bg-indigo-600 text-white shadow-md' 
          : 'text-gray-700 hover:bg-gray-100'
      }`}
    >
      <Icon className="w-5 h-5" />
      <span className="font-medium">{label}</span>
    </button>
  );
}

// DERSLER SAYFASI
function LessonsPage({ lessons, notes, setNotes, selectedLesson, setSelectedLesson }) {
  const [expandedNote, setExpandedNote] = useState(null);
  const [noteInput, setNoteInput] = useState('');

  const handleAddNote = (lessonId, sectionId) => {
    if (!noteInput.trim()) return;
    
    const noteKey = `${lessonId}-${sectionId}`;
    setNotes(prev => ({
      ...prev,
      [noteKey]: [...(prev[noteKey] || []), {
        id: Date.now(),
        text: noteInput,
        date: new Date().toLocaleString('tr-TR')
      }]
    }));
    setNoteInput('');
    setExpandedNote(null);
  };

  if (!selectedLesson) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Dersler</h2>
          <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
            <Plus className="w-4 h-4" />
            Yeni Ünite Ekle
          </button>
        </div>
        
        <div className="grid gap-4">
          {lessons.map(lesson => (
            <div
              key={lesson.id}
              onClick={() => setSelectedLesson(lesson)}
              className="p-6 border-2 border-gray-200 rounded-xl hover:border-indigo-400 hover:shadow-lg transition cursor-pointer group"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="bg-indigo-100 p-3 rounded-lg group-hover:bg-indigo-200 transition">
                    <Book className="w-6 h-6 text-indigo-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-800">{lesson.title}</h3>
                    <p className="text-sm text-gray-600">{lesson.content.sections.length} bölüm</p>
                  </div>
                </div>
                <ChevronRight className="w-6 h-6 text-gray-400 group-hover:text-indigo-600 transition" />
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-md">
      <div className="p-6 border-b border-gray-200">
        <button
          onClick={() => setSelectedLesson(null)}
          className="text-indigo-600 hover:text-indigo-700 mb-4 flex items-center gap-2"
        >
          ← Derslere Dön
        </button>
        <h2 className="text-2xl font-bold text-gray-800">{selectedLesson.title}</h2>
      </div>
      
      <div className="p-6 space-y-6">
        {selectedLesson.content.sections.map((section, idx) => {
          const noteKey = `${selectedLesson.id}-${section.id}`;
          const sectionNotes = notes[noteKey] || [];
          const isNoteExpanded = expandedNote === noteKey;
          
          return (
            <div key={section.id} className="relative group">
              {/* Not Butonu */}
              <button
                onClick={() => setExpandedNote(isNoteExpanded ? null : noteKey)}
                className="absolute -left-12 top-2 w-8 h-8 bg-yellow-400 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 hover:bg-yellow-500 transition-all shadow-md"
                title="Not ekle"
              >
                <StickyNote className="w-4 h-4 text-yellow-900" />
                {sectionNotes.length > 0 && (
                  <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">
                    {sectionNotes.length}
                  </span>
                )}
              </button>

              {/* İçerik */}
              <div className="pl-2">
                {section.type === 'text' && (
                  <p className="text-gray-700 leading-relaxed">{section.content}</p>
                )}
                
                {section.type === 'formula' && (
                  <div className="bg-indigo-50 p-4 rounded-lg border-l-4 border-indigo-600">
                    <code className="text-indigo-900 font-mono">{section.content}</code>
                  </div>
                )}
                
                {section.type === 'graph' && (
                  <div className="bg-gray-50 p-6 rounded-lg border-2 border-dashed border-gray-300">
                    <div className="flex items-center gap-3 mb-2">
                      <Zap className="w-5 h-5 text-yellow-600" />
                      <h4 className="font-bold text-gray-800">{section.content.title}</h4>
                    </div>
                    <p className="text-sm text-gray-600">{section.content.description}</p>
                    <div className="mt-4 h-48 bg-white rounded flex items-center justify-center">
                      <span className="text-gray-400">Grafik Alanı</span>
                    </div>
                  </div>
                )}
              </div>

              {/* Not Paneli */}
              {isNoteExpanded && (
                <div className="mt-4 ml-2 p-4 bg-yellow-50 rounded-lg border-l-4 border-yellow-400">
                  <h4 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                    <StickyNote className="w-4 h-4" />
                    Notlar
                  </h4>
                  
                  {sectionNotes.map(note => (
                    <div key={note.id} className="bg-white p-3 rounded mb-2 border border-yellow-200">
                      <p className="text-sm text-gray-700">{note.text}</p>
                      <p className="text-xs text-gray-500 mt-1">{note.date}</p>
                    </div>
                  ))}
                  
                  <div className="flex gap-2 mt-3">
                    <input
                      type="text"
                      value={noteInput}
                      onChange={(e) => setNoteInput(e.target.value)}
                      placeholder="Notunuzu yazın..."
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400"
                      onKeyPress={(e) => e.key === 'Enter' && handleAddNote(selectedLesson.id, section.id)}
                    />
                    <button
                      onClick={() => handleAddNote(selectedLesson.id, section.id)}
                      className="px-4 py-2 bg-yellow-400 text-yellow-900 rounded-lg hover:bg-yellow-500 transition"
                    >
                      <Save className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

// TESTLER SAYFASI
function TestsPage({ tests }) {
  const [selectedTest, setSelectedTest] = useState(null);
  const [answers, setAnswers] = useState({});
  const [showAnswers, setShowAnswers] = useState(false);

  if (!selectedTest) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Test & Sorular</h2>
        <div className="grid gap-4">
          {tests.map(test => (
            <div
              key={test.id}
              onClick={() => setSelectedTest(test)}
              className="p-6 border-2 border-gray-200 rounded-xl hover:border-indigo-400 hover:shadow-lg transition cursor-pointer"
            >
              <h3 className="text-lg font-bold text-gray-800">{test.unit}</h3>
              <p className="text-sm text-gray-600">{test.questions.length} soru</p>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <button
        onClick={() => { setSelectedTest(null); setAnswers({}); setShowAnswers(false); }}
        className="text-indigo-600 hover:text-indigo-700 mb-4"
      >
        ← Testlere Dön
      </button>
      
      <h2 className="text-2xl font-bold text-gray-800 mb-6">{selectedTest.unit}</h2>
      
      <div className="space-y-6">
        {selectedTest.questions.map((q, idx) => (
          <div key={q.id} className="p-6 bg-gray-50 rounded-xl">
            <div className="flex items-start gap-3 mb-4">
              <span className="bg-indigo-600 text-white px-3 py-1 rounded-full font-bold">
                {idx + 1}
              </span>
              <p className="flex-1 text-gray-800 font-medium">{q.question}</p>
            </div>
            
            {q.type === 'multiple' && (
              <div className="space-y-2 ml-12">
                {q.options.map((opt, optIdx) => (
                  <label key={optIdx} className="flex items-center gap-3 p-3 bg-white rounded-lg hover:bg-indigo-50 cursor-pointer transition">
                    <input
                      type="radio"
                      name={q.id}
                      checked={answers[q.id] === optIdx}
                      onChange={() => setAnswers(prev => ({ ...prev, [q.id]: optIdx }))}
                      className="w-4 h-4"
                    />
                    <span className={showAnswers && optIdx === q.correct ? 'text-green-600 font-bold' : ''}>
                      {opt}
                    </span>
                    {showAnswers && optIdx === q.correct && <Check className="w-5 h-5 text-green-600 ml-auto" />}
                    {showAnswers && answers[q.id] === optIdx && optIdx !== q.correct && <X className="w-5 h-5 text-red-600 ml-auto" />}
                  </label>
                ))}
              </div>
            )}
            
            {q.type === 'classic' && (
              <textarea
                className="w-full ml-12 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
                rows="4"
                placeholder="Cevabınızı yazın..."
                value={answers[q.id] || ''}
                onChange={(e) => setAnswers(prev => ({ ...prev, [q.id]: e.target.value }))}
              />
            )}
          </div>
        ))}
      </div>
      
      <button
        onClick={() => setShowAnswers(!showAnswers)}
        className="mt-6 w-full py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-bold flex items-center justify-center gap-2"
      >
        {showAnswers ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
        {showAnswers ? 'Cevapları Gizle' : 'Cevaplara Bak'}
      </button>
    </div>
  );
}

// NOTLAR SAYFASI
function NotesPage({ notes, lessons }) {
  const allNotes = Object.entries(notes).flatMap(([key, noteList]) => {
    const [lessonId, sectionId] = key.split('-');
    const lesson = lessons.find(l => l.id === parseInt(lessonId));
    return noteList.map(note => ({
      ...note,
      lessonTitle: lesson?.title || 'Bilinmeyen',
      sectionId
    }));
  });

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Tüm Notlarım</h2>
      
      {allNotes.length === 0 ? (
        <div className="text-center py-12">
          <StickyNote className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500">Henüz not eklenmemiş</p>
        </div>
      ) : (
        <div className="space-y-4">
          {allNotes.map(note => (
            <div key={note.id} className="p-4 bg-yellow-50 rounded-lg border-l-4 border-yellow-400">
              <div className="flex items-start justify-between mb-2">
                <span className="text-xs font-bold text-indigo-600">{note.lessonTitle}</span>
                <span className="text-xs text-gray-500">{note.date}</span>
              </div>
              <p className="text-gray-700">{note.text}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ÖZETLER SAYFASI
function SummariesPage({ summaries, setSummaries }) {
  const [newSummary, setNewSummary] = useState('');
  
  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Özetler</h2>
      
      <div className="mb-6 p-4 bg-blue-50 rounded-lg">
        <p className="text-sm text-blue-800">
          <strong>Not:</strong> Claude AI ile oluşturduğunuz özetleri JSON formatında buraya ekleyebilirsiniz.
        </p>
      </div>
      
      <textarea
        className="w-full p-4 border-2 border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        rows="6"
        placeholder='{"unit": "Ünite 1", "summary": "..."}'
        value={newSummary}
        onChange={(e) => setNewSummary(e.target.value)}
      />
      
      <button className="w-full py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
        Özet Ekle
      </button>
    </div>
  );
}

// AYARLAR SAYFASI
function SettingsPage({ lessons, setLessons, tests, setTests, notes, setNotes }) {
  const handleExport = () => {
    const data = {
      lessons,
      tests,
      notes,
      exportDate: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `mikro-econ-backup-${Date.now()}.json`;
    a.click();
  };

  const handleImport = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const data = JSON.parse(event.target.result);
        if (data.lessons) setLessons(data.lessons);
        if (data.tests) setTests(data.tests);
        if (data.notes) setNotes(data.notes);
        alert('Veriler başarıyla yüklendi!');
      } catch (error) {
        alert('Hata: Geçersiz dosya formatı');
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Ayarlar</h2>
      
      <div className="space-y-6">
        <div className="p-6 border-2 border-gray-200 rounded-xl">
          <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Download className="w-5 h-5" />
            Veri Yedekleme
          </h3>
          <p className="text-gray-600 mb-4">Tüm verilerinizi JSON dosyası olarak indirin</p>
          <button
            onClick={handleExport}
            className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
          >
            Verileri İndir (JSON)
          </button>
        </div>
        
        <div className="p-6 border-2 border-gray-200 rounded-xl">
          <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Upload className="w-5 h-5" />
            Veri Yükleme
          </h3>
          <p className="text-gray-600 mb-4">Daha önce indirdiğiniz JSON dosyasını yükleyin</p>
          <input
            type="file"
            accept=".json"
            onChange={handleImport}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-indigo-600 file:text-white hover:file:bg-indigo-700"
          />
        </div>
      </div>
    </div>
  );
}
