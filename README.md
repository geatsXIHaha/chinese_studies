# Chinese Academic AI Study System

智能学术论文分析与写作辅助平台 | Full-Stack Web Application for Academic Paper Analysis with AI Support

## 📋 Project Overview

A comprehensive full-stack application designed to help Chinese academic students and researchers:

- **Search & Discover**: Find academic papers using intelligent search
- **Read & Annotate**: View papers with highlighting capabilities
- **Understand**: Get AI-powered explanations of highlighted text
- **Generate Ideas**: Automatically generate essay ideas based on papers
- **Polish Writing**: Humanize academic writing with AI assistance
- **Explore Sources**: Find Chinese classical quotes and their sources (名句溯源)

## 🏗️ Architecture Overview

```
chinese_studies/
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── routes/         # API endpoint definitions
│   │   ├── services/       # Business logic & AI services
│   │   ├── database.py     # Database configuration
│   │   ├── schemas.py      # Pydantic validation schemas
│   │   └── main.py         # FastAPI app setup
│   ├── requirements.txt    # Python dependencies
│   └── init_db.py          # Database initialization script
│
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── utils/          # API calls & utilities
│   │   ├── styles/         # Component stylesheets
│   │   ├── App.js          # Main app component
│   │   └── index.js        # Entry point
│   ├── public/             # Static HTML
│   └── package.json        # npm dependencies
│
└── data/                    # Data storage & mock data
```

## ✨ Core Features

### 1. Academic Paper Search System
- Full-text search across paper titles, authors, and keywords
- Mock data with 3 sample papers
- Paginated results

### 2. Paper Viewer UI
- Beautiful full-text display with syntax highlighting
- Abstract and full-text sections
- Paper metadata (authors, publication date)
- Responsive design

### 3. Text Highlighting & Selection
- Select text directly from paper content
- Highlight important passages
- Visual highlight markers
- Store highlights in database

### 4. AI Text Explanation
- Explain selected academic text
- Extract key terms from explanations
- Mock LLM with predefined responses
- Easy integration with real OpenAI API

### 5. Essay Idea Generator
- Generate 3 unique essay ideas based on paper content
- Ideas tailored to paper title and abstract
- Save ideas to user profile
- Modify and delete generated ideas

### 6. Writing Humanizer (Humanise Writing)
- Transform formal academic writing to natural text
- Replace overly formal expressions
- Improve readability
- Copy-to-clipboard functionality

### 7. Chinese Quote Finder (名句溯源)
- Search classical Chinese quotes
- Find quote origins and authors
- Explore by era (Dynasty/Period)
- View quote meanings and context
- Database of traditional quotes

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ 
- Node.js 14+ and npm
- SQLite (included with Python)

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create virtual environment** (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Initialize database with mock data**:
```bash
python init_db.py
```

5. **Start FastAPI server**:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Local Run (Quick)

Run backend and frontend in two terminals:

**Terminal A (Backend)**
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal B (Frontend)**
```bash
cd frontend
npm install
npm start
```

Open `http://localhost:3000` in your browser.

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Start development server**:
```bash
npm start
```

The frontend will open at `http://localhost:3000`

## 📚 API Endpoints

### Papers
- `GET /api/papers` - List all papers
- `GET /api/papers/{id}` - Get paper details
- `GET /api/papers/search/{query}` - Search papers
- `POST /api/papers` - Create new paper

### Highlights & Annotations
- `POST /api/highlights` - Create highlight
- `GET /api/highlights/paper/{paper_id}` - Get paper highlights
- `DELETE /api/highlights/{id}` - Delete highlight
- `POST /api/highlights/explain` - Get text explanation
- `POST /api/highlights/{id}/explanation` - Add explanation to highlight

### Writing Assistance
- `POST /api/writing/essay-ideas/{paper_id}` - Generate essay ideas
- `GET /api/writing/essay-ideas/{paper_id}` - Get essay ideas
- `DELETE /api/writing/essay-ideas/{id}` - Delete essay idea
- `POST /api/writing/humanise` - Humanize writing

### Chinese Quotes
- `GET /api/quotes/search` - Search quotes
- `GET /api/quotes/browse` - Browse quotes by era
- `POST /api/quotes` - Add new quote

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database**: SQLite with SQLAlchemy ORM
- **Validation**: Pydantic
- **API**: RESTful with CORS support

### Frontend
- **Framework**: React 18
- **HTTP Client**: Axios
- **Styling**: CSS3 with CSS Grid/Flexbox
- **Routing**: React Router (extensible)

### AI/ML
- **Default**: Mock LLM service (no API keys required)
- **Optional**: OpenAI API integration ready (just swap implementation)

## 📝 Database Models

### Paper
- id, title, authors, abstract, full_text, source_url, keywords, DOI
- publication_date, timestamps

### Highlight
- id, paper_id, user_id, text, explanation, position info, timestamp

### EssayIdea
- id, paper_id, user_id, idea, keywords, timestamp

### ChineseQuote
- id, quote, source, author, era, meaning, timestamp

## 🎨 UI Components

- **SearchPaper**: Search interface with result cards
- **PaperViewer**: Paper display with highlighting tools
- **WritingAssistant**: Essay ideas & writing humanizer
- **QuoteFinder**: Classical quote explorer

## 🔧 Extending the Project

### Add Real OpenAI API
Edit `/backend/app/services/ai_service.py`:
```python
def explain_text(self, text: str, context: str = None):
    if self.use_mock:
        return self.mock_service.explain_text(text, context)
    else:
        # Call real OpenAI API
        response = openai.ChatCompletion.create(...)
        return response
```

### Add Authentication
Implement in `/backend/app/routes/` using JWT tokens and dependency injection.

### Deploy to Production
- Backend: Docker + AWS/GCP/Azure
- Frontend: Vercel/Netlify
- Database: PostgreSQL (replace SQLite)

## 📖 Mock Data

The system includes 3 sample papers:
1. Deep Learning in Chinese NLP
2. Fusion of Traditional Chinese Literature with Digital Humanities
3. Rhetorical Strategies in Academic Writing: English-Chinese Comparison

Plus 5 classical Chinese quotes from different eras.

## 🐛 Troubleshooting

**CORS Issues**: Backend includes CORS middleware. Frontend runs on port 3000, backend on 8000.

**Database Locked**: SQLite may show "database is locked". Restart both servers.

**API Not Found**: Ensure backend is running and check `http://localhost:8000/docs` for available endpoints.

## 📄 License

MIT License - Feel free to use and modify for your projects.

## 🙏 Acknowledgments

- Built with FastAPI and React
- Chinese classical quotes from traditional sources
- Designed for Chinese academic research community

---

**Happy studying! 学无止境!** 📚✨
