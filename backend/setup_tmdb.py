#!/usr/bin/env python3
"""
TMDB Setup Script
Helps users configure their TMDB API key for the Torrent Search API
"""

import os
import sys

def create_env_file():
    """Create or update .env file with TMDB configuration"""
    
    print("🎬 TMDB Setup for Torrent Search API")
    print("=" * 50)
    print()
    
    # Check if .env already exists
    env_exists = os.path.exists('.env')
    if env_exists:
        print("📁 Found existing .env file")
        with open('.env', 'r') as f:
            content = f.read()
            if 'TMDB_API_KEY=' in content and 'your_tmdb_api_key_here' not in content:
                print("✅ TMDB API key appears to be already configured")
                response = input("Do you want to update it? (y/N): ").lower()
                if response != 'y':
                    print("Setup cancelled.")
                    return
    
    print()
    print("To get your TMDB API key:")
    print("1. Go to https://www.themoviedb.org/")
    print("2. Create a free account")
    print("3. Go to Settings > API")
    print("4. Request an API key (choose 'Developer')")
    print("5. Copy your API key")
    print()
    
    api_key = input("Enter your TMDB API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return
    
    if api_key == "your_tmdb_api_key_here":
        print("❌ Please enter your actual API key, not the placeholder.")
        return
    
    # Create .env content
    env_content = f"""# TMDB API Configuration
# Get your API key from: https://www.themoviedb.org/settings/api
TMDB_API_KEY={api_key}

# TMDB API URLs (usually don't need to change these)
TMDB_BASE_URL=https://api.themoviedb.org/3
TMDB_IMAGE_BASE_URL=https://image.tmdb.org/t/p/w500

# Torrent Site Configuration
TORRENT_SITE_DOMAIN=tpirbay.site

# API Configuration
API_PORT=8001
DEBUG=True
HOST=0.0.0.0
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print()
        print("✅ .env file created successfully!")
        print("🚀 You can now start the API with: python app.py")
        print()
        print("Test your setup:")
        print("- Health check: http://localhost:8001/health")
        print("- Search movies: http://localhost:8001/movies/inception")
        print("- Search TV shows: http://localhost:8001/tv-shows/breaking%20bad")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return

def test_tmdb_connection():
    """Test TMDB connection with the configured API key"""
    try:
        from services.tmdb_client import TMDBClient
        
        print("🔍 Testing TMDB connection...")
        client = TMDBClient()
        
        if not client.enabled:
            print("❌ TMDB client is disabled - API key not configured")
            return False
        
        if client.test_connection():
            print("✅ TMDB connection successful!")
            
            # Test a simple search
            print("🎬 Testing movie search...")
            results = client.search_movie("inception")
            if results:
                print(f"✅ Found {len(results)} results for 'inception'")
                print(f"   First result: {results[0].get('title', 'Unknown')}")
            else:
                print("⚠️  No results found, but connection is working")
            
            return True
        else:
            print("❌ TMDB connection failed - check your API key")
            return False
            
    except Exception as e:
        print(f"❌ Error testing TMDB connection: {e}")
        return False

def main():
    """Main setup function"""
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test_tmdb_connection()
    else:
        create_env_file()
        print()
        if input("Test the connection now? (Y/n): ").lower() != 'n':
            test_tmdb_connection()

if __name__ == '__main__':
    main() 