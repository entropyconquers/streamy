# Torrent Search API v5.0

A modern, modular torrent search API that integrates **The Movie Database (TMDB)** for rich metadata and scrapes torrent sites for magnet links. Perfect for building streaming service UIs with comprehensive movie/TV show information.

## 🚀 New API Structure (v5.0)

**Search Endpoints**: Return top 5 TMDB results only (fast, lightweight)
**Detail Endpoints**: Return streamlined TMDB details + torrent links (optimized for streaming apps)

## 📋 OpenAPI Schema & Documentation

### Schema Access

The API now includes comprehensive OpenAPI 3.0.3 schema documentation:

```bash
# Get complete OpenAPI schema
curl http://localhost:8001/schema

# Get API documentation
curl http://localhost:8001/

# Check API health
curl http://localhost:8001/health
```

### Integration Tools

- **Swagger UI**: Import schema from `/schema` endpoint for interactive documentation
- **Postman**: Import OpenAPI spec for automatic collection generation
- **Code Generation**: Use OpenAPI generators for client SDKs in any language
- **API Testing**: Use schema for automated testing and validation

### Documentation Files

- **OpenAPI Schema**: Available at `/schema` endpoint (JSON format)
- **Markdown Documentation**: `backend/API_SCHEMA.md` (comprehensive guide)
- **Test Suite**: `backend/test_schema.py` (schema validation)

### Schema Features

- ✅ **Complete Coverage**: All 10 endpoints documented with examples
- ✅ **Detailed Schemas**: 20+ data models with validation rules
- ✅ **Error Handling**: Proper HTTP status codes and error responses
- ✅ **Type Safety**: Strict type definitions for all fields
- ✅ **Real Examples**: Actual response examples for all endpoints

## ✨ Features

- **Streamlined TMDB Integration**: Essential fields only, optimized for streaming app UIs
- **Integrated Credits**: Cast and crew combined in single array within tmdb_details
- **Direct Torrent Scraping**: No Telegram dependencies, just internet connection
- **Modular Architecture**: Clean separation of concerns, easy to maintain
- **Quality Detection**: Automatic quality extraction (4K, 1080p, 720p, etc.)
- **Season/Episode Support**: Detailed TV show navigation
- **Environment Configuration**: Secure credential management
- **Professional API Design**: RESTful endpoints with proper error handling
- **Intelligent Scoring**: Balanced algorithm considering size, seeders, and availability
- **Advanced Search Patterns**: Multiple search strategies for better results
- **Duplicate Removal**: Automatic deduplication based on magnet links
- **Quality Filtering**: Removes 0-seeder torrents for reliable downloads

## 🎬 Streamlined TMDB Structure

### Cleaned Response Format

The API now returns only essential fields needed for streaming applications:

**Essential Fields Kept**:

- `id`, `title/name`, `overview`, `release_date/first_air_date`
- `vote_average`, `vote_count`, `popularity`, `runtime`
- `genres`, `spoken_languages`, `homepage`, `imdb_id`
- `poster_path`, `backdrop_path` (full URLs)

**Removed Unnecessary Fields**:

- `production_companies`, `production_countries`, `belongs_to_collection`
- `budget`, `revenue`, `video`, `networks`, `created_by`
- All other production-related metadata not needed for streaming UIs

### Integrated Credits Structure

Credits are now included within `tmdb_details` as a single array:

**Combined Credits Array** (Top 20, sorted by popularity):

- Cast and crew members in one unified structure
- Sorted by popularity (most important people first)
- Standardized fields for both actors and crew

**Credit Object Structure**:

```json
{
  "id": 287,
  "name": "Brad Pitt",
  "character": "Tyler Durden", // null for crew
  "job": "Actor", // "Actor" for cast, actual job for crew
  "department": "Acting",
  "popularity": 15.1539,
  "profile_path": "https://image.tmdb.org/t/p/w500/..."
}
```

**Benefits**:

- ✅ **Smaller Response Size**: 20% reduction by removing unnecessary fields
- ✅ **Easier to Display**: Single array instead of separate cast/crew objects
- ✅ **Popularity Sorted**: Most important people appear first
- ✅ **Standardized Structure**: Consistent format for all credit types
- ✅ **Streaming App Optimized**: Only fields needed for UI display

## 🎯 Intelligent Torrent Scoring

### Balanced Scoring Algorithm

Our advanced scoring system finds the optimal balance between file size and availability:

**Scoring Factors:**

