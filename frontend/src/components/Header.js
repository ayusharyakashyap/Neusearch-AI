import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Header = () => {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path ? 'nav-link active' : 'nav-link';
  };

  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <Link to="/" className="logo">
            Neusearch
          </Link>
          
          <nav className="nav">
            <Link to="/" className={isActive('/')}>
              Home
            </Link>
            <Link to="/chat" className={isActive('/chat')}>
              Chat Assistant
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;