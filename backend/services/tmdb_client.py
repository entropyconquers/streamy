import logging
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import Config

class TMDBClient:
    """Client for The Movie Database (TMDB) API with improved error handling"""
    
    def __init__(self):
        self.api_key = Config.TMDB_API_KEY
        self.base_url = Config.TMDB_BASE_URL
        self.image_base_url = Config.TMDB_IMAGE_BASE_URL
        
        # Check if API key is configured
        if not self.api_key or self.api_key == "your_tmdb_api_key_here":
            logging.warning("TMDB API key not configured. TMDB features will be disabled.")
            self.enabled = False
            return
        
        self.enabled = True
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'accept': 'application/json',
            'User-Agent': 'TorrentSearchAPI/4.0'
        }
        
        # Configure session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def _make_request(self, url, params=None, timeout=15):
        """Make a request with improved error handling"""
        if not self.enabled:
            logging.warning("TMDB client is disabled - API key not configured")
            return None
            
        try:
            response = self.session.get(
                url, 
                headers=self.headers, 
                params=params, 
                timeout=timeout
            )
            
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 1))
                logging.warning(f"TMDB rate limit hit. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                # Retry once after rate limit
                response = self.session.get(
                    url, 
                    headers=self.headers, 
                    params=params, 
                    timeout=timeout
                )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError as e:
            logging.error(f"TMDB connection error: {e}")
            return None
        except requests.exceptions.Timeout as e:
            logging.error(f"TMDB request timeout: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logging.error("TMDB authentication failed - check your API key")
            elif e.response.status_code == 404:
                logging.warning("TMDB resource not found")
            else:
                logging.error(f"TMDB HTTP error: {e}")
            return None
        except Exception as e:
            logging.error(f"TMDB unexpected error: {e}")
            return None
    
    def search_movie(self, title):
        """Search for movies on TMDB"""
        if not self.enabled:
            return []
            
        url = f"{self.base_url}/search/movie"
        params = {
            'query': title,
            'include_adult': 'false',
            'language': 'en-US',
            'page': 1
        }
        
        data = self._make_request(url, params)
        if data:
            return data.get('results', [])[:5]  # Return top 5 results
        return []
    
    def search_tv_show(self, title):
        """Search for TV shows on TMDB"""
        if not self.enabled:
            return []
            
        url = f"{self.base_url}/search/tv"
        params = {
            'query': title,
            'include_adult': 'false',
            'language': 'en-US',
            'page': 1
        }
        
        data = self._make_request(url, params)
        if data:
            return data.get('results', [])[:5]  # Return top 5 results
        return []
    
    def search_multi(self, title):
        """Search for both movies and TV shows on TMDB"""
        if not self.enabled:
            return []
            
        url = f"{self.base_url}/search/multi"
        params = {
            'query': title,
            'include_adult': 'false',
            'language': 'en-US',
            'page': 1
        }
        
        data = self._make_request(url, params)
        if data:
            return data.get('results', [])[:5]  # Return top 5 results
        return []
    
    def get_movie_details(self, movie_id):
        """Get detailed movie information"""
        if not self.enabled:
            return None
            
        url = f"{self.base_url}/movie/{movie_id}"
        params = {'language': 'en-US'}
        
        return self._make_request(url, params)
    
    def get_movie_credits(self, movie_id):
        """Get movie credits (cast and crew)"""
        if not self.enabled:
            return None
            
        url = f"{self.base_url}/movie/{movie_id}/credits"
        params = {'language': 'en-US'}
        
        data = self._make_request(url, params)
        if data:
            # Sort cast by popularity (descending) and return top 10
            cast = sorted(data.get('cast', []), key=lambda x: x.get('popularity', 0), reverse=True)[:10]
            
            # Sort crew by popularity (descending) and return top 10
            crew = sorted(data.get('crew', []), key=lambda x: x.get('popularity', 0), reverse=True)[:10]
            
            return {
                'id': data.get('id'),
                'cast': cast,
                'crew': crew
            }
        return None
    
    def get_tv_details(self, tv_id):
        """Get detailed TV show information"""
        if not self.enabled:
            return None
            
        url = f"{self.base_url}/tv/{tv_id}"
        params = {'language': 'en-US'}
        
        return self._make_request(url, params)
    
    def get_tv_season_details(self, tv_id, season_number):
        """Get detailed TV season information"""
        if not self.enabled:
            return None
            
        url = f"{self.base_url}/tv/{tv_id}/season/{season_number}"
        params = {'language': 'en-US'}
        
        return self._make_request(url, params)
    
    def get_tv_episode_details(self, tv_id, season_number, episode_number):
        """Get detailed TV episode information"""
        if not self.enabled:
            return None
            
        url = f"{self.base_url}/tv/{tv_id}/season/{season_number}/episode/{episode_number}"
        params = {'language': 'en-US'}
        
        return self._make_request(url, params)
    
    def test_connection(self):
        """Test TMDB API connection"""
        if not self.enabled:
            return False
            
        url = f"{self.base_url}/configuration"
        data = self._make_request(url, timeout=5)
        return data is not None 