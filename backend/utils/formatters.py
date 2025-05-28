import re
from config import Config

def extract_quality(title):
    """Extract quality from torrent title"""
    quality_patterns = ['4K', '2160p', '1080p', '720p', '480p', 'HDRip', 'BluRay', 'WEBRip', 'DVDRip']
    for pattern in quality_patterns:
        if pattern.lower() in title.lower():
            return pattern
    return None

def parse_size_to_bytes(size_str):
    """Convert size string to bytes for sorting"""
    if not size_str or size_str == 'Unknown':
        return 0
    
    # Remove extra spaces and convert to uppercase
    size_str = size_str.strip().upper()
    
    # Extract number and unit
    size_match = re.match(r'([\d.]+)\s*([KMGT]?I?B)', size_str)
    if not size_match:
        return 0
    
    number = float(size_match.group(1))
    unit = size_match.group(2)
    
    # Convert to bytes
    multipliers = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4,
        'KIB': 1024,
        'MIB': 1024**2,
        'GIB': 1024**3,
        'TIB': 1024**4
    }
    
    return int(number * multipliers.get(unit, 1))

import math

def calculate_torrent_score(size_bytes, seeders):
    """
    Calculate a sophisticated score for torrent quality using advanced heuristics.
    Higher score = better torrent
    
    Advanced Logic:
    - Multi-factor weighted scoring with non-linear relationships
    - Dynamic size preferences based on seeder density
    - Popularity momentum and swarm health indicators
    - Diminishing returns for excessive seeders to balance quality vs availability
    """
    if seeders == 0:
        return 0  # No seeders = unusable
    
    # Convert size to GB for calculations
    size_gb = size_bytes / (1024**3)
    
    # === SEEDER AVAILABILITY SCORE ===
    # Logarithmic scaling with diminishing returns after certain thresholds
    # This prevents torrents with 1000+ seeders from dominating unrealistically
    if seeders <= 2:
        seeder_base = seeders * 25  # High weight for low seeder counts
    elif seeders <= 10:
        seeder_base = 50 + (seeders - 2) * 15  # Moderate scaling
    elif seeders <= 50:
        seeder_base = 170 + (seeders - 10) * 8  # Reduced scaling
    else:
        seeder_base = 490 + math.log10(seeders - 49) * 25  # Logarithmic for high counts
    
    # === DYNAMIC SIZE SCORING ===
    # Size preferences adapt based on seeder count (popular content can be larger)
    seeder_size_tolerance = min(2.0, math.log10(seeders + 1) * 0.8)
    
    # Base size categories with dynamic thresholds
    tiny_threshold = 0.05  # 50MB
    small_threshold = 0.3 + seeder_size_tolerance * 0.2  # 300MB+ (adaptive)
    optimal_min = 0.7 + seeder_size_tolerance * 0.3  # 700MB+ (adaptive)
    optimal_max = 2.5 + seeder_size_tolerance * 1.5  # 2.5GB+ (adaptive)
    large_threshold = 6.0 + seeder_size_tolerance * 2.0  # 6GB+ (adaptive)
    
    if size_gb < tiny_threshold:
        # Micro files - likely samples, previews, or poor quality
        size_score = 0.15
    elif size_gb < small_threshold:
        # Small files - could be compressed/low quality but acceptable for rare content
        size_score = 0.4 + (size_gb / small_threshold) * 0.3
    elif size_gb <= optimal_min:
        # Approaching optimal - good balance of quality and size
        size_score = 0.7 + (size_gb - small_threshold) / (optimal_min - small_threshold) * 0.25
    elif size_gb <= optimal_max:
        # Optimal range - best balance point
        size_score = 0.95 + 0.05 * math.sin((size_gb - optimal_min) / (optimal_max - optimal_min) * math.pi)
    elif size_gb <= large_threshold:
        # Large but manageable - slight penalty with gradual falloff
        penalty_factor = (size_gb - optimal_max) / (large_threshold - optimal_max)
        size_score = 0.95 * (1 - penalty_factor * 0.25)
    else:
        # Very large files - significant penalty but not eliminated
        excess_gb = size_gb - large_threshold
        size_score = 0.7 * math.exp(-excess_gb / 10)  # Exponential decay
    
    # === SWARM HEALTH INDICATORS ===
    # Health bonus based on seeder density and distribution assumptions
    if seeders == 1:
        health_multiplier = 0.8  # Single seeder risk
    elif seeders <= 3:
        health_multiplier = 0.9  # Low redundancy
    elif seeders <= 8:
        health_multiplier = 1.0  # Healthy small swarm
    elif seeders <= 25:
        health_multiplier = 1.1  # Very healthy swarm
    else:
        # Extremely popular - bonus but with diminishing returns
        health_multiplier = 1.1 + min(0.3, (seeders - 25) / 100)
    
    # === POPULARITY MOMENTUM ===
    # Higher seeder counts suggest trending/quality content
    if seeders >= 20:
        momentum_bonus = 1.15
    elif seeders >= 10:
        momentum_bonus = 1.08
    elif seeders >= 5:
        momentum_bonus = 1.03
    else:
        momentum_bonus = 1.0
    
    # === SIZE-SEEDER SYNERGY ===
    # Bonus when size and seeders are well-matched
    expected_seeders_for_size = max(1, size_gb * 2)  # Rough heuristic
    synergy_ratio = min(seeders / expected_seeders_for_size, expected_seeders_for_size / seeders)
    synergy_bonus = 0.9 + synergy_ratio * 0.2  # 0.9 to 1.1 multiplier
    
    # === RARITY ADJUSTMENT ===
    # Slight bonus for rare content (low seeders but not zero)
    if 1 <= seeders <= 3 and size_gb >= 0.5:
        rarity_bonus = 1.1
    else:
        rarity_bonus = 1.0
    
    # === FINAL SCORE CALCULATION ===
    base_score = seeder_base * size_score
    final_score = (base_score * 
                  health_multiplier * 
                  momentum_bonus * 
                  synergy_bonus * 
                  rarity_bonus)
    
    # Ensure score is positive and apply final smoothing
    return max(0.1, final_score)

