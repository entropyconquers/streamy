# Streamy API Schema Documentation

## Overview

This document provides comprehensive documentation for the **Streamy Torrent Search API v5.0** OpenAPI schema. The API follows OpenAPI 3.0.3 specification and provides structured access to movie/TV show metadata and torrent information.

## API Information

- **Title**: Streamy Torrent Search API
- **Version**: 5.0.0
- **Base URL**: `http://localhost:8001`
- **License**: MIT
- **OpenAPI Version**: 3.0.3

## Schema Access

The complete OpenAPI schema is available at:

```
GET /schema
```

This endpoint returns the full OpenAPI 3.0 specification in JSON format, which can be used with tools like Swagger UI, Postman, or any OpenAPI-compatible client.

## Endpoint Categories

### 🔍 Search Endpoints

Lightweight endpoints that return only TMDB search results (no torrent data).

### 📋 Detail Endpoints

Comprehensive endpoints that return TMDB metadata + torrent links with intelligent scoring.

### 🛠️ Utility Endpoints

Health checks, documentation, and schema access.

---

## Detailed Endpoint Documentation

### Search Endpoints

#### 1. Multi Search

```http
GET /search/{query}
```

**Description**: Search both movies and TV shows simultaneously.

**Parameters**:

- `query` (path, required): Search query string
  - Type: `string`
  - Example: `"breaking bad"`

**Response**: Returns top 5 TMDB results from both movies and TV shows.

**Response Schema**: `SearchResponse`

---

#### 2. Movie Search

```http
GET /movies/{query}
```

**Description**: Search movies only.

**Parameters**:

- `query` (path, required): Movie search query
  - Type: `string`
  - Example: `"inception"`

**Response**: Returns top 5 TMDB movie results.

**Response Schema**: `SearchResponse`

---

#### 3. TV Show Search

```http
GET /tv-shows/{query}
```

**Description**: Search TV shows only.

**Parameters**:

- `query` (path, required): TV show search query
  - Type: `string`
  - Example: `"breaking bad"`

**Response**: Returns top 5 TMDB TV show results.

**Response Schema**: `SearchResponse`

---

### Detail Endpoints

#### 4. Movie Details

```http
GET /details/movie/{tmdb_id}
```

**Description**: Get comprehensive movie details with integrated credits and torrent links.

**Parameters**:

- `tmdb_id` (path, required): TMDB movie ID
  - Type: `integer`
  - Example: `550` (Fight Club)

**Response**: Complete movie metadata with cast/crew and available torrents.

**Response Schema**: `MovieDetailsResponse`

**Features**:

- ✅ Streamlined TMDB metadata (essential fields only)
- ✅ Integrated credits (cast + crew in single array)
- ✅ Intelligent torrent scoring
- ✅ Quality detection and filtering

---

#### 5. TV Show Details

```http
GET /details/tv/{tmdb_id}
```

**Description**: Get comprehensive TV show details with torrent links.

**Parameters**:

- `tmdb_id` (path, required): TMDB TV show ID
  - Type: `integer`
  - Example: `1396` (Breaking Bad)

**Response**: Complete TV show metadata with available torrents.

**Response Schema**: `TvDetailsResponse`

---

#### 6. Season Details

```http
GET /details/tv/{tv_id}/season/{season_number}
```

**Description**: Get detailed season information with season-specific torrent links.

**Parameters**:

- `tv_id` (path, required): TMDB TV show ID
  - Type: `integer`
  - Example: `1396`
- `season_number` (path, required): Season number
  - Type: `integer`
  - Example: `1`

**Response**: Season metadata with season pack torrents.

**Response Schema**: `SeasonDetailsResponse`

**Advanced Search Strategy**:

- Uses multiple patterns: `"Show Name S01"` + `"Show Name Season 1"`
- Filters out individual episodes (removes S01E01 patterns)
- Returns only season packs and complete season torrents

---

#### 7. Episode Details

```http
GET /details/tv/{tv_id}/season/{season_number}/episode/{episode_number}
```

**Description**: Get detailed episode information with episode-specific torrent links.

**Parameters**:

- `tv_id` (path, required): TMDB TV show ID
  - Type: `integer`
  - Example: `1396`
- `season_number` (path, required): Season number
  - Type: `integer`
  - Example: `1`
- `episode_number` (path, required): Episode number
  - Type: `integer`
  - Example: `1`

**Response**: Episode metadata with episode-specific torrents.

**Response Schema**: `EpisodeDetailsResponse`

**Advanced Search Strategy**:

- Uses targeted patterns: `"Show Name S01E01"` + `"Show Name Season 1 Episode 1"`
- Returns episode-specific torrents only

---

### Utility Endpoints

#### 8. API Documentation

```http
GET /
```

**Description**: Returns comprehensive API documentation and feature overview.

**Response Schema**: `ApiDocumentation`

