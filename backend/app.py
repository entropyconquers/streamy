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
    print("🎭 TMDB metadata:", "✅ Enabled" if Config.is_tmdb_enabled() else "❌ Disabled")
    print(f"🔍 Torrent site: {Config.TORRENT_SITE_DOMAIN}")
    print(f"🌐 Server: http://{Config.HOST}:{Config.API_PORT}")
    
    if not Config.is_tmdb_enabled():
        print("💡 To enable TMDB: Set TMDB_API_KEY in .env file")
    
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.API_PORT
    )

if __name__ == '__main__':
    main() 