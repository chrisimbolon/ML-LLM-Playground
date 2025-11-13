# 🧠 CortexOS API Documentation

## Overview
CortexOS is a production-ready REST API for AI-powered document chat using Retrieval Augmented Generation (RAG).

**Base URL:** `http://localhost:8000`

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file:
```
OPENAI_API_KEY=sk-your-key-here
```

### 3. Run the Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access Interactive Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📡 API Endpoints

### **GET /** - Health Check
Check if the API is running.

**Response:**
```json
{
  "service": "CortexOS API",
  "status": "🔥 Running hot!",
  "version": "1.0.0",
  "active_sessions": 3
}
```

---

### **POST /upload** - Upload Document
Upload a PDF or TXT file to create a new chat session.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: File upload (PDF or TXT)

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "filename": "document.pdf",
  "pages": 15,
  "chunks": 47,
  "message": "✅ Document processed successfully!"
}
```

**Important:** Save the `session_id` - you'll need it for chatting!

---

### **POST /chat** - Chat with Document
Ask questions about your uploaded document.

**Request:**
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "question": "What is this document about?"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id",
    "question": "Summarize the key findings"
  }'
```

**Response:**
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "question": "What is this document about?",
  "answer": "This document is a research paper on machine learning techniques...",
  "sources": [
    {
      "page": 1,
      "content": "Abstract: In this paper we explore...",
      "source": "/path/to/document.pdf"
    }
  ],
  "latency_ms": 1234.56
}
```

---

### **GET /sessions** - List All Sessions
Get a list of all active chat sessions.

**Response:**
```json
[
  {
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "filename": "document.pdf",
    "created_at": "2024-11-10T10:30:00",
    "chunks_count": 47
  }
]
```

---

### **GET /session/{session_id}** - Get Session Info
Get detailed information about a specific session.

**Response:**
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "filename": "document.pdf",
  "created_at": "2024-11-10T10:30:00",
  "chunks_count": 47
}
```

---

### **DELETE /session/{session_id}** - Delete Session
Delete a session and cleanup all associated resources.

**Response:**
```json
{
  "message": "Session a1b2c3d4-... deleted successfully"
}
```

---

## 🐳 Docker Deployment

### Build and Run
```bash
# Build the image
docker-compose build

# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

---

## 🧪 Testing with Python

Save the test client script and run:
```bash
python test_client.py
```

### Manual Testing with `requests`
```python
import requests

# Upload
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/upload',
        files={'file': f}
    )
session_id = response.json()['session_id']

# Chat
response = requests.post(
    'http://localhost:8000/chat',
    json={
        'session_id': session_id,
        'question': 'What is this about?'
    }
)
print(response.json()['answer'])
```

---

## 🔥 Example Workflow

### 1. Upload a Document
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@research_paper.pdf"
```
**Returns:** `session_id`

### 2. Start Chatting
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "question": "What are the main conclusions?"
  }'
```

### 3. Ask Follow-up Questions
The API maintains conversation history, so you can ask follow-ups:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "question": "Can you explain that in simpler terms?"
  }'
```

### 4. Cleanup When Done
```bash
curl -X DELETE http://localhost:8000/session/YOUR_SESSION_ID
```

---

## 💰 Cost Tracking

Each response includes `latency_ms` which you can log. To track tokens:

1. Check OpenAI dashboard for usage
2. Calculate cost: `tokens × model_price`
3. Store in your database for analytics

---

## 🔧 Configuration

### Chunk Size Tuning
In `main.py`, adjust:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Larger = more context, higher cost
    chunk_overlap=200     # Prevents cutting sentences
)
```

### Model Selection
Change the model:
```python
self.llm = ChatOpenAI(
    model_name="gpt-4",  # or "gpt-3.5-turbo" for cheaper
    temperature=0.7
)
```

### Retrieval Tuning
Adjust number of chunks retrieved:
```python
retriever=self.vectorstore.as_retriever(
    search_kwargs={"k": 6}  # Retrieve top 6 chunks
)
```

---

## 🚨 Error Handling

### Common Errors

**400 - Bad Request**
- Unsupported file type
- Missing required fields

**404 - Not Found**
- Session doesn't exist (may have expired)

**500 - Internal Server Error**
- OpenAI API error
- Document processing failed

---

## 🔐 Production Checklist

- [ ] Set up proper CORS origins (not `*`)
- [ ] Add authentication (JWT tokens)
- [ ] Use Redis for session storage
- [ ] Set up rate limiting
- [ ] Add logging and monitoring
- [ ] Use PostgreSQL for metadata
- [ ] Deploy behind reverse proxy (Nginx)
- [ ] Set up SSL/TLS certificates
- [ ] Configure environment-specific settings
- [ ] Add input validation and sanitization

---

## 📊 Next Steps

1. **Add PostgreSQL** for user management
2. **Implement JWT auth** for security
3. **Add Redis** for caching
4. **Build frontend** (React/Vue)
5. **Set up monitoring** (Prometheus/Grafana)
6. **Deploy to production** (DigitalOcean/AWS)

---

## 🎸 You're Ready to Rock!

Your FastAPI RAG service is production-ready. Start building the Cortex monitoring layer next!