---

#### 9. Health Check

```http
GET /health
```

**Description**: Check API health and service status.

**Response Schema**: `HealthResponse`

---

#### 10. OpenAPI Schema

```http
GET /schema
```

**Description**: Returns the complete OpenAPI 3.0 schema specification.

**Response**: Full OpenAPI schema object

---

## Data Schemas

### Core Response Types

#### SearchResponse

```json
{
  "status": "success",
  "query": "breaking bad",
  "count": 5,
  "results": [SearchResult]
}
```

#### SearchResult

```json
{
  "id": 1396,
  "title": "Fight Club", // For movies
  "name": "Breaking Bad", // For TV shows
  "overview": "Description...",
  "release_date": "1999-10-15", // For movies
  "first_air_date": "2008-01-20", // For TV shows
  "vote_average": 8.9,
  "popularity": 61.416,
  "poster_path": "https://image.tmdb.org/t/p/w500/...",
  "backdrop_path": "https://image.tmdb.org/t/p/w500/...",
  "media_type": "tv" // "movie" or "tv"
}
```

---

### Detail Response Types

#### MovieDetailsResponse

```json
{
  "status": "success",
  "tmdb_details": MovieDetails,
  "torrent_count": 35,
  "torrent_results": [TorrentResult]
}
```

#### MovieDetails (Streamlined)

```json
{
  "id": 550,
  "title": "Fight Club",
  "overview": "A ticking-time-bomb insomniac...",
  "release_date": "1999-10-15",
  "vote_average": 8.438,
  "vote_count": 26280,
  "popularity": 61.416,
  "runtime": 139,
  "status": "Released",
  "tagline": "Mischief. Mayhem. Soap.",
  "original_language": "en",
  "original_title": "Fight Club",
  "adult": false,
  "imdb_id": "tt0137523",
  "homepage": "http://www.foxmovies.com/movies/fight-club",
  "poster_path": "https://image.tmdb.org/t/p/w500/...",
  "backdrop_path": "https://image.tmdb.org/t/p/w500/...",
  "genres": [Genre],
  "spoken_languages": [SpokenLanguage],
  "credits": [Credit]  // ⭐ NEW: Integrated credits array
}
```

---

### Integrated Credits Structure

#### Credit (Combined Cast & Crew)

```json
{
  "id": 287,
  "name": "Brad Pitt",
  "character": "Tyler Durden", // null for crew
  "job": "Actor", // "Actor" for cast, actual job for crew
  "department": "Acting",
  "popularity": 15.1539,
  "profile_path": "https://image.tmdb.org/t/p/w500/...",
  "order": 1
}
```

**Key Features**:

- ✅ **Single Array**: Cast and crew combined (easier to display)
- ✅ **Popularity Sorted**: Most important people first (top 20)
- ✅ **Standardized Structure**: Consistent format for all credit types
- ✅ **Full Image URLs**: Ready-to-use profile image links
- ✅ **Streaming Optimized**: Only essential fields for UI display

---

### Torrent Data

#### TorrentResult

```json
{
  "title": "Fight.Club.1999.REMASTERED.1080p.BluRay.DDP5.1.x265.10bit-Galaxy",
  "magnet": "magnet:?xt=urn:btih:...",
  "size": "4.01 GiB",
  "seeders": 252,
  "leechers": 15,
  "quality": "1080p" // Auto-detected quality
}
```

**Intelligent Scoring Features**:

- ✅ **0-Seeder Filtering**: Unusable torrents removed completely
- ✅ **Balanced Algorithm**: Considers size, seeders, and availability
- ✅ **Quality Detection**: Automatic quality extraction (4K, 1080p, 720p, etc.)
- ✅ **Size Optimization**: Sweet spot between quality and download time

---

### Supporting Schemas

#### Genre

```json
{
  "id": 18,
  "name": "Drama"
}
```

#### SpokenLanguage

```json
{
  "iso_639_1": "en",
  "name": "English"
}
```

#### Season

```json
{
  "id": 3572,
  "name": "Season 1",
  "season_number": 1,
  "episode_count": 7,
  "air_date": "2008-01-20",
  "overview": "Season description...",
  "poster_path": "https://image.tmdb.org/t/p/w500/..."
}
```

#### Episode

```json
{
  "id": 62085,
  "name": "Pilot",
  "episode_number": 1,
  "season_number": 1,
  "air_date": "2008-01-20",
  "overview": "Episode description...",
  "vote_average": 7.7,
  "runtime": 58,
  "still_path": "https://image.tmdb.org/t/p/w500/..."
}
```

---

## Error Handling

### ErrorResponse

```json
{
  "status": "error",
  "message": "Content not found"
}
```

**Common HTTP Status Codes**:

- `200`: Success
- `400`: Invalid content type
- `404`: Content not found
- `500`: Internal server error
- `503`: TMDB service unavailable

