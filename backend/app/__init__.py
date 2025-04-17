from flask import Flask
from flask_cors import CORS
from flask_caching import Cache

# Initialize extensions
cache = Cache()

def create_app(config_object='config.DevelopmentConfig'):
    """Create and configure the Flask application.
    
    Args:
        config_object: Configuration object to use.
    
    Returns:
        Flask application instance.
    """
    app = Flask(__name__)
    
    # Load configuration
    if isinstance(config_object, str):
        app.config.from_object(config_object)
    else:
        app.config.update(config_object)
    
    # Initialize extensions
    CORS(app, origins=app.config['CORS_ORIGINS'])
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    
    # Register blueprints
    from .routes import news_bp, risk_bp
    app.register_blueprint(news_bp, url_prefix=app.config['API_PREFIX'])
    app.register_blueprint(risk_bp, url_prefix=app.config['API_PREFIX'])
    
    return app
