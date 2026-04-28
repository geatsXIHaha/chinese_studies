# Architecture & Design

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer (React)                    │
├─────────────────────────────────────────────────────────────┤
│  SearchPaper  │ PaperViewer │ WritingAssistant │ QuoteFinder │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP/JSON (Axios)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│           API Gateway / Backend (FastAPI)                    │
├─────────────────────────────────────────────────────────────┤
│  Routes:                                                     │
│  ├── /api/papers (Search, CRUD)                             │
│  ├── /api/highlights (Annotations, Explanations)            │
│  ├── /api/writing (Essay Ideas, Humanization)               │
│  └── /api/quotes (Chinese Quote Finder)                     │
└────────────────────────────┬────────────────────────────────┘
                             │ SQLAlchemy ORM
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  Data Access Layer                           │
├─────────────────────────────────────────────────────────────┤
│  Models:                                                     │
│  ├── Paper (Academic papers)                                │
│  ├── Highlight (User annotations)                           │
│  ├── EssayIdea (Generated ideas)                             │
│  └── ChineseQuote (Classical quotes)                         │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   SQLite Database                            │
│          (chinese_studies.db)                                │
└─────────────────────────────────────────────────────────────┘
```

## Service Layer Architecture

### AI Service (Mock LLM)
```
AIService
├── explain_text(text, context)
│   └── Returns: explanation, key_terms
├── generate_essay_ideas(title, abstract)
│   └── Returns: list of 3 ideas
├── humanise_writing(text)
│   └── Returns: more natural text
└── find_chinese_quotes(keyword)
    └── Returns: matching quotes
```

### Business Logic Services
```
PaperService
├── create_paper()
├── get_paper()
├── search_papers()
├── list_papers()
└── delete_paper()

HighlightService
├── create_highlight()
├── get_highlights_for_paper()
├── update_highlight_explanation()
└── delete_highlight()

EssayIdeaService
├── create_essay_idea()
├── get_essay_ideas_for_paper()
└── delete_essay_idea()
```

## Data Flow Examples

### Example 1: Paper Search & Highlight
```
1. User enters search query
   │
   ├─→ SearchPaper component
       ├─→ axios.get(/api/papers/search/{query})
           │
           ├─→ Backend paper_routes.py
           ├─→ PaperService.search_papers()
           ├─→ SQLAlchemy query on Paper model
           ├─→ Returns list of matching papers
           │
   ├─→ Display results in PaperCard components
   │
2. User selects a paper
   │
   ├─→ PaperViewer component loaded
   ├─→ Paper full text displayed
   │
3. User selects and highlights text
   │
   ├─→ Selection detected via onMouseUp
   ├─→ Highlight toolbar appears
   ├─→ User clicks "高亮" (Highlight)
       │
       ├─→ highlightAPI.create({
           paper_id, user_id, text, positions
         })
       ├─→ Backend highlight_routes.py
       ├─→ HighlightService.create_highlight()
       ├─→ SQLAlchemy inserts Highlight record
       ├─→ Returns created highlight
       │
   ├─→ UI updates with new highlight
   │
4. User clicks "解释" (Explain)
   │
   ├─→ highlightAPI.explain(text)
   ├─→ Backend: ai_service.explain_text()
   ├─→ Mock LLM returns explanation
   ├─→ Display in explanation panel
```

### Example 2: Essay Idea Generation
```
1. User navigates to WritingAssistant tab
   │
   ├─→ WritingAssistant component receives paper
   │
2. User clicks "生成论文思路" button
   │
   ├─→ writingAPI.generateEssayIdeas(paperId, userId)
   ├─→ POST /api/writing/essay-ideas/{paperId}?user_id={userId}
       │
       ├─→ Backend writing_routes.py
       ├─→ PaperService.get_paper(paperId)
       ├─→ ai_service.generate_essay_ideas(title, abstract)
       ├─→ Mock LLM generates 3 ideas
       ├─→ For each idea:
           │
           ├─→ EssayIdeaService.create_essay_idea()
           ├─→ SQLAlchemy inserts EssayIdea record
           │
       ├─→ Returns all created ideas
       │
   ├─→ Display ideas in component with numbers
