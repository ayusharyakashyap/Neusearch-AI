# Neusearch AI Product Discovery Assistant

An AI-powered furniture and home decor discovery assistant that helps users find the perfect products through natural language conversations and intelligent recommendations.

## 🚀 Live Demo

- **Frontend**: [Deployed Frontend URL]
- **Backend API**: [Deployed Backend URL]
- **Demo Video**: [Loom Video Link]

## 🏗️ Architecture Overview

This project consists of three main components:

1. **FastAPI Backend** - REST API with scraping, vector search, and LLM integration
2. **React Frontend** - User interface with product browsing and chat interface
3. **PostgreSQL Database** - Product data storage
4. **ChromaDB** - Vector database for semantic search

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React App     │    │   FastAPI       │    │   PostgreSQL    │
│   (Frontend)    │───▶│   (Backend)     │───▶│   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   ChromaDB      │
                       │ (Vector Store)  │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   OpenAI API    │
                       │     (LLM)       │
                       └─────────────────┘
```

## ✨ Features

### 🛍️ Core Functionality
- **Product Discovery**: Browse furniture from Furlenco.com
- **AI Chat Assistant**: Natural language product recommendations
- **Semantic Search**: Vector-based product matching
- **Product Details**: Comprehensive product information pages

### 🤖 AI Capabilities
- **Abstract Query Understanding**: Handles queries like "furniture for gym and meetings"
- **Contextual Recommendations**: Provides explanations for product suggestions
- **Clarifying Questions**: Asks for more details when queries are vague
- **Multi-modal Search**: Combines text and product features for better matching

### 🔧 Technical Features
- **Responsive Design**: Works on desktop and mobile
- **Real-time Chat**: Instant AI responses
- **Fallback Data**: Works even when scraping fails
- **Docker Support**: Easy deployment with containers
- **Error Handling**: Graceful error recovery

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Primary database for product storage
- **ChromaDB** - Vector database for embeddings
- **SQLAlchemy** - Database ORM
- **BeautifulSoup4** - Web scraping
- **Sentence Transformers** - Text embeddings
- **OpenAI API** - Large language model
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI framework
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **CSS3** - Styling (no frameworks for simplicity)

### DevOps & Deployment
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Frontend web server
- **PostgreSQL** - Production database

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose (for containerized setup)

### Method 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd neusearch-product-assistant
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database**
   ```bash
   # Wait for services to start, then trigger data loading
   curl -X POST "http://localhost:8000/api/scraping" \\
        -H "Content-Type: application/json" \\
        -d '{"max_products": 30, "use_fallback": true}'
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Method 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL**
   ```bash
   # Install PostgreSQL and create database
   createdb neusearch_db
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and OpenAI API key
   ```

6. **Run the backend**
   ```bash
   python run.py
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

## 📊 Data Collection Pipeline

### Scraping Strategy

The application scrapes product data from **Furlenco.com** using a robust scraping pipeline:

#### Target Data Points
- **Title**: Product name
- **Price**: Pricing information in INR
- **Description**: Product description
- **Features**: Key product attributes
- **Image URL**: Product images
- **Category**: Furniture category (bedroom, living room, etc.)
- **Brand**: Manufacturer information
- **Availability**: Stock status
- **Additional Attributes**: Material, dimensions, color, etc.

#### Implementation Details

1. **Adaptive Scraping**: Multiple CSS selectors for robustness
2. **Rate Limiting**: Respectful scraping with delays
3. **Error Handling**: Graceful fallback to sample data
4. **Data Validation**: Ensures data quality before storage
5. **Fallback System**: Pre-curated product data when scraping fails

#### Scraping Endpoint
```bash
# Trigger scraping
POST /api/scraping
{
    "max_products": 30,
    "use_fallback": true
}

# Check status
GET /api/scraping/status
```

## 🧠 RAG Pipeline Design

### Vector Embeddings

The system uses **Sentence Transformers** (`all-MiniLM-L6-v2`) for creating embeddings:

1. **Text Preparation**: Combines title, description, features, and category
2. **Embedding Generation**: Creates vector representations
3. **Storage**: Persists in ChromaDB with metadata
4. **Retrieval**: Semantic similarity search for user queries

### LLM Integration

**OpenAI GPT-3.5-turbo** provides intelligent responses:

#### Capabilities
- **Query Interpretation**: Understands abstract furniture needs
- **Contextual Recommendations**: Explains why products match
- **Clarification**: Asks follow-up questions for vague queries
- **Fallback Logic**: Keyword matching when LLM is unavailable

#### Example Interactions

**User**: "I need something for both gym and meetings"
**AI**: "I'd recommend looking at versatile furniture pieces like a sleek study table that can work as a home office space for meetings and provide storage for gym equipment. Let me show you some options..."

**User**: "Small bedroom furniture"
**AI**: "For a small bedroom, space-saving furniture is key. Here are some compact options with built-in storage..."

### Search Process

1. **User Query** → Vector similarity search
2. **Relevant Products** → LLM analysis
3. **Contextual Response** → Product recommendations with explanations

## 🌐 API Documentation

### Product Endpoints

```bash
GET /api/products              # Get all products (paginated)
GET /api/products/{id}         # Get specific product
GET /api/products/category/{category}  # Get products by category
```

### Chat Endpoints

```bash
POST /api/chat                 # Send chat message
{
    "message": "Looking for bedroom furniture"
}

