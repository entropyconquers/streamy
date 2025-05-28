#!/usr/bin/env python3
"""
Test script for the new Torrent Search API v5.0
Demonstrates the restructured API with TMDB search and detailed endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001"

def test_endpoint(endpoint, description):
    """Test an API endpoint and display results"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Endpoint: {endpoint}")
    print('='*60)
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Status: {response.status_code}")
            print(f"Response preview:")
            print(json.dumps(data, indent=2)[:1000] + "..." if len(json.dumps(data, indent=2)) > 1000 else json.dumps(data, indent=2))
        else:
            print(f"❌ Error! Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    
    time.sleep(1)  # Rate limiting

def main():
    """Test all API endpoints"""
    print("🚀 Testing Torrent Search API v5.0")
    print("New Structure: Search returns TMDB results, Details include torrents")
    
    # Test API documentation
    test_endpoint("/", "API Documentation")
    
    # Test health check
    test_endpoint("/health", "Health Check")
    
    # Test search endpoints (TMDB only, no torrents)
    test_endpoint("/search/breaking bad", "Multi Search (Movies + TV)")
    test_endpoint("/movies/inception", "Movie Search")
    test_endpoint("/tv-shows/breaking bad", "TV Show Search")
    
    # Test detail endpoints (TMDB + Torrents)
    print(f"\n{'='*60}")
    print("DETAIL ENDPOINTS (TMDB + Torrents)")
    print('='*60)
    
    # Movie details (Fight Club - TMDB ID: 550)
    test_endpoint("/details/movie/550", "Movie Details with Torrents (Fight Club)")
    
    # TV show details (Breaking Bad - TMDB ID: 1396)
    test_endpoint("/details/tv/1396", "TV Show Details with Torrents (Breaking Bad)")
    
    # Season details (Breaking Bad Season 1)
    test_endpoint("/details/tv/1396/season/1", "Season Details with Torrents (Breaking Bad S1)")
    
    # Episode details (Breaking Bad S1E1)
    test_endpoint("/details/tv/1396/season/1/episode/1", "Episode Details with Torrents (Breaking Bad S1E1)")
    
    print(f"\n{'='*60}")
    print("🎉 API Testing Complete!")
    print("New API Structure:")
    print("• Search endpoints: Return top 5 TMDB results only")
    print("• Detail endpoints: Return full TMDB details + torrent links")
    print("• Supports movies, TV shows, seasons, and episodes")
    print('='*60)

if __name__ == "__main__":
    main() 