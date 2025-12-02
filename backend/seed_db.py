#!/usr/bin/env python3
"""
Seed database with fallback demo products.
Safe to run multiple times - will skip duplicates.
"""
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.product import Product, Base

def load_fallback_data():
    """Load products from JSON file."""
    json_path = Path(__file__).parent / "sample_data" / "products_fallback.json"
    with open(json_path, 'r') as f:
        return json.load(f)

def seed_database(database_url: str = None):
    """Seed database with demo products."""
    # Get database URL from environment or parameter
    db_url = database_url or os.getenv('DATABASE_URL')
    
    if not db_url:
        print("❌ No DATABASE_URL provided. Skipping seed.")
        return False
    
    # Handle Railway/Render postgres:// to postgresql://
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        # Create engine and session
        engine = create_engine(db_url)
        SessionLocal = sessionmaker(bind=engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Load and insert products
        products_data = load_fallback_data()
        session = SessionLocal()
        
        inserted_count = 0
        skipped_count = 0
        
        for product_dict in products_data:
            # Check if product already exists
            existing = session.query(Product).filter_by(id=product_dict['id']).first()
            
            if existing:
                skipped_count += 1
                continue
            
            # Create new product
            product = Product(
                id=product_dict['id'],
                title=product_dict['title'],
                price=product_dict['price'],
                description=product_dict['description'],
                features=product_dict['features'],
                image_url=product_dict['image_url'],
                category=product_dict['category'],
                brand=product_dict['brand'],
                availability=product_dict['availability']
            )
            session.add(product)
            inserted_count += 1
        
        session.commit()
        session.close()
        
        print(f"✅ Seed complete: {inserted_count} inserted, {skipped_count} skipped")
        return True
        
    except Exception as e:
        print(f"❌ Seed failed: {e}")
        return False

if __name__ == "__main__":
    # Allow passing DATABASE_URL as command line argument
    db_url = sys.argv[1] if len(sys.argv) > 1 else None
    success = seed_database(db_url)
    sys.exit(0 if success else 1)
