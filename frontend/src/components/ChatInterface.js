import React, { useState, useRef, useEffect } from 'react';
import { chatService } from '../services/api';
import { useNavigate } from 'react-router-dom';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  useEffect(() => {
    // Add welcome message
    setMessages([{
      type: 'assistant',
      content: "Hello! I'm your furniture shopping assistant. I can help you find the perfect furniture for your home. Try asking me something like: 'I need furniture for my living room' or 'What's good for a small bedroom?'",
      products: []
    }]);
  }, []);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // Add user message to chat
    setMessages(prev => [...prev, { type: 'user', content: userMessage }]);
    
    setIsLoading(true);
    
    try {
      const response = await chatService.sendMessage(userMessage);
      
      // Add assistant response to chat
      setMessages(prev => [...prev, {
        type: 'assistant',
        content: response.message,
        products: response.products || [],
        clarifying_questions: response.clarifying_questions || []
      }]);
      
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, {
        type: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        products: []
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleProductClick = (product) => {
    navigate(`/product/${product.id}`, { state: { product } });
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  const renderMessage = (message, index) => {
    return (
      <div key={index} className={`message ${message.type}`}>
        <div dangerouslySetInnerHTML={{ __html: message.content.replace(/\n/g, '<br>') }} />
        
        {message.products && message.products.length > 0 && (
          <div className="recommended-products">
            {message.products.map((product, productIndex) => (
              <div 
                key={productIndex} 
                className="mini-product-card"
                onClick={() => handleProductClick(product)}
              >
                {product.image_url && (
                  <img 
                    src={product.image_url} 
                    alt={product.title}
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                )}
                <h4>{product.title}</h4>
                <p>{formatPrice(product.price)}</p>
              </div>
            ))}
          </div>
        )}
        
        {message.clarifying_questions && message.clarifying_questions.length > 0 && (
          <div style={{ marginTop: '1rem' }}>
            <p><strong>Some questions to help me assist you better:</strong></p>
            <ul>
              {message.clarifying_questions.map((question, qIndex) => (
                <li key={qIndex}>{question}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="container">
      <div className="chat-container">
        <div className="chat-header">
          <h2>🛋️ Furniture Assistant</h2>
          <p style={{ margin: '0.5rem 0 0 0', color: '#64748b', fontSize: '0.9rem' }}>
            Ask me about furniture for any room or specific needs!
          </p>
        </div>
        
        <div className="chat-messages">
          {messages.map((message, index) => renderMessage(message, index))}
          
          {isLoading && (
            <div className="message assistant">
              <div className="loading">Thinking</div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        <div className="chat-input-container">
          <input
            type="text"
            className="chat-input"
            placeholder="Ask about furniture, room setups, or specific needs..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
          />
          <button 
            className="send-button"
            onClick={handleSendMessage}
            disabled={isLoading || !inputMessage.trim()}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;