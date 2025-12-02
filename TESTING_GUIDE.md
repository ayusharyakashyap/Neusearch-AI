# 🧪 Testing Guide - Neusearch Product Assistant

## Current Status

✅ **Backend**: Running on http://localhost:8000
✅ **Frontend**: Running on http://localhost:3000
✅ **Products Loaded**: 5 sample products
✅ **Vector DB**: Operational
✅ **Chat AI**: Working (with fallback logic)

## Quick Test Commands

### 1. Test Backend Health
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

### 2. Get All Products
```bash
curl http://localhost:8000/api/products | python3 -m json.tool
```

### 3. Chat with AI Assistant
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I need furniture for my small bedroom"}' \
  | python3 -m json.tool
```

### 4. Search Products
```bash
curl http://localhost:8000/api/chat/search/bedroom | python3 -m json.tool
```

### 5. Load More Products
```bash
curl -X POST http://localhost:8000/api/scraping \
  -H "Content-Type: application/json" \
  -d '{"max_products": 30, "use_fallback": true}'
```

## Frontend Testing

### Open in Browser
1. **Home Page**: http://localhost:3000
   - See product grid
   - Click on products for details

2. **Chat Interface**: http://localhost:3000/chat
   - Type natural language queries
   - See AI recommendations
   - Click on product cards

### Test Queries for Chat

Try these in the chat interface:

1. **Simple Query**:
   ```
   Show me sofas
   ```

2. **Room-based Query**:
   ```
   I need furniture for my bedroom
   ```

3. **Abstract Query**:
   ```
   Looking for something comfortable for both working and relaxing
   ```

4. **Size-based Query**:
   ```
   Small apartment furniture with storage
   ```

5. **Price-based Query**:
   ```
   Affordable furniture under 15000
   ```

## API Documentation

Visit: http://localhost:8000/docs

Interactive Swagger UI with all endpoints.

## Stop Services

### Stop Backend
```bash
# Find process
ps aux | grep uvicorn | grep -v grep

# Kill process
kill -9 <PID>
```

### Stop Frontend
```bash
# Find process
ps aux | grep react-scripts | grep -v grep

# Kill process
kill -9 <PID>
```

Or use:
```bash
pkill -f uvicorn
pkill -f react-scripts
```

## Restart Services

### Backend
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/backend.log 2>&1 &
```

### Frontend
```bash
cd frontend
PORT=3000 npm start > /tmp/frontend.log 2>&1 &
```

## Check Logs

```bash
# Backend logs
tail -f /tmp/backend.log

# Frontend logs
tail -f /tmp/frontend.log
```

## Current Products in Database

1. Valencia Fabric Sofa 3 Seater - ₹8,999
2. Archer Queen Bed with Storage - ₹12,999
3. Dining Table 4 Seater with Chairs - ₹15,999
4. Study Table with Chair - ₹6,999
5. Wardrobe 3 Door with Mirror - ₹18,999

## Testing the RAG Pipeline

The system uses:
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB
- **LLM**: OpenAI GPT-3.5 (with fallback to keyword matching)

To test RAG:
1. Ask abstract questions in chat
2. Check if relevant products are returned
3. Verify AI provides explanations

## Known Issues

1. **OpenAI API**: Set `OPENAI_API_KEY` in .env for better responses
2. **Images**: Some placeholder images may not load
3. **Warnings**: React has some ESLint warnings (non-critical)

## Success Criteria

✅ Backend responds to API calls
✅ Frontend loads and displays products
✅ Chat returns relevant recommendations
✅ Product detail pages work
✅ Navigation between pages works
✅ Responsive design on mobile
