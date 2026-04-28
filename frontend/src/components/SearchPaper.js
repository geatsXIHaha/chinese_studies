/**
 * Search Papers Component
 */
import React, { useState } from 'react';
import { paperAPI } from '../utils/api';
import '../styles/SearchPaper.css';

export const SearchPaper = ({ onSearch, onSelectPaper }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [uploadFile, setUploadFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState('');
  const [uploadSuccess, setUploadSuccess] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setHasSearched(true);
    try {
      const response = await paperAPI.search(query);
      setResults(response.data);
      onSearch?.(response.data);
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!uploadFile) return;

    setUploading(true);
    setUploadError('');
    setUploadSuccess('');

    try {
      const response = await paperAPI.uploadPdf(uploadFile);
      setUploadSuccess('上传成功，已加入论文列表');
      setResults((prev) => [response.data, ...prev]);
    } catch (error) {
      setUploadError(error.response?.data?.detail || '上传失败');
    } finally {
      setUploading(false);
      setUploadFile(null);
    }
  };

  const formatYear = (dateValue) => {
    if (!dateValue) return '未知年份';
    const date = new Date(dateValue);
    if (Number.isNaN(date.getTime())) return '未知年份';
    return date.getFullYear();
  };

  return (
    <div className="search-paper">
      <form onSubmit={handleSearch}>
        <div className="search-box">
          <input
            type="text"
            placeholder="搜索论文标题、作者或关键词..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="search-input"
          />
          <button type="submit" disabled={loading} className="search-btn">
            {loading ? '搜索中...' : '搜索'}
          </button>
        </div>
      </form>

      <div className="search-results">
        {hasSearched && results.length === 0 && !loading && (
          <p className="no-results">未找到匹配的论文</p>
        )}
        {results.map((paper) => (
          <div
            key={paper.id}
            className="paper-card"
            onClick={() => onSelectPaper?.(paper)}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                onSelectPaper?.(paper);
              }
            }}
          >
            <h3>{paper.title}</h3>
            <p className="authors">作者: {paper.authors}</p>
            <div className="paper-details">
              <span className="year">年份: {formatYear(paper.publication_date)}</span>
              {paper.source_url && (
                <a
                  className="source-link"
                  href={paper.source_url}
                  onClick={(e) => e.stopPropagation()}
                  target="_blank"
                  rel="noreferrer"
                >
                  来源链接
                </a>
              )}
            </div>
            <p className="abstract">{paper.abstract}</p>
            <div className="paper-meta">
              <span className="keywords">{paper.keywords}</span>
            </div>
            <button
              className="view-btn"
              onClick={(e) => {
                e.stopPropagation();
                onSelectPaper?.(paper);
              }}
            >
              查看详情
            </button>
          </div>
        ))}
      </div>

      <div className="upload-section">
        <h3>上传论文 PDF</h3>
        <p className="upload-hint">支持手动上传 PDF 文件（仅保存文件，不做解析）</p>
        <form onSubmit={handleUpload} className="upload-form">
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
          />
          <button type="submit" className="upload-btn" disabled={!uploadFile || uploading}>
            {uploading ? '上传中...' : '上传 PDF'}
          </button>
        </form>
        {uploadError && <p className="upload-error">{uploadError}</p>}
        {uploadSuccess && <p className="upload-success">{uploadSuccess}</p>}
      </div>
    </div>
  );
};