GET /api/chat/search/{query}   # Direct product search
```

### Scraping Endpoints

```bash
POST /api/scraping            # Trigger scraping
GET /api/scraping/status      # Get scraping status
```

### Response Format

```json
{
    "response_type": "recommendation",
    "message": "Here are some great bedroom options for you...",
    "products": [
        {
            "id": 1,
            "title": "Archer Queen Bed with Storage",
            "price": 12999,
            "description": "Queen size bed with built-in storage...",
            "features": ["Queen Size", "Storage Compartments"],
            "image_url": "https://...",
            "category": "Bedroom",
            "brand": "Furlenco"
        }
    ]
}
```

## 🚀 Deployment

### Production Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# OpenAI
OPENAI_API_KEY=sk-your-api-key-here

# Vector Database
CHROMA_PERSIST_DIRECTORY=/app/chroma_db

# Frontend
REACT_APP_API_URL=https://your-api-domain.com/api
```

### Deployment Platforms

The application is designed to work with various deployment platforms:

#### Recommended Platforms
- **Railway** - Full-stack deployment with PostgreSQL
- **Render** - Web services with managed PostgreSQL
- **Fly.io** - Containerized deployment
- **Vercel + Supabase** - Frontend + managed backend
- **DigitalOcean App Platform** - Managed deployment

#### Deployment Steps (Railway Example)

1. **Connect GitHub Repository**
2. **Set Environment Variables**
3. **Deploy Backend** (Python service)
4. **Deploy Frontend** (Static site)
5. **Configure PostgreSQL** (Add-on)

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `OPENAI_API_KEY` | OpenAI API key for LLM | Optional* |
| `CHROMA_PERSIST_DIRECTORY` | Vector DB storage path | No |
| `REACT_APP_API_URL` | Backend URL for frontend | Yes |

*The system works without OpenAI API key using fallback logic

### Performance Tuning

- **Vector Search**: Adjust `n_results` parameter for search
- **LLM Responses**: Configure `temperature` and `max_tokens`
- **Database**: Optimize PostgreSQL connections
- **Caching**: Add Redis for API response caching

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### Manual Testing
1. **Product Loading**: Visit homepage and load products
2. **Chat Interface**: Try various furniture queries
3. **Product Details**: Click on products for detailed views
4. **Error Handling**: Test with network issues

## 🚧 Known Issues & Limitations

### Current Limitations

1. **Scraping Dependency**: Real-time scraping may fail due to website changes
2. **LLM Costs**: OpenAI API usage incurs costs
3. **Image Loading**: Some product images may not load
4. **Mobile UX**: Chat interface could be improved for mobile

### Future Improvements

1. **Enhanced Scraping**: More robust scraping with proxy support
2. **Image Processing**: Better image handling and optimization
3. **Caching Layer**: Redis for improved performance
4. **User Accounts**: Save preferences and chat history
5. **Advanced Filters**: Price, brand, and feature filtering
6. **Recommendation Engine**: ML-based personalized recommendations

## 🏆 Design Decisions & Trade-offs

### Technical Decisions

1. **ChromaDB over Pinecone**: Self-hosted, no external dependencies
2. **Sentence Transformers**: Free alternative to OpenAI embeddings
3. **Fallback Data**: Ensures demo works without scraping
4. **Minimal UI**: Focus on functionality over aesthetics
5. **Docker First**: Easy deployment and development

### Trade-offs

| Decision | Pros | Cons |
|----------|------|------|
| Self-hosted Vector DB | Free, privacy, control | Setup complexity |
| Fallback LLM Logic | Works without API key | Limited intelligence |
| Simple CSS | Fast, lightweight | Less polished UI |
| Furlenco Focus | Deep integration | Limited product variety |

## 📈 Challenges & Solutions

### Challenge 1: Reliable Web Scraping
**Problem**: Website structure changes break scraping
**Solution**: Multiple CSS selectors, fallback data, graceful error handling

### Challenge 2: Vector Search Quality
**Problem**: Poor search results for abstract queries
**Solution**: Comprehensive text preparation, feature combination, LLM interpretation

### Challenge 3: LLM Cost Management
**Problem**: OpenAI API costs for frequent queries
**Solution**: Fallback logic, response caching, smart prompt design

### Challenge 4: Mobile Experience
**Problem**: Chat interface not optimal for mobile
**Solution**: Responsive CSS, touch-friendly interactions

## 🎯 Future Roadmap

### Short-term (1-2 weeks)
- [ ] Improved mobile responsiveness
- [ ] Error boundary components
- [ ] Loading states optimization
- [ ] API response caching

### Medium-term (1 month)
- [ ] User authentication system
- [ ] Favorite products feature
- [ ] Chat history persistence
- [ ] Advanced product filters

### Long-term (3+ months)
- [ ] Multi-website scraping
- [ ] Personalized recommendations
- [ ] Real-time inventory updates
- [ ] Voice search interface
- [ ] Augmented reality product preview

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Furlenco.com** for product data
- **OpenAI** for GPT-3.5-turbo
- **Sentence Transformers** for embeddings
- **ChromaDB** for vector storage
- **FastAPI** community for excellent documentation

---

**Built with ❤️ for Neusearch AI Technical Assignment**

For questions or support, please contact: [Your Email]