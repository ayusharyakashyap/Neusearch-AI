from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from pathlib import Path
from ..database import get_db
from ..models.product import Product

router = APIRouter()

def load_fallback_products():
    """Load products from fallback JSON file."""
    json_path = Path(__file__).parent.parent.parent / "sample_data" / "products_fallback.json"
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except Exception:
        return []

@router.get("/", response_model=List[dict])
async def get_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all products with pagination. Falls back to JSON if DB unavailable."""
    try:
        products = db.query(Product).offset(skip).limit(limit).all()
        if products:
            return [product.to_dict() for product in products]
        # If DB is empty, return fallback data
        return load_fallback_products()[skip:skip+limit]
    except Exception:
        # If DB connection fails, return fallback data
        return load_fallback_products()[skip:skip+limit]

@router.get("/{product_id}", response_model=dict)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID. Falls back to JSON if DB unavailable."""
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            return product.to_dict()
    except Exception:
@router.get("/category/{category}")
async def get_products_by_category(category: str, db: Session = Depends(get_db)):
    """Get products by category. Falls back to JSON if DB unavailable."""
    try:
        products = db.query(Product).filter(Product.category.ilike(f"%{category}%")).all()
        if products:
            return [product.to_dict() for product in products]
    except Exception:
        pass
    
    # Fallback to JSON data
    fallback_products = load_fallback_products()
    return [p for p in fallback_products if category.lower() in p.get('category', '').lower()]
        if p.get('id') == product_id:
            return p
    
    raise HTTPException(status_code=404, detail="Product not found")

@router.get("/category/{category}")
async def get_products_by_category(category: str, db: Session = Depends(get_db)):
    """Get products by category"""
    products = db.query(Product).filter(Product.category.ilike(f"%{category}%")).all()
    return [product.to_dict() for product in products]