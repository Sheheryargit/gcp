import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any

API_KEY = "cc08d16a5bd445ce891420bb1ea9d335"
BASE_URL = "https://newsapi.org/v2/everything"

def fetch_supply_chain_news(days_back: int = 1) -> List[Dict[str, Any]]:
    """
    Fetch supply chain related news articles from NewsAPI.
    
    Args:
        days_back (int): Number of days back to fetch news from. Defaults to 1.
    
    Returns:
        List[Dict]: List of news articles with title, description, source, url, and published date.
    """
    try:
        # Calculate the date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Parameters for the API request
        params = {
            'apiKey': API_KEY,
            'q': '(supply chain OR logistics OR shipping OR ports) AND (disruption OR delay OR risk OR impact)',
            'language': 'en',
            'sortBy': 'relevancy',
            'from': start_date.strftime('%Y-%m-%d'),
            'to': end_date.strftime('%Y-%m-%d')
        }
        
        # Make the API request
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the response
        data = response.json()
        
        # Format the articles
        formatted_articles = []
        for article in data.get('articles', []):
            # Safely concatenate title and description, handling None values
            title = article.get('title', '')
            description = article.get('description', '')
            article_text = f"{title} {description}".strip()
            
            formatted_article = {
                'title': title,
                'description': description,
                'source': article.get('source', {}).get('name', 'Unknown Source'),
                'url': article.get('url', ''),
                'published_at': article.get('publishedAt', ''),
                'relevance_tags': extract_relevance_tags(article_text)
            }
            formatted_articles.append(formatted_article)
        
        return formatted_articles[:10]  # Return top 10 most relevant articles
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def extract_relevance_tags(text: str) -> List[str]:
    """
    Extract relevant tags from article text to categorize the type of supply chain news.
    
    Args:
        text (str): The article text to analyze
    
    Returns:
        List[str]: List of relevant tags
    """
    tags = []
    
    # Keywords for different categories
    categories = {
        'Transportation': ['shipping', 'ports', 'vessels', 'containers', 'freight'],
        'Manufacturing': ['production', 'factory', 'manufacturing', 'assembly'],
        'Inventory': ['stock', 'inventory', 'warehouse', 'storage'],
        'Risk': ['disruption', 'delay', 'shortage', 'crisis', 'risk'],
        'Technology': ['digital', 'automation', 'AI', 'technology'],
        'Sustainability': ['green', 'sustainable', 'environmental', 'carbon']
    }
    
    # Check for keywords in text
    text_lower = text.lower()
    for category, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            tags.append(category)
    
    return tags

if __name__ == "__main__":
    # Test the function
    articles = fetch_supply_chain_news(days_back=2)
    for article in articles:
        print(f"\nTitle: {article['title']}")
        print(f"Tags: {article['relevance_tags']}")
        print(f"Source: {article['source']}")
        print("-" * 80) 