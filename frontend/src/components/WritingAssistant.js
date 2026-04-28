/**
 * Writing Assistant Component
 */
import React, { useState } from 'react';
import { writingAPI } from '../utils/api';
import '../styles/WritingAssistant.css';

export const WritingAssistant = ({ paper, userId = 'default-user' }) => {
  const [essayIdeas, setEssayIdeas] = useState([]);
  const [loadingIdeas, setLoadingIdeas] = useState(false);
  const [textToHumanise, setTextToHumanise] = useState('');
  const [humanisedText, setHumanisedText] = useState('');
  const [loadingHumanise, setLoadingHumanise] = useState(false);

  const handleGenerateEssayIdeas = async () => {
    setLoadingIdeas(true);
    try {
      const response = await writingAPI.generateEssayIdeas(paper.id, userId);
      setEssayIdeas(response.data.ideas);
    } catch (error) {
      console.error('Error generating essay ideas:', error);
    } finally {
      setLoadingIdeas(false);
    }
  };

  const handleHumaniseText = async () => {
    if (!textToHumanise.trim()) return;
    
    setLoadingHumanise(true);
    try {
      const response = await writingAPI.humaniseText(textToHumanise);
      setHumanisedText(response.data.humanised_text);
    } catch (error) {
      console.error('Error humanising text:', error);
    } finally {
      setLoadingHumanise(false);
    }
  };

  return (
    <div className="writing-assistant">
      <div className="assistant-section essay-ideas-section">
        <h3>📝 论文思路生成器</h3>
        <p>基于当前论文生成创意性的论文思路</p>
        <button
          onClick={handleGenerateEssayIdeas}
          disabled={loadingIdeas}
          className="generate-btn"
        >
          {loadingIdeas ? '生成中...' : '生成论文思路'}
        </button>

        {essayIdeas.length > 0 && (
          <div className="ideas-list">
            {essayIdeas.map((idea, idx) => (
              <div key={idx} className="idea-item">
                <span className="idea-number">{idx + 1}</span>
                <p>{idea.idea}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="assistant-section humanise-section">
        <h3>✨ 文字润色 (Humanise Writing)</h3>
        <p>将学术文字改写得更自然流畅</p>
        
        <textarea
          placeholder="粘贴您需要润色的学术文字..."
          value={textToHumanise}
          onChange={(e) => setTextToHumanise(e.target.value)}
          className="text-input"
          rows="4"
        />
        
        <button
          onClick={handleHumaniseText}
          disabled={loadingHumanise || !textToHumanise.trim()}
          className="humanise-btn"
        >
          {loadingHumanise ? '处理中...' : '润色文字'}
        </button>

        {humanisedText && (
          <div className="humanised-result">
            <h4>润色后的文字:</h4>
            <div className="result-text">
              {humanisedText}
            </div>
            <button
              onClick={() => {
                navigator.clipboard.writeText(humanisedText);
                alert('已复制到剪贴板');
              }}
              className="copy-btn"
            >
              📋 复制
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
