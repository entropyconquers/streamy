from flask import Blueprint, jsonify
from services.tmdb_client import TMDBClient
from config import Config
from api_schema import get_api_schema

# Create blueprint
health_bp = Blueprint('health', __name__)

@health_bp.route('/', methods=['GET'])
def api_documentation():
    """API documentation and available endpoints"""
    return jsonify({
        'api_name': 'Torrent Search API',
        'version': '5.0',
        'description': 'Modern torrent search API with TMDB integration and intelligent scoring',
        'features': [
            'TMDB metadata integration with streamlined essential fields only',
            'Integrated credits within tmdb_details (cast + crew combined)',
            'Direct torrent scraping (no Telegram dependencies)',
            'Intelligent balanced scoring algorithm',
            'Quality detection and filtering',
            'Season/episode support for TV shows',
            'Advanced search patterns with deduplication',
            '0-seeder filtering for reliable downloads',
            'Optimized for streaming app UIs',
            'Professional API design with proper error handling'
        ],
        'endpoints': {
            'search': {
                'GET /search/<query>': 'General search (movies + TV shows) - Returns top 5 TMDB results',
                'GET /movies/<query>': 'Movie search only - Returns top 5 TMDB results',
                'GET /tv-shows/<query>': 'TV show search only - Returns top 5 TMDB results'
            },
            'details': {
                'GET /details/movie/<tmdb_id>': 'Movie details with torrents and credits (cast/crew)',
                'GET /details/tv/<tmdb_id>': 'TV show details with torrents',
                'GET /details/tv/<tv_id>/season/<season_number>': 'Season details with torrents',
                'GET /details/tv/<tv_id>/season/<season_number>/episode/<episode_number>': 'Episode details with torrents'
            },
            'utility': {
                'GET /': 'API documentation',
                'GET /health': 'Health check',
                'GET /schema': 'OpenAPI 3.0 schema specification'
            }
        },
        'new_features': {
            'cleaned_tmdb_structure': {
                'description': 'Streamlined TMDB responses with only essential fields for streaming apps',
                'removed_fields': [
                    'production_companies', 'production_countries', 'belongs_to_collection',
                    'budget', 'revenue', 'video', 'networks', 'created_by'
                ],
                'kept_fields': [
                    'id', 'title/name', 'overview', 'release_date', 'vote_average',
                    'genres', 'runtime', 'poster_path', 'backdrop_path', 'imdb_id'
                ]
            },
            'integrated_credits': {
                'description': 'Credits now integrated within tmdb_details as a single array',
                'structure': 'Combined cast and crew sorted by popularity (top 20)',
                'fields': [
                    'id', 'name', 'character (for actors)', 'job', 'department',
                    'popularity', 'profile_path (full URL)'
                ],
                'benefits': [
                    'Single array easier to display',
                    'Sorted by popularity (most important first)',
                    'Standardized structure for cast and crew',
                    'Smaller response size'
                ]
            }
        },
        'intelligent_scoring': {
            'description': 'Advanced algorithm balancing size, seeders, and availability',
            'factors': [
                'Seeders (primary): Higher seeders = better availability',
                'Size optimization: Sweet spot between quality and download time',
                'Bonus system: Extra points for high-seeder torrents',
                'Quality filtering: Removes 0-seeder torrents automatically'
            ],
            'size_categories': {
                '< 100MB': 'Poor quality penalty (0.3x)',
                '100MB - 500MB': 'Small file penalty (0.6x)',
                '500MB - 3GB': 'Sweet spot (1.0x) ⭐',
                '3GB - 8GB': 'Large file slight penalty (0.8x)',
                '> 8GB': 'Very large penalty (0.5x)'
            },
            'seeder_bonuses': {
                '10+ seeders': '20% bonus',
                '5+ seeders': '10% bonus',
                '0 seeders': 'Filtered out completely'
            }
        },
        'advanced_search': {
            'season_search': [
                'Uses multiple patterns: "Show Name S01" + "Show Name Season 1"',
                'Filters out individual episodes (removes S01E01 patterns)',
                'Returns only season packs and complete season torrents'
            ],
            'episode_search': [
                'Uses targeted patterns: "Show Name S01E01" + "Show Name Season 1 Episode 1"',
                'Returns episode-specific torrents only'
            ]
        },
        'example_responses': {
            'search_response': {
                'status': 'success',
                'query': 'breaking bad',
                'count': 5,
                'results': ['TMDB search results with posters and metadata']
            },
            'movie_details_response': {
                'status': 'success',
                'tmdb_details': {
                    'id': 550,
                    'title': 'Fight Club',
                    'overview': 'Movie description...',
                    'vote_average': 8.4,
                    'genres': [{'id': 18, 'name': 'Drama'}],
                    'poster_path': 'Full image URL',
                    'credits': [
                        {
                            'name': 'Brad Pitt',
                            'character': 'Tyler Durden',
                            'job': 'Actor',
                            'department': 'Acting',
                            'popularity': 15.15,
                            'profile_path': 'Full image URL'
                        },
                        {
                            'name': 'David Fincher',
                            'character': None,
                            'job': 'Director',
                            'department': 'Directing',
                            'popularity': 8.64,
                            'profile_path': 'Full image URL'
                        }
                    ]
                },
                'torrent_count': 27,
                'torrent_results': 'Sorted by intelligent scoring'
            }
        },
        'status': 'Production Ready',
        'last_updated': '2024'
    })

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test TMDB connection if available
        tmdb_status = 'disabled'
        if Config.is_tmdb_enabled():
            tmdb_client = TMDBClient()
            tmdb_status = 'connected' if tmdb_client.test_connection() else 'error'
        
        return jsonify({
            'status': 'healthy',
            'api_version': '5.0',
            'services': {
                'torrent_scraping': 'active',
                'tmdb_integration': tmdb_status
            },
            'features': {
                'intelligent_scoring': 'active',
                'quality_filtering': 'active',
                'advanced_search': 'active',
                'integrated_credits': 'active',
                'streamlined_responses': 'active',
                'duplicate_removal': 'active'
            },
            'timestamp': 'live'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@health_bp.route('/schema', methods=['GET'])
def api_schema():
    """Return OpenAPI 3.0 schema for the API"""
    return jsonify(get_api_schema()) 