---

## Key Features & Benefits

### 🎯 Streamlined TMDB Structure

**Removed Unnecessary Fields**:

- `production_companies`, `production_countries`, `belongs_to_collection`
- `budget`, `revenue`, `video`, `networks`, `created_by`
- All production-related metadata not needed for streaming UIs

**Benefits**:

- ✅ **20% Smaller Responses**: Faster loading and reduced bandwidth
- ✅ **UI Optimized**: Only fields needed for streaming app displays
- ✅ **Cleaner Structure**: Easier to parse and work with

### 🎬 Integrated Credits

**New Structure**:

- Cast and crew combined in single `credits` array within `tmdb_details`
- Sorted by popularity (most important people first)
- Top 20 credits only (optimized for mobile displays)
- Standardized structure for both actors and crew

**Benefits**:

- ✅ **Easier Display**: Single array instead of separate cast/crew objects
- ✅ **Popularity Sorted**: Most important people appear first
- ✅ **Mobile Friendly**: Optimized count for mobile UI constraints
- ✅ **Consistent Format**: Same structure for all credit types

### 🧠 Intelligent Torrent Scoring

**Scoring Algorithm**:

1. **Seeders** (Primary): Higher seeders = better availability
2. **Size Optimization**: Sweet spot between quality and download time
3. **Bonus System**: Extra points for high-seeder torrents
4. **Quality Filtering**: Removes 0-seeder torrents automatically

**Size Categories**:

- `< 100MB`: Poor quality penalty (0.3x multiplier)
- `100MB - 500MB`: Small file penalty (0.6x multiplier)
- `500MB - 3GB`: Sweet spot (1.0x multiplier) ⭐
- `3GB - 8GB`: Large file slight penalty (0.8x multiplier)
- `> 8GB`: Very large penalty (0.5x multiplier)

**Seeder Bonuses**:

- `10+ seeders`: 20% bonus (excellent availability)
- `5+ seeders`: 10% bonus (good availability)
- `0 seeders`: Filtered out completely

### 🔍 Advanced Search Patterns

**Season Search Intelligence**:

- Multiple search patterns: `"Show Name S01"` + `"Show Name Season 1"`
- Episode filtering: Removes individual episodes (S01E01 patterns)
- Deduplication: Combines and removes duplicate results
- Result focus: Only season packs and complete season torrents

**Episode Search Intelligence**:

- Targeted patterns: `"Show Name S01E01"` + `"Show Name Season 1 Episode 1"`
- Specific targeting: Searches for exact episode, not episode name
- Multiple strategies: Combines results from different search approaches

---

## Usage Examples

### 1. Search for Content

```bash
# General search
curl "http://localhost:8001/search/breaking%20bad"

# Movie-specific search
curl "http://localhost:8001/movies/inception"

# TV show-specific search
curl "http://localhost:8001/tv-shows/breaking%20bad"
```

### 2. Get Detailed Information

```bash
# Movie details with torrents and credits
curl "http://localhost:8001/details/movie/550"

# TV show details
curl "http://localhost:8001/details/tv/1396"

# Season details with season torrents
curl "http://localhost:8001/details/tv/1396/season/1"

# Episode details with episode torrents
curl "http://localhost:8001/details/tv/1396/season/1/episode/1"
```

### 3. API Information

```bash
# Get API documentation
curl "http://localhost:8001/"

# Check health status
curl "http://localhost:8001/health"

# Get OpenAPI schema
curl "http://localhost:8001/schema"
```

---

## Integration Guide

### Using with OpenAPI Tools

1. **Swagger UI**: Import the schema from `/schema` endpoint
2. **Postman**: Import OpenAPI spec for automatic collection generation
3. **Code Generation**: Use OpenAPI generators for client SDKs
4. **API Testing**: Use schema for automated testing and validation

### Frontend Integration

The API is optimized for streaming service UIs with:

- Ready-to-use image URLs (no additional processing needed)
- Streamlined metadata (only essential fields)
- Integrated credits (single array for easy display)
- Quality-sorted torrents (best options first)
- Mobile-optimized response sizes

### Backend Integration

- RESTful design follows standard conventions
- Consistent error handling across all endpoints
- JSON responses with proper HTTP status codes
- Environment-based configuration support

---

## Schema Validation

The OpenAPI schema includes:

- ✅ **Required Fields**: Clearly marked required vs optional fields
- ✅ **Data Types**: Proper type definitions (string, integer, number, boolean)
- ✅ **Format Validation**: Date formats, URI formats, etc.
- ✅ **Examples**: Real-world examples for all schemas
- ✅ **Descriptions**: Detailed descriptions for all fields and endpoints
- ✅ **Enum Values**: Defined allowed values where applicable

This comprehensive schema ensures reliable API integration and enables automatic validation, testing, and documentation generation.
