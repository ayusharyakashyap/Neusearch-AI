import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const productService = {
  // Get all products
  getAllProducts: async (skip = 0, limit = 100) => {
    const response = await api.get(`/products?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  // Get product by ID
  getProduct: async (id) => {
    const response = await api.get(`/products/${id}`);
    return response.data;
  },

  // Get products by category
  getProductsByCategory: async (category) => {
    const response = await api.get(`/products/category/${category}`);
    return response.data;
  },

  // Search products
  searchProducts: async (query) => {
    const response = await api.get(`/chat/search/${encodeURIComponent(query)}`);
    return response.data;
  },
};

export const chatService = {
  // Send chat message
  sendMessage: async (message) => {
    const response = await api.post('/chat', { message });
    return response.data;
  },
};

export const scrapingService = {
  // Trigger scraping
  triggerScraping: async (maxProducts = 30, useFallback = true) => {
    const response = await api.post('/scraping', { 
      max_products: maxProducts, 
      use_fallback: useFallback 
    });
    return response.data;
  },

  // Get scraping status
  getScrapingStatus: async () => {
    const response = await api.get('/scraping/status');
    return response.data;
  },
};

export default api;