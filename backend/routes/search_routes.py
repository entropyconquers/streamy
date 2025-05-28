from flask import Blueprint, jsonify, request
import logging
from services.torrent_finder import TorrentFinder
from services.tmdb_client import TMDBClient
from utils.formatters import (
    format_tmdb_search_results, 
    format_tmdb_details, 
    search_torrents_for_title
)
from config import Config

# Create blueprint
search_bp = Blueprint('search', __name__)

# Initialize services
torrent_finder = TorrentFinder()
tmdb_client = TMDBClient() if Config.is_tmdb_enabled() else None

@search_bp.route('/search/<query>', methods=['GET'])
def search_multi(query):
    """General search returning top 5 TMDB results (movies and TV shows)"""
    try:
        if not tmdb_client:
            return jsonify({
                'status': 'error',
                'message': 'TMDB service not available'
            }), 503
        
        # Get TMDB multi search results (top 5)
        results = tmdb_client.search_multi(query)
        formatted_results = format_tmdb_search_results(results)
        
        return jsonify({
            'status': 'success',
            'query': query,
            'count': len(formatted_results),
            'results': formatted_results
        })
        
    except Exception as e:
        logging.error(f'Multi search failed: {e}')
        return jsonify({
            'status': 'error',
            'message': f'Search failed: {str(e)}'
        }), 500

@search_bp.route('/movies/<query>', methods=['GET'])
def search_movies(query):
    """Search movies returning top 5 TMDB results"""
    try:
        if not tmdb_client:
            return jsonify({
                'status': 'error',
                'message': 'TMDB service not available'
            }), 503
        
        # Get TMDB movie search results (top 5)
        results = tmdb_client.search_movie(query)
        formatted_results = format_tmdb_search_results(results)
        
        return jsonify({
            'status': 'success',
            'query': query,
            'count': len(formatted_results),
            'results': formatted_results
        })
        
    except Exception as e:
        logging.error(f'Movie search failed: {e}')
        return jsonify({
            'status': 'error',
            'message': f'Movie search failed: {str(e)}'
        }), 500

@search_bp.route('/tv-shows/<query>', methods=['GET'])
def search_tv_shows(query):
    """Search TV shows returning top 5 TMDB results"""
    try:
        if not tmdb_client:
            return jsonify({
                'status': 'error',
                'message': 'TMDB service not available'
            }), 503
        
        # Get TMDB TV search results (top 5)
        results = tmdb_client.search_tv_show(query)
        formatted_results = format_tmdb_search_results(results)
        
        return jsonify({
            'status': 'success',
            'query': query,
            'count': len(formatted_results),
            'results': formatted_results
        })
        
    except Exception as e:
        logging.error(f'TV show search failed: {e}')
        return jsonify({
            'status': 'error',
            'message': f'TV show search failed: {str(e)}'
        }), 500

@search_bp.route('/details/<content_type>/<int:tmdb_id>', methods=['GET'])
def get_details_with_torrents(content_type, tmdb_id):
    """Get detailed TMDB info with available torrent links"""
    try:
        if not tmdb_client:
            return jsonify({
                'status': 'error',
                'message': 'TMDB service not available'
            }), 503
        
        if content_type not in ['movie', 'tv']:
            return jsonify({
                'status': 'error',
                'message': 'Content type must be "movie" or "tv"'
            }), 400
        
        # Get detailed TMDB information
        if content_type == 'movie':
            details = tmdb_client.get_movie_details(tmdb_id)
            title = details.get('title') if details else None
            
            # Get movie credits (cast and crew)
            credits = tmdb_client.get_movie_credits(tmdb_id) if details else None
        else:  # tv
            details = tmdb_client.get_tv_details(tmdb_id)
            title = details.get('name') if details else None
            credits = None  # TV credits not implemented yet
        
        if not details:
            return jsonify({
                'status': 'error',
                'message': 'Content not found'
            }), 404
        
        # Format TMDB details with credits integrated
        formatted_details = format_tmdb_details(details, credits)
        
        # Search for torrents
        torrent_results = []
        if title:
            torrent_results = search_torrents_for_title(
                torrent_finder, 
                title, 
                content_type
            )
        
        return jsonify({
            'status': 'success',
            'tmdb_details': formatted_details,
            'torrent_count': len(torrent_results),
            'torrent_results': torrent_results
        })
        
    except Exception as e:
        logging.error(f'Details with torrents failed: {e}')
        return jsonify({
            'status': 'error',
            'message': f'Failed to get details: {str(e)}'
        }), 500

@search_bp.route('/details/tv/<int:tv_id>/season/<int:season_number>', methods=['GET'])
def get_season_details_with_torrents(tv_id, season_number):
    """Get TV season details with available torrent links"""
    try:
        if not tmdb_client:
            return jsonify({
                'status': 'error',
                'message': 'TMDB service not available'
            }), 503
        
        # Get TV show details first to get the show name
        tv_details = tmdb_client.get_tv_details(tv_id)
        if not tv_details:
            return jsonify({
                'status': 'error',
                'message': 'TV show not found'
            }), 404
        
        # Get season details
        season_details = tmdb_client.get_tv_season_details(tv_id, season_number)
        if not season_details:
            return jsonify({
                'status': 'error',
                'message': 'Season not found'
            }), 404
        
        # Format season details
        formatted_season = format_tmdb_details(season_details)
        
        # Search for season torrents
        show_name = tv_details.get('name')
        torrent_results = []
        if show_name:
            torrent_results = search_torrents_for_title(
                torrent_finder, 
                show_name, 
                'tv',
                season=season_number
            )
        
        return jsonify({
            'status': 'success',
            'tv_show_name': show_name,
            'season_details': formatted_season,
            'torrent_count': len(torrent_results),
            'torrent_results': torrent_results
        })
        
    except Exception as e:
        logging.error(f'Season details with torrents failed: {e}')
        return jsonify({
            'status': 'error',
            'message': f'Failed to get season details: {str(e)}'
        }), 500

@search_bp.route('/details/tv/<int:tv_id>/season/<int:season_number>/episode/<int:episode_number>', methods=['GET'])
def get_episode_details_with_torrents(tv_id, season_number, episode_number):
    """Get TV episode details with available torrent links"""
    try:
        if not tmdb_client:
            return jsonify({
                'status': 'error',
                'message': 'TMDB service not available'
            }), 503
        
        # Get TV show details first to get the show name
        tv_details = tmdb_client.get_tv_details(tv_id)
        if not tv_details:
            return jsonify({
                'status': 'error',
                'message': 'TV show not found'
            }), 404
        
        # Get episode details
        episode_details = tmdb_client.get_tv_episode_details(tv_id, season_number, episode_number)
        if not episode_details:
            return jsonify({
                'status': 'error',
                'message': 'Episode not found'
            }), 404
        
        # Format episode details
        formatted_episode = format_tmdb_details(episode_details)
        
        # Search for episode torrents
        show_name = tv_details.get('name')
        torrent_results = []
        if show_name:
            torrent_results = search_torrents_for_title(
                torrent_finder, 
                show_name, 
                'tv',
                season=season_number,
                episode=episode_number
            )
        
        return jsonify({
            'status': 'success',
            'tv_show_name': show_name,
            'episode_details': formatted_episode,
            'torrent_count': len(torrent_results),
            'torrent_results': torrent_results
        })
        
    except Exception as e:
        logging.error(f'Episode details with torrents failed: {e}')
        return jsonify({
            'status': 'error',
            'message': f'Failed to get episode details: {str(e)}'
        }), 500 