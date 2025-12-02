import React from 'react';

const ProductCard = ({ product, onClick }) => {
  const handleClick = () => {
    if (onClick) {
      onClick(product);
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  const renderImage = () => {
    if (product.image_url && product.image_url !== 'https://images.furlenco.com/sofa-placeholder.jpg') {
      return (
        <img 
          src={product.image_url} 
          alt={product.title}
          className="product-image"
          onError={(e) => {
            e.target.style.display = 'none';
            e.target.nextSibling.style.display = 'flex';
          }}
        />
      );
    }
    
    return (
      <div className="product-image">
        No Image Available
      </div>
    );
  };

  return (
    <div className="product-card" onClick={handleClick}>
      {renderImage()}
      <div className="product-image" style={{ display: 'none' }}>
        No Image Available
      </div>
      
      <div className="product-info">
        <h3 className="product-title">{product.title}</h3>
        <div className="product-price">{formatPrice(product.price)}</div>
        
        {product.category && (
          <span className="product-category">{product.category}</span>
        )}
        
        {product.description && (
          <p className="product-description">{product.description}</p>
        )}
        
        {product.features && product.features.length > 0 && (
          <div style={{ marginTop: '0.5rem' }}>
            <small style={{ color: '#64748b' }}>
              {product.features.slice(0, 3).join(' • ')}
            </small>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductCard;