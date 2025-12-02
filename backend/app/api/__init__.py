from .products import router as products_router
from .chat import router as chat_router
from .scraping import router as scraping_router

__all__ = ["products_router", "chat_router", "scraping_router"]