/**
 * API utility functions for communicating with backend
 */
import axios from 'axios';

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';
const API_ORIGIN = API_BASE_URL.replace(/\/api\/?$/, '');

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Paper API
export const paperAPI = {
  search: (query, limit = 10) => 
    api.get('/papers/search', { params: { query, limit } }),
  get: (paperId) => 
    api.get(`/papers/${paperId}`),
  list: (skip = 0, limit = 10) => 
    api.get(`/papers?skip=${skip}&limit=${limit}`),
  create: (paperData) => 
    api.post('/papers', paperData),
  uploadPdf: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/papers/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  delete: (paperId) => 
    api.delete(`/papers/${paperId}`),
};

// Highlight API
export const highlightAPI = {
  create: (highlightData) => 
    api.post('/highlights', highlightData),
  getForPaper: (paperId, userId) => 
    api.get(`/highlights/paper/${paperId}?user_id=${userId}`),
  delete: (highlightId) => 
    api.delete(`/highlights/${highlightId}`),
  explain: (text, context = null) => 
    api.post('/highlights/explain', { text, context }),
  translate: (text, targetLanguage = 'en') =>
    api.post('/highlights/translate', { text, target_language: targetLanguage }),
  addExplanation: (highlightId, text, context = null) => 
    api.post(`/highlights/${highlightId}/explanation`, { text, context }),
};

// Writing API
export const writingAPI = {
  generateEssayIdeas: (paperId, userId) => 
    api.post(`/writing/essay-ideas/${paperId}?user_id=${userId}`),
  generateEssayIdeasFromText: (payload) =>
    api.post('/essay-ideas', payload),
  chatEssayIdea: (payload) =>
    api.post('/essay-ideas/chat', payload),
  getEssayIdeas: (paperId, userId) => 
    api.get(`/writing/essay-ideas/${paperId}?user_id=${userId}`),
  deleteEssayIdea: (ideaId) => 
    api.delete(`/writing/essay-ideas/${ideaId}`),
  humaniseText: (text) => 
    api.post('/writing/humanise', { text }),
  pdfChat: (payload) =>
    api.post('/writing/pdf-chat', payload),
};

// Quote API
export const quoteAPI = {
  search: (keyword) => 
    api.get(`/quotes/search?keyword=${keyword}`),
  findSource: (text) =>
    api.post('/find-source', { text }),
  browse: (era = null, limit = 10) => 
    api.get(`/quotes/browse?${era ? `era=${era}&` : ''}limit=${limit}`),
  add: (quoteData) => 
    api.post('/quotes', quoteData),
};

export { API_BASE_URL, API_ORIGIN };
export default api;
