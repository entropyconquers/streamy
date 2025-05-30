#!/usr/bin/env python3
"""
Torrent Search API v4.0
Clean, modular torrent search API with TMDB metadata integration
"""

import logging
from flask import Flask
from config import Config
from routes.search_routes import search_bp
from routes.health_routes import health_bp
from services.tmdb_client import TMDBClient

# Configure logging
logging.basicConfig(
    level=logging.WARNING, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(search_bp)
    app.register_blueprint(health_bp)
    
    return app

def main():
    """Main entry point"""
    app = create_app()
    
    print("🚀 Starting Torrent Search API v4.0...")
    print("📁 Modular architecture enabled")
    
    # Test TMDB configuration
    tmdb_client = TMDBClient()
    if tmdb_client.enabled:
        print("🎭 TMDB metadata: ✅ Enabled")
        if tmdb_client.test_connection():
            print("🔗 TMDB connection: ✅ Connected")
        else:
            print("🔗 TMDB connection: ❌ Failed (check your API key)")
    else:
        print("🎭 TMDB metadata: ❌ Disabled (API key not configured)")
        print("💡 To enable TMDB: Run 'python setup_tmdb.py' or set TMDB_API_KEY in .env file")
    
    print(f"🔍 Torrent site: {Config.TORRENT_SITE_DOMAIN}")
    print(f"🌐 Server: http://{Config.HOST}:{Config.API_PORT}")
    print()
    print("📖 API Documentation: http://localhost:8001/")
    print("🏥 Health Check: http://localhost:8001/health")
    print()
    
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.API_PORT
    )

if __name__ == '__main__':
    main() 