import os

class Config:
    """Base configuration."""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    
    # API Keys
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY', 'cc08d16a5bd445ce891420bb1ea9d335')
    
    # API Settings
    API_PREFIX = '/api/v1'
    
    # News API Settings
    NEWS_API_BASE_URL = 'https://newsapi.org/v2'
    NEWS_CACHE_TIMEOUT = 300  # 5 minutes
    
    # CORS Settings
    CORS_ORIGINS = ['http://localhost:8501']  # Allow Streamlit dev server

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
