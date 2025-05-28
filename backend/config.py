import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # TMDB API Configuration
    TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
    TMDB_BASE_URL = os.getenv('TMDB_BASE_URL', 'https://api.themoviedb.org/3')
    TMDB_IMAGE_BASE_URL = os.getenv('TMDB_IMAGE_BASE_URL', 'https://image.tmdb.org/t/p/w500')
    
    # Torrent Site Configuration
    TORRENT_SITE_DOMAIN = os.getenv('TORRENT_SITE_DOMAIN', 'tpirbay.site')
    
    # API Configuration
    API_PORT = int(os.getenv('API_PORT', '8001'))
    
    # Flask Configuration
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    
    @classmethod
    def is_tmdb_enabled(cls):
        """Check if TMDB is properly configured"""
        return bool(cls.TMDB_API_KEY and cls.TMDB_API_KEY != "your_tmdb_api_key_here") 