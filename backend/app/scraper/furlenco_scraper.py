import requests
import time
from typing import List, Dict, Any
import logging
from bs4 import BeautifulSoup
import json
import re

logger = logging.getLogger(__name__)

class FurlencoScraper:
    def __init__(self):
        self.base_url = "https://furlenco.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_category_urls(self) -> List[str]:
        """Get category URLs to scrape products from"""
        try:
            response = self.session.get(f"{self.base_url}/bangalore/categories")
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find category links - this might need adjustment based on actual HTML structure
            category_links = []
            
            # Common furniture categories on Furlenco
            categories = [
                "bedroom",
                "living-room", 
                "dining-room",
                "study-room",
                "storage",
                "home-decor"
            ]
            
            for category in categories:
                category_links.append(f"{self.base_url}/bangalore/categories/{category}")
            
            return category_links
        except Exception as e:
            logger.error(f"Error getting category URLs: {e}")
            return []
    
    def scrape_product_listing_page(self, url: str) -> List[str]:
        """Scrape product URLs from a listing page"""
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            product_links = []
            
            # Look for product links - adjust selectors based on actual HTML
            # Common patterns for product links
            selectors = [
                'a[href*="/product/"]',
                'a[href*="/products/"]',
                '.product-card a',
                '.product-item a',
                '[data-testid="product-link"]'
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        if href.startswith('/'):
                            href = self.base_url + href
                        product_links.append(href)
                
                if product_links:
                    break
            
            return list(set(product_links))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Error scraping listing page {url}: {e}")
            return []
    
    def extract_price(self, text: str) -> float:
        """Extract price from text"""
        if not text:
            return 0.0
        
        # Remove common price prefixes and suffixes
        price_text = re.sub(r'[^\d.,]', '', text)
        price_text = price_text.replace(',', '')
        
        try:
            return float(price_text)
        except:
            return 0.0
    
    def scrape_product_details(self, product_url: str) -> Dict[str, Any]:
        """Scrape detailed product information"""
        try:
            response = self.session.get(product_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product details - these selectors might need adjustment
            title = ""
            price = 0.0
            description = ""
            features = []
            image_url = ""
            category = ""
            brand = "Furlenco"
            availability = "Available"
            
            # Try different selectors for title
            title_selectors = ['h1', '.product-title', '[data-testid="product-title"]', '.product-name']
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    break
            
            # Try different selectors for price
            price_selectors = ['.price', '.product-price', '[data-testid="price"]', '.current-price']
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price = self.extract_price(price_elem.get_text(strip=True))
                    break
            
            # Try different selectors for description
            desc_selectors = ['.product-description', '.description', '[data-testid="description"]']
            for selector in desc_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    description = desc_elem.get_text(strip=True)
                    break
            
            # Try to find features/specifications
            feature_selectors = ['.features li', '.specifications li', '.product-features li']
            for selector in feature_selectors:
                feature_elems = soup.select(selector)
                if feature_elems:
                    features = [elem.get_text(strip=True) for elem in feature_elems]
                    break
            
            # Try to find main product image
            img_selectors = ['.product-image img', '.main-image img', 'img[data-testid="product-image"]']
            for selector in img_selectors:
                img_elem = soup.select_one(selector)
                if img_elem:
                    img_src = img_elem.get('src') or img_elem.get('data-src')
                    if img_src:
                        if img_src.startswith('/'):
                            image_url = self.base_url + img_src
                        else:
                            image_url = img_src
                        break
            
            # Try to extract category from breadcrumbs or URL
            breadcrumb_selectors = ['.breadcrumb a', '.breadcrumbs a', '[data-testid="breadcrumb"] a']
            for selector in breadcrumb_selectors:
                breadcrumb_elems = soup.select(selector)
                if breadcrumb_elems and len(breadcrumb_elems) > 1:
                    category = breadcrumb_elems[-2].get_text(strip=True)
                    break
            
            if not category:
                # Extract from URL
                url_parts = product_url.split('/')
                if 'categories' in url_parts:
                    try:
                        category_idx = url_parts.index('categories') + 1
                        if category_idx < len(url_parts):
                            category = url_parts[category_idx].replace('-', ' ').title()
                    except:
                        pass
            
            return {
                "title": title,
                "price": price,
                "description": description,
                "features": features,
                "image_url": image_url,
                "category": category,
                "brand": brand,
                "availability": availability,
                "product_url": product_url,
                "additional_attributes": {}
            }
            
        except Exception as e:
            logger.error(f"Error scraping product {product_url}: {e}")
            return None
    
    def scrape_products(self, max_products: int = 30) -> List[Dict[str, Any]]:
        """Scrape products from Furlenco"""
        products = []
        
        try:
            # Get category URLs
            category_urls = self.get_category_urls()
            
            if not category_urls:
                # Fallback URLs if automatic detection fails
                category_urls = [
                    f"{self.base_url}/bangalore/categories/bedroom",
                    f"{self.base_url}/bangalore/categories/living-room",
                    f"{self.base_url}/bangalore/categories/dining-room"
                ]
            
            for category_url in category_urls:
                if len(products) >= max_products:
                    break
                
                logger.info(f"Scraping category: {category_url}")
                
                # Get product URLs from listing page
                product_urls = self.scrape_product_listing_page(category_url)
                
                for product_url in product_urls[:10]:  # Limit per category
                    if len(products) >= max_products:
                        break
                    
                    logger.info(f"Scraping product: {product_url}")
                    
                    product_data = self.scrape_product_details(product_url)
                    
                    if product_data and product_data.get('title') and product_data.get('price') > 0:
                        products.append(product_data)
                        logger.info(f"Successfully scraped: {product_data['title']}")
                    
                    # Rate limiting
                    time.sleep(1)
                
                # Pause between categories
                time.sleep(2)
            
        except Exception as e:
            logger.error(f"Error in scrape_products: {e}")
        
        return products

# Fallback: Static product data in case scraping fails
def get_fallback_furlenco_products() -> List[Dict[str, Any]]:
    """Fallback product data for Furlenco in case scraping fails"""
    return [
        {
            "title": "Valencia Fabric Sofa 3 Seater",
            "price": 8999.0,
            "description": "Comfortable 3-seater fabric sofa with modern design. Perfect for living rooms and family spaces.",
            "features": ["3 Seater", "Fabric Upholstery", "Modern Design", "Sturdy Frame"],
            "image_url": "https://images.furlenco.com/sofa-placeholder.jpg",
            "category": "Living Room",
            "brand": "Furlenco",
            "availability": "Available",
            "product_url": "https://furlenco.com/product/valencia-fabric-sofa",
            "additional_attributes": {"material": "Fabric", "color": "Grey"}
        },
        {
            "title": "Archer Queen Bed with Storage",
            "price": 12999.0,
            "description": "Queen size bed with built-in storage compartments. Made with high-quality engineered wood.",
            "features": ["Queen Size", "Storage Compartments", "Engineered Wood", "Hydraulic Storage"],
            "image_url": "https://images.furlenco.com/bed-placeholder.jpg",
            "category": "Bedroom",
            "brand": "Furlenco",
            "availability": "Available",
            "product_url": "https://furlenco.com/product/archer-queen-bed",
            "additional_attributes": {"size": "Queen", "material": "Engineered Wood"}
        },
        {
            "title": "Dining Table 4 Seater with Chairs",
            "price": 15999.0,
            "description": "Complete dining set with table and 4 chairs. Solid wood construction with modern finish.",
            "features": ["4 Seater", "Solid Wood", "Complete Set", "Modern Finish"],
            "image_url": "https://images.furlenco.com/dining-placeholder.jpg",
            "category": "Dining Room",
            "brand": "Furlenco", 
            "availability": "Available",
            "product_url": "https://furlenco.com/product/dining-table-4-seater",
            "additional_attributes": {"seating": "4 People", "material": "Solid Wood"}
        },
        {
            "title": "Study Table with Chair",
            "price": 6999.0,
            "description": "Ergonomic study table with matching chair. Includes storage drawers and cable management.",
            "features": ["Storage Drawers", "Cable Management", "Ergonomic Chair", "Compact Design"],
            "image_url": "https://images.furlenco.com/study-table-placeholder.jpg",
            "category": "Study Room",
            "brand": "Furlenco",
            "availability": "Available", 
            "product_url": "https://furlenco.com/product/study-table-chair",
            "additional_attributes": {"type": "Study Furniture", "includes": "Chair"}
        },
        {
            "title": "Wardrobe 3 Door with Mirror",
            "price": 18999.0,
            "description": "Spacious 3-door wardrobe with full-length mirror and hanging space. Multiple compartments for organized storage.",
            "features": ["3 Doors", "Full Length Mirror", "Hanging Space", "Multiple Compartments"],
            "image_url": "https://images.furlenco.com/wardrobe-placeholder.jpg",
            "category": "Bedroom",
            "brand": "Furlenco",
            "availability": "Available",
            "product_url": "https://furlenco.com/product/wardrobe-3-door-mirror",
            "additional_attributes": {"doors": "3", "mirror": "Yes"}
        }
    ]