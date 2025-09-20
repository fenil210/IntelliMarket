from flask import Flask
from flask_cors import CORS
from config import Config
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Setup CORS
    CORS(app, origins=Config.CORS_ORIGINS)
    
    # Setup logging
    logger = Config.setup_logging()
    
    # Validate configuration
    try:
        Config.validate()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
    
    # Register blueprints
    from api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/health')
    def health_check():
        return {"status": "healthy", "service": "IntelliMarket API"}
    
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Endpoint not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return {"error": "Internal server error"}, 500
    
    logger.info("IntelliMarket API initialized successfully")
    return app