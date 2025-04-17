from flask import Blueprint, jsonify, request, current_app
from ..services.news_service import NewsService
from functools import lru_cache
import datetime

news_bp = Blueprint('news', __name__)

@news_bp.route('/news', methods=['GET'])
def get_news():
    """Get supply chain related news with risk analysis.
    
    Query Parameters:
        days_back (int): Number of days to look back (default: 7)
        categories (str): Comma-separated list of categories to filter by
        risk_level (str): Filter by risk level (low, medium, high)
        
    Returns:
        JSON response containing news articles and risk analysis
    """
    try:
        # Get query parameters
        days_back = request.args.get('days_back', default=7, type=int)
        categories = request.args.get('categories', default='', type=str).split(',')
        risk_level = request.args.get('risk_level', default=None, type=str)
        
        # Initialize news service
        news_service = NewsService(
            api_key=current_app.config['NEWS_API_KEY'],
            base_url=current_app.config['NEWS_API_BASE_URL']
        )
        
        # Get news with caching
        news_data = get_cached_news(days_back, ','.join(categories), risk_level, news_service)
        
        return jsonify(news_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching news: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch news data',
            'message': str(e)
        }), 500

@lru_cache(maxsize=32)
def get_cached_news(days_back: int, categories: str, risk_level: str, news_service: NewsService) -> dict:
    """Cache news results to improve performance."""
    return news_service.get_supply_chain_news(
        days_back=days_back,
        categories=categories.split(',') if categories else None,
        risk_level=risk_level
    ) 