def format_tmdb_search_results(results):
    """Format TMDB search results for API response"""
    formatted_results = []
    
    for result in results:
        # Add image URLs
        if result.get('poster_path'):
            result['poster_path'] = f"{Config.TMDB_IMAGE_BASE_URL}{result['poster_path']}"
        if result.get('backdrop_path'):
            result['backdrop_path'] = f"{Config.TMDB_IMAGE_BASE_URL}{result['backdrop_path']}"
        
        formatted_results.append(result)
    
    return formatted_results

def format_tmdb_details(details, credits=None):
    """Format TMDB details with full image URLs and clean unnecessary fields"""
    if not details:
        return None
    
    # Start with a clean copy
    formatted_details = {}
    
    # Essential movie/TV fields only
    essential_fields = [
        'id', 'title', 'name', 'overview', 'release_date', 'first_air_date',
        'vote_average', 'vote_count', 'popularity', 'adult', 'original_language',
        'original_title', 'original_name', 'runtime', 'status', 'tagline',
        'genres', 'spoken_languages', 'homepage', 'imdb_id'
    ]
    
    # TV-specific essential fields
    tv_fields = [
        'number_of_episodes', 'number_of_seasons', 'episode_run_time',
        'in_production', 'last_air_date', 'type', 'seasons'
    ]
    
    # Season/Episode specific fields
    season_episode_fields = [
        'season_number', 'episode_number', 'air_date', 'still_path',
        'episode_count', 'episodes'
    ]
    
    # Copy only essential fields
    all_essential = essential_fields + tv_fields + season_episode_fields
    for field in all_essential:
        if field in details:
            formatted_details[field] = details[field]
    
    # Add image URLs
    if details.get('poster_path'):
        formatted_details['poster_path'] = f"{Config.TMDB_IMAGE_BASE_URL}{details['poster_path']}"
    if details.get('backdrop_path'):
        formatted_details['backdrop_path'] = f"{Config.TMDB_IMAGE_BASE_URL}{details['backdrop_path']}"
    
    # Format genres (keep only id and name)
    if formatted_details.get('genres'):
        formatted_details['genres'] = [
            {'id': genre['id'], 'name': genre['name']} 
            for genre in formatted_details['genres']
        ]
    
    # Format spoken languages (keep only essential info)
    if formatted_details.get('spoken_languages'):
        formatted_details['spoken_languages'] = [
            {'iso_639_1': lang.get('iso_639_1'), 'name': lang.get('name')} 
            for lang in formatted_details['spoken_languages']
        ]
    
    # Format seasons (TV shows) - keep only essential info
    if formatted_details.get('seasons'):
        clean_seasons = []
        for season in formatted_details['seasons']:
            clean_season = {
                'id': season.get('id'),
                'name': season.get('name'),
                'season_number': season.get('season_number'),
                'episode_count': season.get('episode_count'),
                'air_date': season.get('air_date'),
                'overview': season.get('overview')
            }
            if season.get('poster_path'):
                clean_season['poster_path'] = f"{Config.TMDB_IMAGE_BASE_URL}{season['poster_path']}"
            clean_seasons.append(clean_season)
        formatted_details['seasons'] = clean_seasons
    
    # Format episodes (for season details) - keep only essential info
    if formatted_details.get('episodes'):
        clean_episodes = []
        for episode in formatted_details['episodes']:
            clean_episode = {
                'id': episode.get('id'),
                'name': episode.get('name'),
                'episode_number': episode.get('episode_number'),
                'season_number': episode.get('season_number'),
                'air_date': episode.get('air_date'),
                'overview': episode.get('overview'),
                'vote_average': episode.get('vote_average'),
                'runtime': episode.get('runtime')
            }
            if episode.get('still_path'):
                clean_episode['still_path'] = f"{Config.TMDB_IMAGE_BASE_URL}{episode['still_path']}"
            clean_episodes.append(clean_episode)
        formatted_details['episodes'] = clean_episodes
    
    # Add credits as a single array within tmdb_details (for movies)
    if credits:
        combined_credits = []
        
        # Add cast members
        for cast_member in credits.get('cast', []):
            credit = {
                'id': cast_member.get('id'),
                'name': cast_member.get('name'),
                'character': cast_member.get('character'),
                'job': 'Actor',  # Standardize job for cast
                'department': 'Acting',
                'popularity': cast_member.get('popularity', 0),
                'order': cast_member.get('order', 999)
            }
            if cast_member.get('profile_path'):
                credit['profile_path'] = f"{Config.TMDB_IMAGE_BASE_URL}{cast_member['profile_path']}"
            combined_credits.append(credit)
        
        # Add crew members
        for crew_member in credits.get('crew', []):
            credit = {
                'id': crew_member.get('id'),
                'name': crew_member.get('name'),
                'character': None,  # Crew don't have characters
                'job': crew_member.get('job'),
                'department': crew_member.get('department'),
                'popularity': crew_member.get('popularity', 0),
                'order': 999  # Crew comes after cast
            }
            if crew_member.get('profile_path'):
                credit['profile_path'] = f"{Config.TMDB_IMAGE_BASE_URL}{crew_member['profile_path']}"
            combined_credits.append(credit)
        
        # Sort by popularity (descending) and limit to top 20
        combined_credits.sort(key=lambda x: x['popularity'], reverse=True)
        formatted_details['credits'] = combined_credits[:20]
    
    return formatted_details

