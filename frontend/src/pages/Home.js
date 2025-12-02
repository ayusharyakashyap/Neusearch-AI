import React, { useState, useEffect } from 'react';
import { productService, scrapingService } from '../services/api';
import ProductCard from '../components/ProductCard';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [scrapingStatus, setScrapingStatus] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadProducts();
    checkScrapingStatus();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const data = await productService.getAllProducts();
      setProducts(data);
    } catch (err) {
      setError('Failed to load products');
      console.error('Error loading products:', err);
    } finally {
      setLoading(false);
    }
  };

  const checkScrapingStatus = async () => {
    try {
      const status = await scrapingService.getScrapingStatus();
      setScrapingStatus(status);
      
      // If no products, trigger scraping with fallback data
      if (status.database_products === 0) {
        await handleTriggerScraping();
      }
    } catch (err) {
      console.error('Error checking scraping status:', err);
    }
  };

  const handleTriggerScraping = async () => {
    try {
      await scrapingService.triggerScraping(30, true); // Use fallback data
      
      // Wait a bit and reload products
      setTimeout(() => {
        loadProducts();
        checkScrapingStatus();
      }, 3000);
      
    } catch (err) {
      console.error('Error triggering scraping:', err);
    }
  };

  const handleProductClick = (product) => {
    navigate(`/product/${product.id}`, { state: { product } });
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading products...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="error">
          {error}
          <br />
          <button 
            className="btn btn-primary" 
            onClick={loadProducts}
            style={{ marginTop: '1rem' }}
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      {/* Header Section */}
      <section style={{ textAlign: 'center', padding: '3rem 0 2rem 0' }}>
        <h1 style={{ 
          fontSize: '2.5rem', 
          fontWeight: 'bold', 
          color: '#1e293b', 
          marginBottom: '1rem' 
        }}>
          Find Your Perfect Furniture
        </h1>
        <p style={{ 
          fontSize: '1.1rem', 
          color: '#64748b', 
          marginBottom: '2rem',
          maxWidth: '600px',
          margin: '0 auto 2rem auto'
        }}>
          Discover quality furniture for every room in your home. 
          Use our AI assistant to get personalized recommendations.
        </p>
        
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <button 
            className="btn btn-primary"
            onClick={() => navigate('/chat')}
          >
            🤖 Chat with AI Assistant
          </button>
          
          {scrapingStatus && scrapingStatus.database_products === 0 && (
            <button 
              className="btn btn-secondary"
              onClick={handleTriggerScraping}
            >
              Load Sample Products
            </button>
          )}
        </div>
      </section>

      {/* Status Info */}
      {scrapingStatus && (
        <div style={{ 
          background: '#f1f5f9', 
          padding: '1rem', 
          borderRadius: '8px', 
          marginBottom: '2rem',
          textAlign: 'center',
          color: '#475569'
        }}>
          <small>
            Database: {scrapingStatus.database_products} products | 
            Vector Store: {scrapingStatus.vector_products} products
          </small>
        </div>
      )}

      {/* Products Grid */}
      {products.length > 0 ? (
        <>
          <h2 style={{ 
            color: '#1e293b', 
            marginBottom: '2rem',
            textAlign: 'center' 
          }}>
            Featured Products ({products.length})
          </h2>
          
          <div className="products-grid">
            {products.map((product, index) => (
              <ProductCard 
                key={product.id || index} 
                product={product} 
                onClick={handleProductClick}
              />
            ))}
          </div>
        </>
      ) : (
        <div style={{ textAlign: 'center', padding: '3rem 0' }}>
          <h3 style={{ color: '#64748b', marginBottom: '1rem' }}>
            No products available yet
          </h3>
          <p style={{ color: '#94a3b8', marginBottom: '2rem' }}>
            Click the button below to load sample products or try the AI assistant.
          </p>
          <button 
            className="btn btn-primary"
            onClick={handleTriggerScraping}
          >
            Load Sample Products
          </button>
        </div>
      )}

      {/* Call to Action */}
      <section style={{ 
        textAlign: 'center', 
        padding: '4rem 0',
        background: 'white',
        margin: '3rem 0',
        borderRadius: '12px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)'
      }}>
        <h3 style={{ color: '#1e293b', marginBottom: '1rem' }}>
          Need Help Finding the Right Furniture?
        </h3>
        <p style={{ color: '#64748b', marginBottom: '2rem' }}>
          Our AI assistant can help you find exactly what you're looking for based on your needs.
        </p>
        <button 
          className="btn btn-primary"
          onClick={() => navigate('/chat')}
        >
          Start Chatting Now
        </button>
      </section>
    </div>
  );
};

export default Home;