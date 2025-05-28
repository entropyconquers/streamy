import re
import logging
import requests
from bs4 import BeautifulSoup
from config import Config

class TorrentFinder:
    """Service for finding torrents from torrent sites"""
    
    def __init__(self):
        self.base_domain = Config.TORRENT_SITE_DOMAIN
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_html(self, url):
        """Fetch HTML content from URL"""
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def search_all(self, query):
        """Search all categories"""
        try:
            url = f'https://{self.base_domain}/search/{query}/1/99/0'
            html = self.fetch_html(url)
            soup = BeautifulSoup(html, 'html.parser')
            return self._parse_results(soup)
        except Exception as e:
            logging.error(f'Search failed: {e}')
            return []

    def search_hd_movies(self, query):
        """Search HD movies category"""
        try:
            url = f'https://{self.base_domain}/search/{query}/1/99/207'
            html = self.fetch_html(url)
            soup = BeautifulSoup(html, 'html.parser')
            return self._parse_results(soup)
        except Exception as e:
            logging.error(f'HD movie search failed: {e}')
            return []

    def search_movies(self, query):
        """Search movies category"""
        try:
            url = f'https://{self.base_domain}/search/{query}/1/99/201'
            html = self.fetch_html(url)
            soup = BeautifulSoup(html, 'html.parser')
            return self._parse_results(soup)
        except Exception as e:
            logging.error(f'Movie search failed: {e}')
            return []

    def search_hd_tv_shows(self, query):
        """Search HD TV shows category"""
        try:
            url = f'https://{self.base_domain}/search/{query}/1/99/208'
            html = self.fetch_html(url)
            soup = BeautifulSoup(html, 'html.parser')
            return self._parse_results(soup)
        except Exception as e:
            logging.error(f'HD TV search failed: {e}')
            return []

    def search_tv_shows(self, query):
        """Search TV shows category"""
        try:
            url = f'https://{self.base_domain}/search/{query}/1/99/205'
            html = self.fetch_html(url)
            soup = BeautifulSoup(html, 'html.parser')
            return self._parse_results(soup)
        except Exception as e:
            logging.error(f'TV search failed: {e}')
            return []

    def _parse_results(self, soup):
        """Parse torrent results from HTML soup"""
        results = []
        for trs in soup.find_all('tr'):
            tds = trs.find_all('td')
            if len(tds) > 1:
                magnet_link_tag = tds[1].find('a', href=True, title="Download this torrent using magnet")
                if not magnet_link_tag:
                    continue

                title_tag = tds[1].find('a', class_='detLink')
                if not title_tag:
                    continue

                title = title_tag.get('title', '').replace('Details for ', '')
                magnet = magnet_link_tag['href']
                
                if not title or not magnet:
                    continue

                size_match = re.search(r'(?<=Size )(.*)(?=,)', str(tds[1]))
                size = size_match.group(0) if size_match else None

                seeders = tds[2].text if len(tds) > 2 else None
                leechers = tds[3].text if len(tds) > 3 else None

                result = {
                    'title': title,
                    'magnet': magnet,
                    'size': size,
                    'seeders': seeders,
                    'leechers': leechers
                }
                result = {key: value.replace('\xa0', ' ') if value else value for key, value in result.items()}
                results.append(result)
        return results 