/**
 * Writing Assistant Component
 */
import React, { useState } from 'react';
import { writingAPI } from '../utils/api';
import '../styles/WritingAssistant.css';

export const WritingAssistant = ({ paper, userId = 'default-user' }) => {
  const [essayIdeas, setEssayIdeas] = useState([]);
  const [loadingIdeas, setLoadingIdeas] = useState(false);
  const [ideaText, setIdeaText] = useState('');
  const [useFullText, setUseFullText] = useState(true);
  const [showPdfChat, setShowPdfChat] = useState(false);
  const [pdfChatMessages, setPdfChatMessages] = useState([]);
  const [pdfChatInput, setPdfChatInput] = useState('');
  const [pdfChatLoading, setPdfChatLoading] = useState(false);
  const [activeIdeaTopic, setActiveIdeaTopic] = useState('');
  const [customIdeaTopic, setCustomIdeaTopic] = useState('');
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [textToHumanise, setTextToHumanise] = useState('');
  const [humanisedText, setHumanisedText] = useState('');
  const [loadingHumanise, setLoadingHumanise] = useState(false);

  const handleGenerateEssayIdeas = async () => {
    setLoadingIdeas(true);
    try {
      const sourceText = useFullText
        ? paper.full_text || paper.abstract || paper.title
        : ideaText.trim();
      const response = await writingAPI.generateEssayIdeasFromText({
        text: sourceText,
        title: paper.title,
        max_ideas: 5,
      });
      setEssayIdeas(response.data.ideas || []);
      setActiveIdeaTopic('');
      setConversationId(null);
      setChatMessages([]);
    } catch (error) {
      console.error('Error generating essay ideas:', error);
    } finally {
      setLoadingIdeas(false);
    }
  };

  const handleSelectIdea = (idea) => {
    setActiveIdeaTopic(idea.topic);
    setCustomIdeaTopic('');
    setConversationId(null);
    setChatMessages([
      { role: 'assistant', content: '已选择选题，可继续提问或让 AI 展开写作思路。' },
    ]);
  };

  const handleSendChat = async () => {
    const message = chatInput.trim();
    if (!message) return;

    const ideaTopic = activeIdeaTopic || customIdeaTopic.trim();
    if (!ideaTopic) return;

    setChatLoading(true);
    const nextMessages = [...chatMessages, { role: 'user', content: message }];
    setChatMessages(nextMessages);
    setChatInput('');

    try {
      const response = await writingAPI.chatEssayIdea({
        paper_id: paper.id,
        user_id: userId,
        idea_topic: ideaTopic,
        message,
        conversation_id: conversationId,
      });

      setConversationId(response.data.conversation_id);
      if (Array.isArray(response.data.messages) && response.data.messages.length > 0) {
        setChatMessages(
          response.data.messages.map((msg) => ({
            role: msg.role,
            content: msg.content,
          }))
        );
      } else {
        setChatMessages((prev) => [...prev, { role: 'assistant', content: response.data.reply }]);
      }
    } catch (error) {
      console.error('Error chatting for essay idea:', error);
      setChatMessages((prev) => [
        ...prev,
        { role: 'assistant', content: '生成失败，请稍后再试。' },
      ]);
    } finally {
      setChatLoading(false);
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

  const handlePdfChatSend = async () => {
    const message = pdfChatInput.trim();
    if (!message) return;

    const nextMessages = [...pdfChatMessages, { role: 'user', content: message }];
    setPdfChatMessages(nextMessages);
    setPdfChatInput('');
    setPdfChatLoading(true);

    try {
      const response = await writingAPI.pdfChat({
        paper_id: paper.id,
        message,
      });
      setPdfChatMessages((prev) => [
        ...prev,
        { role: 'assistant', content: response.data.reply },
      ]);
    } catch (error) {
      console.error('Error chatting about PDF:', error);
      setPdfChatMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'AI 暂时不可用，请稍后再试。' },
      ]);
    } finally {
      setPdfChatLoading(false);
    }
  };

  return (
    <div className="writing-assistant">
      <div className="assistant-section essay-ideas-section">
        <div className="assistant-header-row">
          <h3>📝 论文思路生成器</h3>
          <button
            className="mini-chat-btn"
            type="button"
            onClick={() => setShowPdfChat((prev) => !prev)}
          >
            💬 PDF问答
          </button>
        </div>
        <p>基于论文文本生成选题、论点与要点</p>

        <div className="idea-source">
          <label>
            <input
              type="checkbox"
              checked={useFullText}
              onChange={(e) => setUseFullText(e.target.checked)}
            />
            使用全文内容
          </label>
          {!useFullText && (
            <textarea
              placeholder="粘贴选中段落或自定义文本..."
              value={ideaText}
              onChange={(e) => setIdeaText(e.target.value)}
              className="text-input"
              rows="4"
            />
          )}
        </div>
        <button
          onClick={handleGenerateEssayIdeas}
          disabled={loadingIdeas || (!useFullText && !ideaText.trim())}
          className="generate-btn"
        >
          {loadingIdeas ? '生成中...' : 'Generate Essay Ideas'}
        </button>

        {essayIdeas.length > 0 && (
          <div className="ideas-list">
            {essayIdeas.map((idea, idx) => (
              <button
                type="button"
                key={idx}
                className={`idea-card ${activeIdeaTopic === idea.topic ? 'active' : ''}`}
                onClick={() => handleSelectIdea(idea)}
              >
                <div className="idea-card-header">
                  <span className="idea-number">{idx + 1}</span>
                  <h4>{idea.topic}</h4>
                </div>
                <p className="idea-thesis"><strong>论点:</strong> {idea.thesis}</p>
                {idea.supporting_points && idea.supporting_points.length > 0 && (
                  <ul className="idea-points">
                    {idea.supporting_points.map((point, pointIdx) => (
                      <li key={pointIdx}>{point}</li>
                    ))}
                  </ul>
                )}
              </button>
            ))}
          </div>
        )}

        <div className="idea-chat">
          <h4>💬 选题写作对话</h4>
          <div className="idea-chat-topic">
            <label>当前选题</label>
            {activeIdeaTopic ? (
              <div className="idea-chat-pill">{activeIdeaTopic}</div>
            ) : (
              <input
                type="text"
                placeholder="输入自定义选题..."
                value={customIdeaTopic}
                onChange={(e) => setCustomIdeaTopic(e.target.value)}
              />
            )}
          </div>

          <div className="idea-chat-messages">
            {chatMessages.length === 0 ? (
              <p className="idea-chat-empty">选择一个选题或输入自定义选题开始对话。</p>
            ) : (
              chatMessages.map((msg, index) => (
                <div key={index} className={`idea-chat-bubble ${msg.role}`}>
                  {msg.content}
                </div>
              ))
            )}
          </div>

          <div className="idea-chat-input">
            <textarea
              placeholder="输入问题或要求，例如: 这个选题可以写哪些章节?"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              rows="3"
            />
            <button
              onClick={handleSendChat}
              disabled={chatLoading || !chatInput.trim() || (!activeIdeaTopic && !customIdeaTopic.trim())}
            >
              {chatLoading ? '生成中...' : '发送'}
            </button>
          </div>
        </div>
      </div>

      {showPdfChat && (
        <div className="assistant-section pdf-chat-section">
          <h3>💬 PDF 内容问答</h3>
          <p>基于当前论文内容回答问题</p>
          <div className="pdf-chat-messages">
            {pdfChatMessages.length === 0 ? (
              <p className="pdf-chat-empty">输入问题开始对话</p>
            ) : (
              pdfChatMessages.map((msg, idx) => (
                <div key={idx} className={`pdf-chat-bubble ${msg.role}`}>
                  {msg.content}
                </div>
              ))
            )}
          </div>
          <div className="pdf-chat-input">
            <textarea
              placeholder="问：这篇论文的核心观点是什么？"
              value={pdfChatInput}
              onChange={(e) => setPdfChatInput(e.target.value)}
              rows="3"
            />
            <button
              type="button"
              onClick={handlePdfChatSend}
              disabled={pdfChatLoading || !pdfChatInput.trim()}
            >
              {pdfChatLoading ? '回答中...' : '发送'}
            </button>
          </div>
        </div>
      )}

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
