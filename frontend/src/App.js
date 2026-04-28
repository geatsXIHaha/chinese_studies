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
    };
    localStorage.setItem('paperTabsState', JSON.stringify(state));
  }, [openPapers, activePaperId, currentView, showUploadTab, selectedPaper, tabsRestored]);

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
            <PaperViewer paper={activePaper} userId={userId} />
          )}

          {currentView === 'writing' && activePaper && (
            <WritingAssistant paper={activePaper} userId={userId} />
          )}

          {currentView === 'quotes' && (
            <QuoteFinder />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