def format_torrent_results(results):
    """Format torrent results, filter out 0-seeders, and sort by balanced score"""
    formatted_results = []
    
    for result in results:
        if not result.get('title') or not result.get('magnet'):
            continue
            
        seeders = int(result['seeders']) if result.get('seeders') and result['seeders'].isdigit() else 0
        
        # Filter out torrents with 0 seeders
        if seeders == 0:
            continue
            
        formatted_result = {
            'title': result['title'],
            'magnet': result['magnet'],
            'size': result.get('size', 'Unknown'),
            'seeders': seeders,
            'leechers': int(result['leechers']) if result.get('leechers') and result['leechers'].isdigit() else 0
        }
        
        # Add quality if available
        quality = extract_quality(result['title'])
        if quality:
            formatted_result['quality'] = quality
            
        formatted_results.append(formatted_result)
    
    # Sort by balanced score (higher score = better torrent)
    for result in formatted_results:
        size_bytes = parse_size_to_bytes(result['size'])
        result['_score'] = calculate_torrent_score(size_bytes, result['seeders'])
    
    # Sort by score (highest first)
    formatted_results.sort(key=lambda x: x['_score'], reverse=True)
    
    # Remove the internal score field
    for result in formatted_results:
        result.pop('_score', None)
    
    return formatted_results

