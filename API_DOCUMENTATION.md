# API Documentation and Usage Examples

## Backend API Endpoints

### Base URL
```
http://localhost:8000
```

### Authentication
Currently, no authentication is required (development mode). In production, add JWT tokens.

---

## Papers API

### List All Papers
```http
GET /api/papers?skip=0&limit=10
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "深度学习在中文自然语言处理中的应用",
    "authors": "张三, 李四, 王五",
    "abstract": "本论文研究了...",
    "keywords": "深度学习,中文NLP",
    "publication_date": "2023-05-15T00:00:00"
  }
]
```

### Get Paper by ID
```http
GET /api/papers/1
```

### Search Papers
```http
GET /api/papers/search/深度学习?limit=10
```

### Create Paper
```http
POST /api/papers
Content-Type: application/json

{
  "title": "New Paper Title",
  "authors": "Author Names",
  "abstract": "Paper abstract...",
  "full_text": "Full paper content...",
  "keywords": "keyword1,keyword2"
}
```

### Delete Paper
```http
DELETE /api/papers/1
```

---

## Highlights & Explanation API

### Create Highlight
```http
POST /api/highlights
Content-Type: application/json

{
  "paper_id": 1,
  "user_id": "user123",
  "text": "Selected text from paper",
  "start_position": 100,
  "end_position": 120
}
```

### Get Highlights for Paper
```http
GET /api/highlights/paper/1?user_id=user123
```

### Explain Text
```http
POST /api/highlights/explain
Content-Type: application/json

{
  "text": "epistemology",
  "context": "academic research"
}
```

**Response:**
```json
{
  "original_text": "epistemology",
  "explanation": "认识论，研究知识的来源、本质和范围的哲学分支...",
  "key_terms": ["哲学", "知识论"]
}
```

### Delete Highlight
```http
DELETE /api/highlights/1
```

---

## Writing Assistance API

### Generate Essay Ideas
```http
POST /api/writing/essay-ideas/1?user_id=user123
```

**Response:**
```json
{
  "paper_id": 1,
  "ideas": [
    {
      "id": 1,
      "idea": "论文'深度学习在中文自然语言处理中的应用'的理论框架对现代教育的影响"
    },
    {
      "id": 2,
      "idea": "从'深度学习在中文自然语言处理中的应用'的角度探讨中文学术写作的未来发展"
    }
  ]
}
```

### Humanize Writing
```http
POST /api/writing/humanise
Content-Type: application/json

{
  "text": "鉴于此外就而言相应地故由此可见..."
}
```

**Response:**
```json
{
  "original_text": "original text...",
  "humanised_text": "more natural text..."
}
```

---

## Chinese Quotes API (名句溯源)

### Search Quotes
```http
GET /api/quotes/search?keyword=学习
```

**Response:**
```json
[
  {
    "id": 1,
    "quote": "学而时习之，不亦说乎",
    "source": "《论语》",
    "author": "孔子",
    "era": "春秋战国",
    "meaning": "学习了知识，经常复习它，不是很快乐吗？..."
  }
]
```

### Browse Quotes
```http
GET /api/quotes/browse?era=唐代&limit=10
```

### Add Quote
```http
POST /api/quotes
Content-Type: application/json

{
  "quote": "新的名句",
  "source": "来源",
  "author": "作者",
  "era": "时代",
  "meaning": "含义"
}
```

---

## Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Interactive API Testing

Visit `http://localhost:8000/docs` for Swagger UI where you can test all endpoints interactively.

---

## Error Handling

### 404 Not Found
```json
{
  "detail": "Paper not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Search query cannot be empty"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Rate Limiting & Performance

- Mock LLM responses are instant (no API calls)
- SQLite handles up to ~100 papers without issues
- For production: Consider PostgreSQL and caching

---

## CORS Configuration

Currently accepts requests from all origins for development:
```python
allow_origins=["*"]
```

For production, update in `backend/app/main.py`:
```python
allow_origins=["https://yourdomain.com"]
```
