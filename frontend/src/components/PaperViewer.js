/**
 * Paper Viewer Component with highlighting and AI explanations
 */
import React, { useMemo, useState, useRef, useEffect } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import { highlightAPI, API_ORIGIN } from '../utils/api';
import '../styles/PaperViewer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';

pdfjs.GlobalWorkerOptions.workerSrc = `${process.env.PUBLIC_URL}/pdf.worker.min.mjs`;

export const PaperViewer = ({ paper, userId = 'default-user' }) => {
  const [highlights, setHighlights] = useState([]);
  const [selectedText, setSelectedText] = useState('');
  const [explanation, setExplanation] = useState(null);
  const [loadingExplanation, setLoadingExplanation] = useState(false);
  const [translation, setTranslation] = useState('');
  const [loadingTranslation, setLoadingTranslation] = useState(false);
  const [notes, setNotes] = useState([]);
  const paperContentRef = useRef(null);
  const [showExplanationPanel, setShowExplanationPanel] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [popupPosition, setPopupPosition] = useState({ x: 0, y: 0 });
  const [pdfPages, setPdfPages] = useState(0);
  const [pdfWidth, setPdfWidth] = useState(800);
  const pdfContainerRef = useRef(null);
  const pdfOptions = useMemo(
    () => ({
      disableRange: true,
      disableStream: true,
    }),
    []
  );

  useEffect(() => {
    // Load highlights for this paper
    const loadHighlights = async () => {
      try {
        const response = await highlightAPI.getForPaper(paper.id, userId);
        setHighlights(response.data);
      } catch (error) {
        console.error('Error loading highlights:', error);
      }
    };
    loadHighlights();
  }, [paper.id, userId]);

  useEffect(() => {
    const updateWidth = () => {
      if (!pdfContainerRef.current) return;
      setPdfWidth(pdfContainerRef.current.clientWidth);
    };

    updateWidth();
    window.addEventListener('resize', updateWidth);
    return () => window.removeEventListener('resize', updateWidth);
  }, [paper.id]);

  const handleTextSelection = async () => {
    const selection = window.getSelection();
    if (!selection || selection.toString().length === 0) {
      setShowPopup(false);
      return;
    }

    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    setSelectedText(selection.toString());
    setPopupPosition({
      x: rect.left + rect.width / 2,
      y: rect.top - 8,
    });
    setShowPopup(true);
    setShowExplanationPanel(false);
    setTranslation('');
  };

  const handleExplainText = async () => {
    if (!selectedText) return;

    setLoadingExplanation(true);
    try {
      const response = await highlightAPI.explain(selectedText);
      setExplanation(response.data);
      setShowExplanationPanel(true);
    } catch (error) {
      console.error('Error getting explanation:', error);
      setExplanation(null);
    } finally {
      setLoadingExplanation(false);
    }
  };

  const handleTranslateText = async () => {
    if (!selectedText) return;

    setLoadingTranslation(true);
    try {
      const response = await highlightAPI.translate(selectedText, 'en');
      setTranslation(response.data.translated_text);
    } catch (error) {
      console.error('Error translating text:', error);
      setTranslation('');
    } finally {
      setLoadingTranslation(false);
    }
  };

  const handleSaveNote = () => {
    if (!selectedText) return;
    setNotes((prev) => [
      { id: `${paper.id}-${Date.now()}`, text: selectedText },
      ...prev,
    ]);
    setShowPopup(false);
  };

  const handleMarkHighlight = () => {
    if (!selectedText) return;
    try {
      const selection = window.getSelection();
      if (!selection || selection.rangeCount === 0) return;
      const range = selection.getRangeAt(0);
      const mark = document.createElement('mark');
      mark.className = 'inline-highlight';
      range.surroundContents(mark);
      selection.removeAllRanges();
    } catch (error) {
      console.error('Highlight error:', error);
    }
    setShowPopup(false);
  };

  return (
    <div className="paper-viewer">
      <div className="paper-header">
        <h2>{paper.title}</h2>
        <p className="paper-meta">
          <span>作者: {paper.authors}</span>
          <span>发布日期: {new Date(paper.publication_date).toLocaleDateString('zh-CN')}</span>
        </p>
      </div>

      <div className="paper-content" ref={paperContentRef} onMouseUp={handleTextSelection}>
        <div className="abstract-section">
          <h3>摘要</h3>
          <p>{paper.abstract}</p>
        </div>

        <div className="full-text-section">
          <h3>全文</h3>
          {paper.source_url ? (
            <div className="pdf-viewer" ref={pdfContainerRef}>
              <Document
                file={paper.source_url.startsWith('http') ? paper.source_url : `${API_ORIGIN}${paper.source_url}`}
                onLoadSuccess={(doc) => setPdfPages(doc.numPages)}
                onLoadError={(error) => {
                  console.error('PDF load error:', error);
                }}
                options={pdfOptions}
                loading={<div className="loading">PDF 加载中...</div>}
                error={<div className="error">PDF 加载失败</div>}
              >
                {Array.from({ length: pdfPages }, (_, idx) => (
                  <Page
                    key={`page_${idx + 1}`}
                    pageNumber={idx + 1}
                    width={pdfWidth}
                    renderAnnotationLayer={false}
                    renderTextLayer={true}
                  />
                ))}
              </Document>
            </div>
          ) : (
            <div className="full-text" style={{ whiteSpace: 'pre-wrap', lineHeight: 1.8 }}>
              {paper.full_text}
            </div>
          )}
        </div>
      </div>

      {showPopup && selectedText && (
        <div
          className="selection-popup"
          style={{ left: popupPosition.x, top: popupPosition.y }}
        >
          <button onClick={handleMarkHighlight}>标记</button>
          <button onClick={handleExplainText}>解释</button>
          <button onClick={handleTranslateText}>翻译</button>
          <button onClick={handleSaveNote}>保存笔记</button>
          <button onClick={() => setShowPopup(false)}>✕</button>
        </div>
      )}

      {showExplanationPanel && (
        <div className="explanation-panel">
          <div className="panel-header">
            <h3>AI 解释</h3>
            <button onClick={() => setShowExplanationPanel(false)} className="close-btn">✕</button>
          </div>
          {loadingExplanation ? (
            <p className="loading">加载中...</p>
          ) : explanation ? (
            <div className="explanation-content">
              <div className="explanation-text">
                <strong>解释:</strong>
                <p>{explanation.explanation}</p>
              </div>
              {explanation.key_terms && explanation.key_terms.length > 0 && (
                <div className="key-terms">
                  <strong>关键术语:</strong>
                  <div className="terms-list">
                    {explanation.key_terms.map((term, idx) => (
                      <span key={idx} className="term-tag">{term}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <p>点击"解释"按钮获取解释</p>
          )}
          {loadingTranslation && <p className="loading">翻译中...</p>}
          {translation && (
            <div className="explanation-content">
              <div className="explanation-text">
                <strong>翻译:</strong>
                <p>{translation}</p>
              </div>
            </div>
          )}
        </div>
      )}

      {notes.length > 0 && (
        <div className="highlights-list">
          <h3>我的笔记 ({notes.length})</h3>
          {notes.map((note) => (
            <div key={note.id} className="highlight-item">
              <p className="highlight-text">"{note.text}"</p>
            </div>
          ))}
        </div>
      )}

      {highlights.length > 0 && (
        <div className="highlights-list">
          <h3>我的高亮 ({highlights.length})</h3>
          {highlights.map((h) => (
            <div key={h.id} className="highlight-item">
              <p className="highlight-text">"{h.text}"</p>
              {h.explanation && (
                <p className="highlight-explanation">{h.explanation}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