```

## Component Hierarchy

```
App (Main component)
├── Header
├── Navigation
│   ├── SearchPaper button
│   ├── PaperViewer button (conditional)
│   ├── WritingAssistant button (conditional)
│   └── QuoteFinder button
│
└── Content Area (conditional rendering based on currentView)
    ├── SearchPaper
    │   ├── Search form
    │   └── Paper cards
    │
    ├── PaperViewer
    │   ├── Paper header
    │   ├── Paper content
    │   ├── Selection toolbar (conditional)
    │   ├── Explanation panel (conditional)
    │   └── Highlights list
    │
    ├── WritingAssistant
    │   ├── Essay Ideas section
    │   │   └── Ideas list
    │   └── Humanize Writing section
    │       ├── Input textarea
    │       └── Result display
    │
    └── QuoteFinder
        ├── Header
        ├── Search form
        └── Quote cards
```

## Database Schema

### Papers Table
```sql
CREATE TABLE papers (
  id INTEGER PRIMARY KEY,
  title VARCHAR(500),
  authors VARCHAR(500),
  abstract TEXT,
  full_text TEXT,
  source_url VARCHAR(500),
  keywords VARCHAR(500),
  publication_date DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Highlights Table
```sql
CREATE TABLE highlights (
  id INTEGER PRIMARY KEY,
  paper_id INTEGER,
  user_id VARCHAR(50),
  text TEXT,
  explanation TEXT,
  start_position INTEGER,
  end_position INTEGER,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (paper_id) REFERENCES papers(id)
);
```

### Essay Ideas Table
```sql
CREATE TABLE essay_ideas (
  id INTEGER PRIMARY KEY,
  paper_id INTEGER,
  user_id VARCHAR(50),
  idea TEXT,
  keywords VARCHAR(500),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (paper_id) REFERENCES papers(id)
);
```

### Chinese Quotes Table
```sql
CREATE TABLE chinese_quotes (
  id INTEGER PRIMARY KEY,
  quote TEXT,
  source VARCHAR(300),
  author VARCHAR(100),
  era VARCHAR(100),
  meaning TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Design Patterns Used

### 1. **Service Pattern**
- Separates business logic from routes
- AIService, PaperService, etc.
- Reusable across multiple routes

### 2. **Repository Pattern**
- Database queries isolated in services
- Easy to switch backends (DB → API, etc.)

### 3. **Dependency Injection**
- FastAPI's `Depends()` for database sessions
- Clean and testable code

### 4. **Custom Hooks (React)**
- `useApi()` for API calls with loading states
- Reusable across components

### 5. **Composition (React)**
- Components composed from smaller pieces
- SearchPaper, PaperViewer are standalone

## State Management

### Frontend
- Component-level state using `useState()`
- No Redux/Context needed for current scope
- Parent component (App) manages view selection

### Backend
- Database as source of truth
- Stateless FastAPI design
- Session management via Depends()

## Security Considerations

### Current (Development)
- CORS allows all origins
- No authentication required
- No input sanitization

### Production Recommendations
- ✅ Add JWT authentication
- ✅ Validate/sanitize all inputs
- ✅ Use environment variables for secrets
- ✅ Add rate limiting
- ✅ Use HTTPS only
- ✅ Database backups
- ✅ SQL injection prevention (already handled by ORM)

## Performance Optimizations

### Current
- SQLite with indexes on common queries
- Mock LLM (instant responses)
- Client-side highlighting (no backend processing)

### Future
- Add caching layer (Redis)
- Pagination for large datasets
- Database query optimization
- Frontend code splitting
- Image optimization

## Scalability Path

```
Phase 1 (Current):
SQLite + FastAPI + React on single server

Phase 2:
PostgreSQL + Redis + Multiple FastAPI instances (Kubernetes)

Phase 3:
Distributed microservices, API gateway, message queues
```
