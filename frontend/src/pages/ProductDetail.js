import React from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';

const ProductDetail = () => {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  
  // Get product from location state (passed from navigation)
  const product = location.state?.product;

  if (!product) {
    return (
      <div className="container">
        <div style={{ textAlign: 'center', padding: '3rem 0' }}>
          <h2>Product not found</h2>
          <p style={{ color: '#64748b', marginBottom: '2rem' }}>
            Sorry, we couldn't find the product you're looking for.
          </p>
          <button 
            className="btn btn-primary"
            onClick={() => navigate('/')}
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  const renderImage = () => {
    if (product.image_url && !product.image_url.includes('placeholder')) {
      return (
        <img 
          src={product.image_url} 
          alt={product.title}
          style={{
            width: '100%',
            maxHeight: '400px',
            objectFit: 'cover',
            borderRadius: '12px',
            background: '#e2e8f0'
          }}
          onError={(e) => {
            e.target.style.display = 'none';
            e.target.nextSibling.style.display = 'flex';
          }}
        />
      );
    }
    
    return (
      <div style={{
        width: '100%',
        height: '400px',
        background: '#e2e8f0',
        borderRadius: '12px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: '#94a3b8',
        fontSize: '1.1rem'
      }}>
        No Image Available
      </div>
    );
  };

  return (
    <div className="container" style={{ padding: '2rem 0' }}>
      {/* Back Button */}
      <button 
        onClick={() => navigate(-1)}
        style={{
          background: 'none',
          border: 'none',
          color: '#3b82f6',
          cursor: 'pointer',
          fontSize: '1rem',
          marginBottom: '2rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}
      >
        ← Back
      </button>

      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '3rem',
        alignItems: 'start'
      }}>
        {/* Product Image */}
        <div>
          {renderImage()}
          <div style={{
            width: '100%',
            height: '400px',
            background: '#e2e8f0',
            borderRadius: '12px',
            display: 'none',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#94a3b8',
            fontSize: '1.1rem'
          }}>
            No Image Available
          </div>
        </div>

        {/* Product Info */}
        <div>
          {product.category && (
            <span className="product-category" style={{ marginBottom: '1rem' }}>
              {product.category}
            </span>
          )}
          
          <h1 style={{
            fontSize: '2rem',
            fontWeight: 'bold',
            color: '#1e293b',
            marginBottom: '1rem',
            lineHeight: '1.3'
          }}>
            {product.title}
          </h1>
          
          <div style={{
            fontSize: '2rem',
            fontWeight: 'bold',
            color: '#059669',
            marginBottom: '2rem'
          }}>
            {formatPrice(product.price)}
          </div>

          {product.brand && (
            <div style={{ marginBottom: '1rem' }}>
              <strong style={{ color: '#374151' }}>Brand: </strong>
              <span style={{ color: '#64748b' }}>{product.brand}</span>
            </div>
          )}

          {product.availability && (
            <div style={{
              display: 'inline-block',
              background: product.availability === 'Available' ? '#dcfce7' : '#fef3c7',
              color: product.availability === 'Available' ? '#166534' : '#92400e',
              padding: '0.5rem 1rem',
              borderRadius: '20px',
              fontSize: '0.9rem',
              fontWeight: '500',
              marginBottom: '2rem'
            }}>
              {product.availability}
            </div>
          )}

          {product.description && (
            <div style={{ marginBottom: '2rem' }}>
              <h3 style={{ color: '#374151', marginBottom: '1rem' }}>Description</h3>
              <p style={{
                color: '#64748b',
                lineHeight: '1.6',
                fontSize: '1rem'
              }}>
                {product.description}
              </p>
            </div>
          )}

          {product.features && product.features.length > 0 && (
            <div style={{ marginBottom: '2rem' }}>
              <h3 style={{ color: '#374151', marginBottom: '1rem' }}>Features</h3>
              <ul style={{
                listStyle: 'none',
                padding: '0',
                margin: '0'
              }}>
                {product.features.map((feature, index) => (
                  <li key={index} style={{
                    color: '#64748b',
                    marginBottom: '0.5rem',
                    paddingLeft: '1.5rem',
                    position: 'relative'
                  }}>
                    <span style={{
                      position: 'absolute',
                      left: '0',
                      color: '#3b82f6'
                    }}>
                      ✓
                    </span>
                    {feature}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Action Buttons */}
          <div style={{
            display: 'flex',
            gap: '1rem',
            marginTop: '3rem'
          }}>
            {product.product_url ? (
              <a
                href={product.product_url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary"
                style={{ textDecoration: 'none' }}
              >
                View on Website
              </a>
            ) : (
              <button className="btn btn-primary">
                Contact for Details
              </button>
            )}
            
            <button 
              className="btn btn-secondary"
              onClick={() => navigate('/chat')}
            >
              Ask AI About This
            </button>
          </div>
        </div>
      </div>

      {/* Additional Product Details */}
      {product.additional_attributes && Object.keys(product.additional_attributes).length > 0 && (
        <div style={{
          marginTop: '3rem',
          padding: '2rem',
          background: 'white',
          borderRadius: '12px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05)'
        }}>
          <h3 style={{ color: '#374151', marginBottom: '1.5rem' }}>
            Additional Details
          </h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '1rem'
          }}>
            {Object.entries(product.additional_attributes).map(([key, value]) => (
              <div key={key}>
                <strong style={{ color: '#374151', textTransform: 'capitalize' }}>
                  {key.replace('_', ' ')}: 
                </strong>
                <span style={{ color: '#64748b', marginLeft: '0.5rem' }}>
                  {value}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductDetail;