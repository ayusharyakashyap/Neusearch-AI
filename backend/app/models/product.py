from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    features = Column(JSON, nullable=True)  # Store features as JSON
    image_url = Column(String(1000), nullable=True)
    category = Column(String(200), nullable=True)
    brand = Column(String(200), nullable=True)
    availability = Column(String(100), nullable=True)
    product_url = Column(String(1000), nullable=True)
    additional_attributes = Column(JSON, nullable=True)  # Store any extra attributes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "description": self.description,
            "features": self.features,
            "image_url": self.image_url,
            "category": self.category,
            "brand": self.brand,
            "availability": self.availability,
            "product_url": self.product_url,
            "additional_attributes": self.additional_attributes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }