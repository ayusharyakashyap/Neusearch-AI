from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from ..scraper.furlenco_scraper import FurlencoScraper, get_fallback_furlenco_products
from ..services.vector_service import VectorService
from ..models.product import Product
from ..database import SessionLocal
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ScrapeRequest(BaseModel):
    max_products: int = 30
    use_fallback: bool = False

@router.post("/")
async def trigger_scraping(background_tasks: BackgroundTasks, request: ScrapeRequest):
    """Trigger product scraping"""
    background_tasks.add_task(scrape_and_store_products, request.max_products, request.use_fallback)
    return {"message": "Scraping started in background"}

def scrape_and_store_products(max_products: int = 30, use_fallback: bool = False):
    """Scrape products and store them in database and vector store"""
    try:
        logger.info("Starting product scraping...")
        
        if use_fallback:
            # Use fallback data
            products = get_fallback_furlenco_products()
            logger.info(f"Using fallback data: {len(products)} products")
        else:
            # Try to scrape
            scraper = FurlencoScraper()
            products = scraper.scrape_products(max_products)
            
            # If scraping fails or returns too few products, use fallback
            if len(products) < 5:
                logger.warning("Scraping returned few products, using fallback data")
                products = get_fallback_furlenco_products()
        
        # Store in database
        db = SessionLocal()
        try:
            stored_count = 0
            for product_data in products:
                # Check if product already exists
                existing_product = db.query(Product).filter(
                    Product.title == product_data['title']
                ).first()
                
                if not existing_product:
                    product = Product(
                        title=product_data['title'],
                        price=product_data['price'],
                        description=product_data['description'],
                        features=product_data['features'],
                        image_url=product_data['image_url'],
                        category=product_data['category'],
                        brand=product_data['brand'],
                        availability=product_data['availability'],
                        product_url=product_data['product_url'],
                        additional_attributes=product_data['additional_attributes']
                    )
                    db.add(product)
                    stored_count += 1
                
                # Update existing product with ID for vector storage
                if existing_product:
                    product_data['id'] = existing_product.id
            
            db.commit()
            logger.info(f"Stored {stored_count} new products in database")
            
            # Store in vector database
            vector_service = VectorService()
            vector_service.add_products(products)
            logger.info(f"Added {len(products)} products to vector database")
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error in scraping task: {e}")

@router.get("/status")
async def get_scraping_status():
    """Get current status of product database"""
    try:
        db = SessionLocal()
        try:
            product_count = db.query(Product).count()
        finally:
            db.close()
        
        vector_service = VectorService()
        vector_count = vector_service.get_collection_count()
        
        return {
            "database_products": product_count,
            "vector_products": vector_count,
            "status": "ready" if product_count > 0 else "no_data"
        }
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail="Error getting status")