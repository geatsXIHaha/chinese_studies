/**
 * Chinese Quotes Finder Component (名句溯源)
 */
import React, { useState } from 'react';
import { quoteAPI } from '../utils/api';
import '../styles/QuoteFinder.css';

export const QuoteFinder = () => {
  const [searchKeyword, setSearchKeyword] = useState('');
  const [quotes, setQuotes] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchKeyword.trim()) return;

    setLoading(true);
    setHasSearched(true);
    try {
      const response = await quoteAPI.findSource(searchKeyword);
      setQuotes(response.data.results || []);
      setSuggestions(response.data.suggestions || []);
    } catch (error) {
      console.error('Error searching quotes:', error);
      setQuotes([]);
      setSuggestions([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (value) => {
    setSearchKeyword(value);
    setTimeout(() => {
      const fakeEvent = { preventDefault: () => {} };
      handleSearch(fakeEvent);
    }, 0);
  };

  return (
    <div className="quote-finder">
      <div className="quote-header">
        <h2>📚 名句溯源 (Chinese Quote Finder)</h2>
        <p>输入一句中文，查询出处与语境说明</p>
      </div>

      <form onSubmit={handleSearch} className="quote-search">
        <input
          type="text"
          placeholder="输入完整或部分句子..."
          value={searchKeyword}
          onChange={(e) => setSearchKeyword(e.target.value)}
          className="quote-search-input"
        />
        <button type="submit" disabled={loading} className="quote-search-btn">
          {loading ? '搜索中...' : '搜索'}
        </button>
      </form>

      <div className="quotes-results">
        {suggestions.length > 0 && (
          <div className="quote-suggestions">
            <h4>可能的补全/相关名句</h4>
            <div className="suggestion-list">
              {suggestions.map((item, idx) => (
                <button
                  key={idx}
                  type="button"
                  className="suggestion-item"
                  onClick={() => handleSuggestionClick(item)}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>
        )}
        {hasSearched && quotes.length === 0 && !loading && (
          <p className="no-results">未找到相关名句</p>
        )}
        {quotes.map((quote, idx) => (
          <div key={idx} className="quote-card">
            <div className="quote-content">
              <p className="quote-text">"{quote.original_text}"</p>
              <p className="quote-source">——《{quote.source}》</p>
            </div>
            <div className="quote-info">
              {quote.author && <span className="quote-author">作者: {quote.author}</span>}
            </div>
            {quote.context_explanation && (
              <div className="quote-meaning">
                <strong>语境说明:</strong>
                <p>{quote.context_explanation}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
