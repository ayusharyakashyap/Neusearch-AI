from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.product import Product

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all products with pagination"""
    products = db.query(Product).offset(skip).limit(limit).all()
    return [product.to_dict() for product in products]

@router.get("/{product_id}", response_model=dict)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.to_dict()

@router.get("/category/{category}")
async def get_products_by_category(category: str, db: Session = Depends(get_db)):
    """Get products by category"""
    products = db.query(Product).filter(Product.category.ilike(f"%{category}%")).all()
    return [product.to_dict() for product in products]