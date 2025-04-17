import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
from ..utils.api_utils import calculate_risk_score, extract_entities, categorize_content

class NewsService:
    def __init__(self, api_key: str, base_url: str):
        """Initialize the news service.
        
        Args:
            api_key: News API key
            base_url: Base URL for the News API
        """
        self.api_key = api_key
        self.base_url = base_url

    def get_supply_chain_news(self, days_back: int = 7, categories: List[str] = None) -> Dict[str, Any]:
        """Fetch and analyze supply chain related news.
        
        Args:
            days_back: Number of days to look back
            categories: List of categories to filter by
            
        Returns:
            Dictionary containing processed news articles and metadata
        """
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Prepare API parameters
            params = {
                'apiKey': self.api_key,
                'q': '(supply chain OR logistics OR shipping OR ports) AND (disruption OR delay OR risk OR impact)',
                'language': 'en',
                'sortBy': 'relevancy',
                'from': start_date.strftime('%Y-%m-%d'),
                'to': end_date.strftime('%Y-%m-%d')
            }
            
            # Make API request
            response = requests.get(f"{self.base_url}/everything", params=params)
            response.raise_for_status()
            data = response.json()
            
            # Process articles
            processed_articles = []
            risk_distribution = {'high': 0, 'medium': 0, 'low': 0}
            
            for article in data.get('articles', []):
                # Extract text for analysis
                text = f"{article.get('title', '')} {article.get('description', '')}"
                
                # Calculate risk score
                risk_score = calculate_risk_score(text)
                
                # Determine risk level
                risk_level = self._determine_risk_level(risk_score)
                risk_distribution[risk_level] += 1
                
                # Extract entities and categories
                entities = extract_entities(text)
                article_categories = categorize_content(text)
                
                # Filter by categories if specified
                if categories and not any(cat in article_categories for cat in categories):
                    continue
                
                processed_article = {
                    'id': hash(article.get('url', '')),
                    'title': article.get('title'),
                    'summary': article.get('description'),
                    'source': article.get('source', {}).get('name'),
                    'published_at': article.get('publishedAt'),
                    'url': article.get('url'),
                    'risk_score': risk_score,
                    'risk_level': risk_level,
                    'categories': article_categories,
                    'entities': entities,
                    'impact_analysis': {
                        'severity': risk_level.capitalize(),
                        'affected_regions': entities.get('locations', []),
                        'supply_chain_segments': self._identify_segments(text)
                    }
                }
                processed_articles.append(processed_article)
            
            return {
                'status': 'success',
                'data': {
                    'articles': processed_articles[:10],  # Return top 10 most relevant
                    'meta': {
                        'total_count': len(data.get('articles', [])),
                        'filtered_count': len(processed_articles),
                        'risk_distribution': risk_distribution
                    }
                }
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'message': f'Failed to fetch news: {str(e)}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'An unexpected error occurred: {str(e)}'
            }
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """Determine risk level based on risk score."""
        if risk_score >= 0.7:
            return 'high'
        elif risk_score >= 0.4:
            return 'medium'
        return 'low'
    
    def _identify_segments(self, text: str) -> List[str]:
        """Identify affected supply chain segments from text."""
        segments = []
        keywords = {
            'Maritime': ['port', 'shipping', 'vessel', 'container', 'maritime'],
            'Manufacturing': ['factory', 'production', 'assembly', 'manufacturing'],
            'Logistics': ['warehouse', 'distribution', 'logistics', 'transportation'],
            'Sourcing': ['supplier', 'procurement', 'sourcing', 'vendor']
        }
        
        text_lower = text.lower()
        for segment, words in keywords.items():
            if any(word in text_lower for word in words):
                segments.append(segment)
        
        return segments 