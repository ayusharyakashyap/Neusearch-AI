import os
import openai
from typing import List, Dict, Any, Optional
import logging
import json

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
    def interpret_query_and_recommend(self, user_query: str, relevant_products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Use LLM to interpret user query and provide recommendations"""
        try:
            if not self.openai_api_key:
                # Fallback response when OpenAI API key is not available
                return self._fallback_recommendation(user_query, relevant_products)
            
            # Create product context for LLM
            products_context = self._format_products_for_llm(relevant_products)
            
            system_prompt = """You are a helpful furniture and home decor shopping assistant. Your job is to:
1. Understand abstract and nuanced user queries about furniture needs
2. Match products from the available inventory to user requirements
3. Provide thoughtful explanations for recommendations
4. Ask clarifying questions when needed

Guidelines:
- Be conversational and helpful
- Explain why you recommend specific products
- Consider user's lifestyle, space, and usage patterns
- If query is too vague, ask 1-2 specific questions to clarify
- Focus on matching functional needs over just keywords
- Suggest 2-4 relevant products maximum
- Include price information in recommendations
"""

            user_prompt = f"""
User Query: "{user_query}"

Available Products:
{products_context}

Please provide a helpful response that either:
1. Recommends specific products with explanations, OR
2. Asks clarifying questions if the query is too vague

Format your response as JSON with this structure:
{{
    "response_type": "recommendation" or "clarification",
    "message": "Your conversational response to the user",
    "recommended_products": [list of product titles if recommending],
    "clarifying_questions": [list of questions if seeking clarification]
}}
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse LLM response
            llm_response = response.choices[0].message.content.strip()
            
            try:
                parsed_response = json.loads(llm_response)
                return self._process_llm_response(parsed_response, relevant_products)
            except json.JSONDecodeError:
                # If JSON parsing fails, create a simple recommendation
                return {
                    "response_type": "recommendation",
                    "message": llm_response,
                    "products": relevant_products[:3]
                }
                
        except Exception as e:
            logger.error(f"Error in LLM service: {e}")
            return self._fallback_recommendation(user_query, relevant_products)
    
    def _format_products_for_llm(self, products: List[Dict[str, Any]]) -> str:
        """Format products for LLM context"""
        formatted_products = []
        
        for i, product in enumerate(products, 1):
            features = product.get('features', [])
            features_text = ", ".join(features) if features else "No features listed"
            
            product_text = f"""
{i}. {product.get('title', 'Unknown Product')}
   Price: ₹{product.get('price', 0)}
   Category: {product.get('category', 'Unknown')}
   Description: {product.get('description', 'No description')[:150]}
   Features: {features_text}
"""
            formatted_products.append(product_text)
        
        return "\n".join(formatted_products)
    
    def _process_llm_response(self, parsed_response: Dict[str, Any], all_products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process and validate LLM response"""
        response_type = parsed_response.get('response_type', 'recommendation')
        message = parsed_response.get('message', '')
        
        result = {
            "response_type": response_type,
            "message": message
        }
        
        if response_type == "recommendation":
            recommended_titles = parsed_response.get('recommended_products', [])
            recommended_products = []
            
            # Find products by title
            for title in recommended_titles:
                for product in all_products:
                    if title.lower() in product.get('title', '').lower():
                        recommended_products.append(product)
                        break
            
            # If no specific products matched, return first few products
            if not recommended_products:
                recommended_products = all_products[:3]
            
            result["products"] = recommended_products
        
        elif response_type == "clarification":
            result["clarifying_questions"] = parsed_response.get('clarifying_questions', [])
        
        return result
    
    def _fallback_recommendation(self, user_query: str, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback recommendation when LLM is not available"""
        query_lower = user_query.lower()
        
        # Simple keyword matching for common queries
        if any(word in query_lower for word in ['bedroom', 'bed', 'sleep']):
            filtered_products = [p for p in products if 'bedroom' in p.get('category', '').lower() or 'bed' in p.get('title', '').lower()]
            message = "I found some bedroom furniture that might work for you. These pieces are popular for creating comfortable sleeping spaces."
        
        elif any(word in query_lower for word in ['living', 'sofa', 'couch', 'seating']):
            filtered_products = [p for p in products if 'living' in p.get('category', '').lower() or 'sofa' in p.get('title', '').lower()]
            message = "Here are some living room options that would be great for relaxation and entertaining guests."
        
        elif any(word in query_lower for word in ['dining', 'eat', 'table', 'chair']):
            filtered_products = [p for p in products if 'dining' in p.get('category', '').lower() or 'table' in p.get('title', '').lower()]
            message = "I found some dining furniture perfect for meals and family time."
        
        elif any(word in query_lower for word in ['study', 'work', 'office', 'desk']):
            filtered_products = [p for p in products if 'study' in p.get('category', '').lower() or any(word in p.get('title', '').lower() for word in ['study', 'desk', 'table'])]
            message = "Here are some study/work furniture options to help you be productive."
        
        elif any(word in query_lower for word in ['storage', 'organize', 'wardrobe']):
            filtered_products = [p for p in products if any(word in p.get('title', '').lower() for word in ['storage', 'wardrobe', 'cabinet'])]
            message = "These storage solutions can help you organize your space efficiently."
        
        else:
            filtered_products = products[:3]
            message = f"Based on your query '{user_query}', here are some furniture options that might interest you."
        
        return {
            "response_type": "recommendation",
            "message": message,
            "products": filtered_products[:4]  # Limit to 4 products
        }