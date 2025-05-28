import logging
import requests
from config import Config

class TMDBClient:
    """Client for The Movie Database (TMDB) API"""
    
    def __init__(self):
        self.api_key = Config.TMDB_API_KEY
        self.base_url = Config.TMDB_BASE_URL
        self.image_base_url = Config.TMDB_IMAGE_BASE_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'accept': 'application/json'
        }
    
    def search_movie(self, title):
        """Search for movies on TMDB"""
        try:
            url = f"{self.base_url}/search/movie"
            params = {
                'query': title,
                'include_adult': 'false',
                'language': 'en-US',
                'page': 1
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return data.get('results', [])[:5]  # Return top 5 results
        except Exception as e:
            logging.error(f'TMDB movie search failed: {e}')
            return []
    
    def search_tv_show(self, title):
        """Search for TV shows on TMDB"""
        try:
            url = f"{self.base_url}/search/tv"
            params = {
                'query': title,
                'include_adult': 'false',
                'language': 'en-US',
                'page': 1
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return data.get('results', [])[:5]  # Return top 5 results
        except Exception as e:
            logging.error(f'TMDB TV search failed: {e}')
            return []
    
    def search_multi(self, title):
        """Search for both movies and TV shows on TMDB"""
        try:
            url = f"{self.base_url}/search/multi"
            params = {
                'query': title,
                'include_adult': 'false',
                'language': 'en-US',
                'page': 1
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return data.get('results', [])[:5]  # Return top 5 results
        except Exception as e:
            logging.error(f'TMDB multi search failed: {e}')
            return []
    
    def get_movie_details(self, movie_id):
        """Get detailed movie information"""
        try:
            url = f"{self.base_url}/movie/{movie_id}"
            params = {
                'language': 'en-US'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f'TMDB movie details failed: {e}')
            return None
    
    def get_movie_credits(self, movie_id):
        """Get movie credits (cast and crew)"""
        try:
            url = f"{self.base_url}/movie/{movie_id}/credits"
            params = {
                'language': 'en-US'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Sort cast by popularity (descending) and return top 10
            cast = sorted(data.get('cast', []), key=lambda x: x.get('popularity', 0), reverse=True)[:10]
            
            # Sort crew by popularity (descending) and return top 10
            crew = sorted(data.get('crew', []), key=lambda x: x.get('popularity', 0), reverse=True)[:10]
            
            return {
                'id': data.get('id'),
                'cast': cast,
                'crew': crew
            }
        except Exception as e:
            logging.error(f'TMDB movie credits failed: {e}')
            return None
    
    def get_tv_details(self, tv_id):
        """Get detailed TV show information"""
        try:
            url = f"{self.base_url}/tv/{tv_id}"
            params = {
                'language': 'en-US'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f'TMDB TV details failed: {e}')
            return None
    
    def get_tv_season_details(self, tv_id, season_number):
        """Get detailed TV season information"""
        try:
            url = f"{self.base_url}/tv/{tv_id}/season/{season_number}"
            params = {
                'language': 'en-US'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f'TMDB TV season details failed: {e}')
            return None
    
    def get_tv_episode_details(self, tv_id, season_number, episode_number):
        """Get detailed TV episode information"""
        try:
            url = f"{self.base_url}/tv/{tv_id}/season/{season_number}/episode/{episode_number}"
            params = {
                'language': 'en-US'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f'TMDB TV episode details failed: {e}')
            return None
    
    def test_connection(self):
        """Test TMDB API connection"""
        try:
            url = f"{self.base_url}/configuration"
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200
        except:
            return False 