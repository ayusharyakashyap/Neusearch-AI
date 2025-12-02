from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from ..services.vector_service import VectorService
from ..services.llm_service import LLMService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
vector_service = VectorService()
llm_service = LLMService()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response_type: str
    message: str
    products: List[Dict[str, Any]] = []
    clarifying_questions: List[str] = []

@router.post("/", response_model=ChatResponse)
async def chat_with_assistant(chat_message: ChatMessage):
    """Chat with the AI assistant for product recommendations"""
    try:
        user_query = chat_message.message.strip()
        
        if not user_query:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Search for relevant products using vector similarity
        relevant_products = vector_service.search_products(user_query, n_results=8)
        
        if not relevant_products:
            return ChatResponse(
                response_type="no_results",
                message="I'm sorry, I couldn't find any products matching your query. Could you try describing what you're looking for in a different way?",
                products=[],
                clarifying_questions=["What type of furniture are you looking for?", "What room is this for?"]
            )
        
        # Use LLM to interpret query and provide recommendations
        llm_response = llm_service.interpret_query_and_recommend(user_query, relevant_products)
        
        return ChatResponse(
            response_type=llm_response.get("response_type", "recommendation"),
            message=llm_response.get("message", ""),
            products=llm_response.get("products", []),
            clarifying_questions=llm_response.get("clarifying_questions", [])
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/search/{query}")
async def search_products(query: str, limit: int = 10):
    """Search products by query using vector similarity"""
    try:
        products = vector_service.search_products(query, n_results=limit)
        return {"products": products}
    except Exception as e:
        logger.error(f"Error in search endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")