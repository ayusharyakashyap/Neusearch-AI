import os
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any
import json
import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class VectorService:
    def __init__(self):
        self.chroma_persist_directory = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
        self.client = chromadb.PersistentClient(path=self.chroma_persist_directory)
        
        # Use sentence-transformers for embeddings (free alternative to OpenAI)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="products",
            embedding_function=self.embedding_function
        )
    
    def create_product_text(self, product: Dict[str, Any]) -> str:
        """Create searchable text from product data"""
        text_parts = []
        
        if product.get('title'):
            text_parts.append(f"Title: {product['title']}")
        
        if product.get('description'):
            text_parts.append(f"Description: {product['description']}")
        
        if product.get('category'):
            text_parts.append(f"Category: {product['category']}")
        
        if product.get('features') and isinstance(product['features'], list):
            features_text = ", ".join(product['features'])
            text_parts.append(f"Features: {features_text}")
        
        if product.get('brand'):
            text_parts.append(f"Brand: {product['brand']}")
        
        if product.get('additional_attributes'):
            attrs = product['additional_attributes']
            for key, value in attrs.items():
                text_parts.append(f"{key}: {value}")
        
        return " | ".join(text_parts)
    
    def add_products(self, products: List[Dict[str, Any]]):
        """Add products to vector database"""
        try:
            documents = []
            metadatas = []
            ids = []
            
            for product in products:
                # Create searchable text
                document = self.create_product_text(product)
                documents.append(document)
                
                # Store metadata (all product info except the searchable text)
                metadata = {
                    "title": product.get('title', ''),
                    "price": product.get('price', 0.0),
                    "description": product.get('description', ''),
                    "image_url": product.get('image_url', ''),
                    "category": product.get('category', ''),
                    "brand": product.get('brand', ''),
                    "availability": product.get('availability', ''),
                    "product_url": product.get('product_url', ''),
                    "features": json.dumps(product.get('features', [])),
                    "additional_attributes": json.dumps(product.get('additional_attributes', {}))
                }
                metadatas.append(metadata)
                
                # Use product ID if available, otherwise use title hash
                product_id = str(product.get('id', hash(product.get('title', ''))))
                ids.append(product_id)
            
            # Add to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(products)} products to vector database")
            
        except Exception as e:
            logger.error(f"Error adding products to vector database: {e}")
    
    def search_products(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for products using vector similarity"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            products = []
            if results['metadatas'] and len(results['metadatas']) > 0:
                for metadata in results['metadatas'][0]:
                    # Parse JSON fields back to Python objects
                    features = json.loads(metadata.get('features', '[]'))
                    additional_attributes = json.loads(metadata.get('additional_attributes', '{}'))
                    
                    product = {
                        "title": metadata.get('title'),
                        "price": metadata.get('price'),
                        "description": metadata.get('description'),
                        "image_url": metadata.get('image_url'),
                        "category": metadata.get('category'),
                        "brand": metadata.get('brand'),
                        "availability": metadata.get('availability'),
                        "product_url": metadata.get('product_url'),
                        "features": features,
                        "additional_attributes": additional_attributes
                    }
                    products.append(product)
            
            return products
            
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            return []
    
    def get_collection_count(self) -> int:
        """Get the number of products in the collection"""
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Error getting collection count: {e}")
            return 0