1. **Seeders** (Primary): Higher seeders = better availability and download speed
2. **Size Optimization**: Sweet spot between quality and download time
3. **Bonus System**: Extra points for high-seeder torrents
4. **Quality Filtering**: Automatically removes unusable 0-seeder torrents

**Size Categories:**

- **< 100MB**: Poor quality penalty (0.3x multiplier)
- **100MB - 500MB**: Small file penalty (0.6x multiplier)
- **500MB - 3GB**: Sweet spot (1.0x multiplier) ⭐
- **3GB - 8GB**: Large file slight penalty (0.8x multiplier)
- **> 8GB**: Very large penalty (0.5x multiplier)

**Seeder Bonuses:**

- **10+ seeders**: 20% bonus (excellent availability)
- **5+ seeders**: 10% bonus (good availability)
- **0 seeders**: Filtered out completely

**Example Preference:**

- ✅ **1.3GB with 10 seeders** (Score: ~120) - Preferred
- ❌ **750MB with 2 seeders** (Score: ~12) - Lower ranked

### Advanced Search & Sorting

### Season Search Intelligence

When searching for a specific season (e.g., Breaking Bad Season 1):

- Uses multiple search patterns: `"Show Name S01"` + `"Show Name Season 1"`
- Automatically filters out individual episodes (removes S01E01 patterns)
- Combines and deduplicates results from both searches
- Returns only season packs and complete season torrents

### Episode Search Intelligence

When searching for a specific episode (e.g., Breaking Bad S1E1):

- Uses targeted patterns: `"Show Name S01E01"` + `"Show Name Season 1 Episode 1"`
- Searches for the exact episode, not the episode name
- Combines results from multiple search strategies
- Returns episode-specific torrents

## 📋 Requirements

