/**
 * Main App Component
 */
import React, { useEffect, useState } from 'react';
import { SearchPaper, PaperViewer, WritingAssistant, QuoteFinder } from './components';
import './styles/App.css';
import './styles/index.css';

function App() {
  const [currentView, setCurrentView] = useState('search');
  const [selectedPaper, setSelectedPaper] = useState(null);
  const [openPapers, setOpenPapers] = useState([]);
  const [activePaperId, setActivePaperId] = useState(null);
  const userId = 'demo-user'; // In production, this would come from auth
  const [showUploadTab, setShowUploadTab] = useState(false);
  const [tabsRestored, setTabsRestored] = useState(false);
  const [notes, setNotes] = useState([]);

  useEffect(() => {
    const saved = localStorage.getItem('paperTabsState');
    if (!saved) return;
    try {
      const state = JSON.parse(saved);
      if (Array.isArray(state.openPapers)) {
        setOpenPapers(state.openPapers);
      }
      if (state.activePaperId) {
        setActivePaperId(state.activePaperId);
      }
      if (state.currentView) {
        setCurrentView(state.currentView);
      }
      if (state.showUploadTab) {
        setShowUploadTab(true);
      }
      if (state.selectedPaper) {
        setSelectedPaper(state.selectedPaper);
      }
      if (Array.isArray(state.notes)) {
        setNotes(state.notes);
      }
    } catch (error) {
      console.warn('Failed to restore tabs state', error);
    }
    setTabsRestored(true);
  }, []);

  useEffect(() => {
    if (!tabsRestored) return;
    const state = {
      openPapers,
      activePaperId,
      currentView,
      showUploadTab,
      selectedPaper,
      notes,
    };
    localStorage.setItem('paperTabsState', JSON.stringify(state));
  }, [openPapers, activePaperId, currentView, showUploadTab, selectedPaper, notes, tabsRestored]);

  const handleSaveNote = (note) => {
    setNotes((prev) => [{ ...note, id: `${note.sourceId}-${Date.now()}` }, ...prev]);
  };

  const handleDeleteNote = (noteId) => {
    setNotes((prev) => prev.filter((note) => note.id !== noteId));
  };

  const handleSelectPaper = (paper) => {
    setSelectedPaper(paper);
    setCurrentView('paper');
    setOpenPapers((prev) => {
      if (prev.some((p) => p.id === paper.id)) {
        return prev;
      }
      return [...prev, paper];
    });
    setActivePaperId(paper.id);
  };

  const handleCloseTab = (paperId) => {
    setOpenPapers((prev) => prev.filter((paper) => paper.id !== paperId));
    setShowUploadTab(false);
    if (activePaperId === paperId) {
      const remaining = openPapers.filter((paper) => paper.id !== paperId);
      if (remaining.length > 0) {
        setActivePaperId(remaining[remaining.length - 1].id);
      } else {
        setActivePaperId(null);
        setSelectedPaper(null);
        setCurrentView('search');
      }
    }
  };

  const activePaper =
    openPapers.find((paper) => paper.id === activePaperId) || selectedPaper;

  return (
    <div className="app">
      <header className="app-header">
        <h1>📚 Chinese Academic AI Study System</h1>
        <p>智能学术论文分析与写作辅助平台</p>
      </header>

      <div className="app-container">
        <nav className="app-nav">
          <button
            className={`nav-btn ${currentView === 'search' ? 'active' : ''}`}
            onClick={() => setCurrentView('search')}
          >
            🔍 搜索论文
          </button>
          {selectedPaper && (
            <>
              <button
                className={`nav-btn ${currentView === 'paper' ? 'active' : ''}`}
                onClick={() => setCurrentView('paper')}
              >
                📄 论文查看
              </button>
              <button
                className={`nav-btn ${currentView === 'writing' ? 'active' : ''}`}
                onClick={() => setCurrentView('writing')}
              >
                ✨ 写作助手
              </button>
            </>
          )}
          <button
            className={`nav-btn ${currentView === 'quotes' ? 'active' : ''}`}
            onClick={() => setCurrentView('quotes')}
          >
            📚 名句溯源
          </button>
          <button
            className={`nav-btn ${currentView === 'notes' ? 'active' : ''}`}
            onClick={() => setCurrentView('notes')}
          >
            🗒️ 笔记
          </button>
        </nav>

        {(openPapers.length > 0 || showUploadTab) && (
          <div className="paper-tabs">
            {openPapers.map((paper) => (
              <div
                key={paper.id}
                className={`paper-tab ${activePaperId === paper.id ? 'active' : ''}`}
              >
                <button
                  className="paper-tab-title"
                  onClick={() => {
                    setActivePaperId(paper.id);
                    setCurrentView('paper');
                  }}
                >
                  {paper.title}
                </button>
                <button
                  className="paper-tab-close"
                  onClick={() => handleCloseTab(paper.id)}
                  aria-label="Close tab"
                >
                  ✕
                </button>
              </div>
            ))}
            {showUploadTab && (
              <div className="paper-tab active">
                <button className="paper-tab-title" onClick={() => setCurrentView('search')}>
                  上传 PDF
                </button>
                <button
                  className="paper-tab-close"
                  onClick={() => setShowUploadTab(false)}
                  aria-label="Close upload tab"
                >
                  ✕
                </button>
              </div>
            )}
            <button
              className="paper-tab-add"
              onClick={() => {
                setShowUploadTab(true);
                setCurrentView('search');
              }}
            >
              ＋ 新建
            </button>
          </div>
        )}

        <div className="app-content">
          {currentView === 'search' && (
            <SearchPaper onSelectPaper={handleSelectPaper} />
          )}

          {currentView === 'paper' && activePaper && (
            <PaperViewer paper={activePaper} userId={userId} onSaveNote={handleSaveNote} />
          )}

          {currentView === 'writing' && activePaper && (
            <WritingAssistant paper={activePaper} userId={userId} />
          )}

          {currentView === 'quotes' && (
            <QuoteFinder />
          )}

          {currentView === 'notes' && (
            <div className="notes-page">
              <h2>我的笔记</h2>
              {notes.length === 0 ? (
                <p className="no-results">暂无笔记</p>
              ) : (
                <div className="notes-page-list">
                  {notes.map((note) => (
                    <div key={note.id} className="note-card">
                      <p className="note-text">"{note.text}"</p>
                      <span className="note-source">来源: {note.sourceTitle}</span>
                      <button className="note-delete" onClick={() => handleDeleteNote(note.id)}>
                        删除
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
