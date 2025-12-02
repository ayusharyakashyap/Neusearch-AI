from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from .database import engine
from .models import Base
from .api import products_router, chat_router, scraping_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Neusearch Product Assistant API",
    description="AI-powered product discovery assistant for furniture and home decor",
    version="1.0.0"
)

# Configure CORS - Allow all origins for easy deployment
# SECURITY NOTE: In production, replace ["*"] with your actual frontend domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo - lock down in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products_router, prefix="/api/products", tags=["products"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(scraping_router, prefix="/api/scraping", tags=["scraping"])

@app.get("/")
async def root():
    return {"message": "Neusearch Product Assistant API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/api/health")
async def api_health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)