- Python 3.7+
- Internet connection
- TMDB API key (free from [themoviedb.org](https://www.themoviedb.org/settings/api))

## 🛠️ Installation

1. **Clone the repository**:

```bash
git clone <repository-url>
cd TorrentSearchApi
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:

```bash
# Copy the example .env file
cp .env.example .env

# Edit .env with your TMDB API key
TMDB_API_KEY=your_tmdb_bearer_token_here
```

4. **Run the API**:

```bash
python app.py
```

The API will be available at `http://localhost:8001`

## 📚 API Endpoints

### Search Endpoints (TMDB Results Only)

#### General Search

```http
GET /search/<query>
```

Search both movies and TV shows, returns top 5 TMDB results.

**Example**: `/search/breaking bad`

#### Movie Search

```http
GET /movies/<query>
```

Search movies only, returns top 5 TMDB results.

**Example**: `/movies/inception`

#### TV Show Search

```http
GET /tv-shows/<query>
```

Search TV shows only, returns top 5 TMDB results.

**Example**: `/tv-shows/breaking bad`

### Detail Endpoints (TMDB + Torrents)

#### Movie Details

```http
GET /details/movie/<tmdb_id>
```

Get comprehensive movie details with integrated credits and available torrent links.

**Example**: `/details/movie/550` (Fight Club)

**New in v5.0**: Credits are now integrated within `tmdb_details` as a single array.

#### TV Show Details

```http
GET /details/tv/<tmdb_id>
```

Get comprehensive TV show details with available torrent links.

**Example**: `/details/tv/1396` (Breaking Bad)

#### Season Details

```http
GET /details/tv/<tv_id>/season/<season_number>
```

Get detailed season information with torrent links for that season.

**Example**: `/details/tv/1396/season/1` (Breaking Bad Season 1)

**Search Strategy**:

- Searches: `"Breaking Bad S01"` + `"Breaking Bad Season 1"`
- Filters out episodes (no S01E01 patterns)
- Returns season packs only

#### Episode Details

```http
GET /details/tv/<tv_id>/season/<season_number>/episode/<episode_number>
```

Get detailed episode information with specific episode torrent links.

**Example**: `/details/tv/1396/season/1/episode/1` (Breaking Bad S1E1)

**Search Strategy**:

- Searches: `"Breaking Bad S01E01"` + `"Breaking Bad Season 1 Episode 1"`
- Returns episode-specific torrents

### Utility Endpoints

#### API Documentation

```http
GET /
```

Returns complete API documentation and available endpoints.

#### Health Check

```http
GET /health
```

Check API health and service status.

## 📊 Response Examples

### Search Response (TMDB Only)

```json
{
  "status": "success",
  "query": "breaking bad",
  "count": 5,
  "results": [
    {
      "id": 1396,
      "name": "Breaking Bad",
      "overview": "Walter White, a New Mexico chemistry teacher...",
      "first_air_date": "2008-01-20",
      "vote_average": 8.9,
      "poster_path": "https://image.tmdb.org/t/p/w500/ztkUQFLlC19CCMYHW9o1zWhJRNq.jpg",
      "backdrop_path": "https://image.tmdb.org/t/p/w500/9faGSFi5jam6pDWGNd0p8JcJgXQ.jpg"
    }
  ]
}
```

### Movie Detail Response (Streamlined + Integrated Credits)

```json
{
  "status": "success",
  "tmdb_details": {
    "id": 550,
    "title": "Fight Club",
    "overview": "A ticking-time-bomb insomniac...",
    "vote_average": 8.4,
    "genres": [{ "id": 18, "name": "Drama" }],
    "poster_path": "https://image.tmdb.org/t/p/w500/...",
    "backdrop_path": "https://image.tmdb.org/t/p/w500/...",
    "credits": [
      {
        "id": 287,
        "name": "Brad Pitt",
        "character": "Tyler Durden",
        "job": "Actor",
        "department": "Acting",
        "popularity": 15.15,
        "profile_path": "https://image.tmdb.org/t/p/w500/..."
      },
      {
        "id": 7467,
        "name": "David Fincher",
        "character": null,
        "job": "Director",
        "department": "Directing",
        "popularity": 8.64,
        "profile_path": "https://image.tmdb.org/t/p/w500/..."
      }
    ]
  },
  "torrent_count": 27,
  "torrent_results": [
    {
      "title": "Fight Club 1999 1080p BluRay x264",
      "magnet": "magnet:?xt=urn:btih:...",
      "size": "2.71 GiB",
      "seeders": 419,
      "leechers": 23,
      "quality": "1080p"
    }
  ]
}
```

**Note**:

- Torrents are automatically sorted by intelligent scoring (balanced size/seeders)
- 0-seeder torrents are filtered out completely
- Credits are integrated within tmdb_details as a single array
- Only essential TMDB fields are included (production data removed)

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_new_api.py
```

Test the balanced scoring system:

```bash
python test_balanced_scoring.py
```

This will demonstrate:

- 0-seeder filtering
- Balanced scoring algorithm
- Size vs seeders optimization
- Quality assessment indicators

## 🏗️ Project Structure

```
TorrentSearchApi/
├── .env                          # Environment variables
├── app.py                        # Main application entry point
├── config.py                     # Configuration management
├── requirements.txt              # Dependencies
├── test_new_api.py              # API test suite
├── test_balanced_scoring.py     # Scoring system test suite
├── services/                     # Business logic services
│   ├── __init__.py
│   ├── torrent_finder.py         # Torrent scraping service
│   └── tmdb_client.py            # TMDB API client
├── routes/                       # API route handlers
│   ├── __init__.py
│   ├── search_routes.py          # Search & detail endpoints
│   └── health_routes.py          # Health & documentation
└── utils/                        # Utility functions
    ├── __init__.py
    └── formatters.py             # Data formatting utilities
```

## 🔧 Configuration

All configuration is managed through environment variables in `.env`:

```env
# TMDB Configuration
TMDB_API_KEY=your_bearer_token_here
TMDB_BASE_URL=https://api.themoviedb.org/3
TMDB_IMAGE_BASE_URL=https://image.tmdb.org/t/p/w500

# Torrent Site Configuration
TORRENT_SITE_DOMAIN=tpirbay.site

# API Configuration
API_PORT=8001
```

## 🎯 Use Cases

- **Streaming Service UIs**: Streamlined metadata perfect for movie/TV catalogs
- **Media Centers**: Integration with Plex, Jellyfin, etc.
- **Content Discovery**: Search and browse movies/TV shows with integrated cast info
- **Torrent Automation**: Automated downloading with quality preferences
- **Mobile Apps**: Lightweight responses optimized for mobile displays

## 🔒 Security & Legal

- **No Authentication Required**: For basic search functionality
- **Rate Limiting**: Built-in delays to respect service limits
- **Legal Disclaimer**: This tool is for educational purposes. Users are responsible for compliance with local laws regarding torrenting.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **TMDB**: For providing comprehensive movie/TV metadata and cast information
- **The Pirate Bay**: For torrent availability data
- **Flask**: For the lightweight web framework
- **BeautifulSoup**: For reliable web scraping

---

**API Version**: 5.0  
**Last Updated**: 2024  
**Status**: Production Ready
