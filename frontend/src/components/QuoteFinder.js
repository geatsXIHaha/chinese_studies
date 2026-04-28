/**
 * Chinese Quotes Finder Component (名句溯源)
 */
import React, { useState } from 'react';
import { quoteAPI } from '../utils/api';
import '../styles/QuoteFinder.css';

export const QuoteFinder = () => {
  const [searchKeyword, setSearchKeyword] = useState('');
  const [quotes, setQuotes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchKeyword.trim()) return;

    setLoading(true);
    setHasSearched(true);
    try {
      const response = await quoteAPI.search(searchKeyword);
      setQuotes(response.data);
    } catch (error) {
      console.error('Error searching quotes:', error);
      setQuotes([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="quote-finder">
      <div className="quote-header">
        <h2>📚 名句溯源 (Chinese Quote Finder)</h2>
        <p>探索中文古籍名句及其出处</p>
      </div>

      <form onSubmit={handleSearch} className="quote-search">
        <input
          type="text"
          placeholder="搜索关键词、作者或经典著作..."
          value={searchKeyword}
          onChange={(e) => setSearchKeyword(e.target.value)}
          className="quote-search-input"
        />
        <button type="submit" disabled={loading} className="quote-search-btn">
          {loading ? '搜索中...' : '搜索'}
        </button>
      </form>

      <div className="quotes-results">
        {hasSearched && quotes.length === 0 && !loading && (
          <p className="no-results">未找到相关名句</p>
        )}
        {quotes.map((quote, idx) => (
          <div key={idx} className="quote-card">
            <div className="quote-content">
              <p className="quote-text">"{quote.quote}"</p>
              <p className="quote-source">——《{quote.source}》</p>
            </div>
            <div className="quote-info">
              {quote.author && <span className="quote-author">作者: {quote.author}</span>}
              {quote.era && <span className="quote-era">年代: {quote.era}</span>}
            </div>
            {quote.meaning && (
              <div className="quote-meaning">
                <strong>含义:</strong>
                <p>{quote.meaning}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