def search_torrents_for_title(torrent_finder, title, content_type='movie', season=None, episode=None):
    """Search for torrents based on title and content type with improved season/episode logic"""
    # Clean the title for better torrent search
    search_title = clean_title_for_search(title)
    
    if content_type == 'movie':
        # Search both regular and HD movies
        regular_results = torrent_finder.search_movies(search_title)
        hd_results = torrent_finder.search_hd_movies(search_title)
        results = regular_results + hd_results
    elif content_type == 'tv':
        if episode is not None and season is not None:
            # Search for specific episode
            results = search_specific_episode(torrent_finder, search_title, season, episode)
        elif season is not None:
            # Search for specific season
            results = search_specific_season(torrent_finder, search_title, season)
        else:
            # General TV show search
            regular_results = torrent_finder.search_tv_shows(search_title)
            hd_results = torrent_finder.search_hd_tv_shows(search_title)
            results = regular_results + hd_results
    else:
        # General search
        results = torrent_finder.search_all(search_title)
    
    # Remove duplicates based on magnet link
    unique_results = remove_duplicate_torrents(results)
    
    return format_torrent_results(unique_results)

def search_specific_season(torrent_finder, show_name, season_num):
    """Search for specific season using multiple search patterns"""
    search_patterns = [
        f"{show_name} S{season_num:02d}",
        f"{show_name} Season {season_num}"
    ]
    
    all_results = []
    for pattern in search_patterns:
        # Search both regular and HD TV shows
        regular_results = torrent_finder.search_tv_shows(pattern)
        hd_results = torrent_finder.search_hd_tv_shows(pattern)
        all_results.extend(regular_results + hd_results)
    
    # Filter out individual episodes (those with SxxExx pattern)
    season_results = []
    episode_pattern = re.compile(r'S\d{2}E\d{2}', re.IGNORECASE)
    
    for result in all_results:
        title = result.get('title', '')
        # Exclude results that contain episode patterns
        if not episode_pattern.search(title):
            season_results.append(result)
    
    return season_results

def search_specific_episode(torrent_finder, show_name, season_num, episode_num):
    """Search for specific episode using multiple search patterns"""
    search_patterns = [
        f"{show_name} S{season_num:02d}E{episode_num:02d}",
        f"{show_name} Season {season_num} Episode {episode_num}"
    ]
    
    all_results = []
    for pattern in search_patterns:
        # Search both regular and HD TV shows
        regular_results = torrent_finder.search_tv_shows(pattern)
        hd_results = torrent_finder.search_hd_tv_shows(pattern)
        all_results.extend(regular_results + hd_results)
    
    return all_results

def remove_duplicate_torrents(results):
    """Remove duplicate torrents based on magnet link"""
    seen_magnets = set()
    unique_results = []
    
    for result in results:
        magnet = result.get('magnet', '')
        if magnet and magnet not in seen_magnets:
            seen_magnets.add(magnet)
            unique_results.append(result)
    
    return unique_results

def clean_title_for_search(title):
    """Clean title for better torrent search results"""
    # Remove special characters and extra spaces
    title = re.sub(r'[^\w\s]', ' ', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title

def filter_4k_results(results):
    """Filter results to only include 4K content"""
    return [r for r in results if '4K' in r.get('title', '') or '2160p' in r.get('title', '')]

def filter_by_season(results, season_num):
    """Filter TV show results by season number (legacy function, kept for compatibility)"""
    filtered_results = []
    for result in results:
        title = result.get('title', '')
        if f'S{season_num:02d}' in title or f's{season_num:02d}' in title or f'Season {season_num}' in title:
            filtered_results.append(result)
    return filtered_results

def filter_by_episode(results, season_num, episode_num):
    """Filter TV show results by season and episode number (legacy function, kept for compatibility)"""
    filtered_results = []
    for result in results:
        title = result.get('title', '')
        # Look for S01E01 or similar patterns
        if f'S{season_num:02d}E{episode_num:02d}' in title or f's{season_num:02d}e{episode_num:02d}' in title:
            filtered_results.append(result)
    return filtered_results 