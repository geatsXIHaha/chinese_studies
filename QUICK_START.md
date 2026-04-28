# Quick Start Guide

## Windows Users

1. **Run Setup Script**:
   ```
   setup.bat
   ```
   This will automatically install all dependencies.

2. **Start Backend** (in a new terminal):
   ```
   cd backend
   venv\Scripts\activate
   python -m uvicorn app.main:app --reload
   ```

3. **Start Frontend** (in another new terminal):
   ```
   cd frontend
   npm start
   ```

4. **Open Browser**: Visit `http://localhost:3000`

## macOS/Linux Users

1. **Run Setup Script**:
   ```bash
   bash setup.sh
   ```
   This will automatically install all dependencies.

2. **Start Backend** (in a new terminal):
   ```bash
   cd backend
   source venv/bin/activate
   python -m uvicorn app.main:app --reload
   ```

3. **Start Frontend** (in another new terminal):
   ```bash
   cd frontend
   npm start
   ```

4. **Open Browser**: Visit `http://localhost:3000`

## Features Demo

### 1. Search Papers 🔍
- Type keywords in the search box
- Mock data includes 3 papers about Chinese academic research
- Click "查看详情" to view full paper

### 2. View Paper 📄
- Read abstract and full text
- Select any text to highlight

### 3. Highlight & Explain 💡
- Select text from the paper
- Click "高亮" to highlight
- Click "解释" to get AI explanation
- Explanations are powered by mock LLM (no API key needed)

### 4. Generate Essay Ideas ✨
- Navigate to "写作助手" tab
- Click "生成论文思路"
- Get 3 unique essay ideas based on the paper

### 5. Humanize Writing ✨
- Paste academic text in the text area
- Click "润色文字"
- Get more natural, readable version
- Click "复制" to copy the result

### 6. Find Chinese Quotes 📚
- Navigate to "名句溯源" tab
- Search by keyword, author, or quote
- Browse classical Chinese quotes
- See meanings and historical context

## API Documentation

While the app is running, visit:
- Backend API Docs: `http://localhost:8000/docs`
- Backend ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

**Q: "Cannot find module 'react'"**
- Solution: Run `npm install` in the frontend folder

**Q: Backend won't start**
- Check if port 8000 is already in use
- Try: `python -m uvicorn app.main:app --port 8001 --reload`

**Q: Database not found**
- Run: `python init_db.py` in the backend folder

**Q: CORS error**
- Ensure backend is running on port 8000
- Frontend should be on port 3000

## File Structure for Development

```
backend/
  ├── app/
  │   ├── models/       - Database models
  │   ├── routes/       - API endpoints
  │   ├── services/     - Business logic
  │   └── main.py       - FastAPI app
  └── init_db.py        - Setup database

frontend/
  ├── src/
  │   ├── components/   - React components
  │   ├── utils/        - API helpers
  │   └── styles/       - CSS files
  └── package.json      - npm packages
```

## Next Steps

1. **Add Real Papers**: Modify mock data in `backend/init_db.py`
2. **Connect OpenAI API**: Update `backend/app/services/ai_service.py`
3. **Add User Authentication**: Implement JWT in backend routes
4. **Deploy**: Use Docker for backend, Vercel for frontend

Enjoy using the Chinese Academic AI Study System! 🎓✨
