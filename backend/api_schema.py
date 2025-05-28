#!/usr/bin/env python3
"""
OpenAPI Schema for Streamy Torrent Search API v5.0
Comprehensive API documentation with request/response schemas
"""

# OpenAPI 3.0 Schema Definition
API_SCHEMA = {
    "openapi": "3.0.3",
    "info": {
        "title": "Streamy Torrent Search API",
        "version": "5.0.0",
        "description": "A modern, modular torrent search API that integrates The Movie Database (TMDB) for rich metadata and scrapes torrent sites for magnet links. Perfect for building streaming service UIs.",
        "contact": {
            "name": "API Support",
            "url": "https://github.com/your-repo/streamy-api"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    },
    "servers": [
        {
            "url": "http://localhost:8001",
            "description": "Development server"
        }
    ],
    "tags": [
        {
            "name": "search",
            "description": "Search endpoints for movies and TV shows"
        },
        {
            "name": "details",
            "description": "Detailed information with torrent links"
        },
        {
            "name": "utility",
            "description": "Health checks and documentation"
        }
    ],
    "paths": {
        "/": {
            "get": {
                "tags": ["utility"],
                "summary": "API Documentation",
                "description": "Returns comprehensive API documentation and available endpoints",
                "responses": {
                    "200": {
                        "description": "API documentation",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ApiDocumentation"}
                            }
                        }
                    }
                }
            }
        },
        "/health": {
            "get": {
                "tags": ["utility"],
                "summary": "Health Check",
                "description": "Check API health and service status",
                "responses": {
                    "200": {
                        "description": "Service is healthy",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/HealthResponse"}
                            }
                        }
                    },
                    "500": {
                        "description": "Service error",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/schema": {
            "get": {
                "tags": ["utility"],
                "summary": "OpenAPI Schema",
                "description": "Returns the complete OpenAPI 3.0 schema for this API",
                "responses": {
                    "200": {
                        "description": "OpenAPI schema",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "description": "Complete OpenAPI 3.0 specification"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/search/{query}": {
            "get": {
                "tags": ["search"],
                "summary": "Multi Search",
                "description": "Search both movies and TV shows, returns top 5 TMDB results",
                "parameters": [
                    {
                        "name": "query",
                        "in": "path",
                        "required": True,
                        "description": "Search query string",
                        "schema": {
                            "type": "string",
                            "example": "breaking bad"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Search results",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SearchResponse"}
                            }
                        }
                    },
                    "500": {
                        "description": "Search failed",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "503": {
                        "description": "TMDB service unavailable",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/movies/{query}": {
            "get": {
                "tags": ["search"],
                "summary": "Movie Search",
                "description": "Search movies only, returns top 5 TMDB results",
                "parameters": [
                    {
                        "name": "query",
                        "in": "path",
                        "required": True,
                        "description": "Movie search query",
                        "schema": {
                            "type": "string",
                            "example": "inception"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Movie search results",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SearchResponse"}
                            }
                        }
                    },
                    "500": {
                        "description": "Search failed",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/tv-shows/{query}": {
            "get": {
                "tags": ["search"],
                "summary": "TV Show Search",
                "description": "Search TV shows only, returns top 5 TMDB results",
                "parameters": [
                    {
                        "name": "query",
                        "in": "path",
                        "required": True,
                        "description": "TV show search query",
                        "schema": {
                            "type": "string",
                            "example": "breaking bad"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "TV show search results",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SearchResponse"}
                            }
                        }
                    },
                    "500": {
                        "description": "Search failed",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/details/movie/{tmdb_id}": {
            "get": {
                "tags": ["details"],
                "summary": "Movie Details",
                "description": "Get comprehensive movie details with integrated credits and available torrent links",
                "parameters": [
                    {
                        "name": "tmdb_id",
                        "in": "path",
                        "required": True,
                        "description": "TMDB movie ID",
                        "schema": {
                            "type": "integer",
                            "example": 550
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Movie details with torrents",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/MovieDetailsResponse"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid content type",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "404": {
                        "description": "Movie not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/details/tv/{tmdb_id}": {
            "get": {
                "tags": ["details"],
                "summary": "TV Show Details",
                "description": "Get comprehensive TV show details with available torrent links",
                "parameters": [
                    {
                        "name": "tmdb_id",
                        "in": "path",
                        "required": True,
                        "description": "TMDB TV show ID",
                        "schema": {
                            "type": "integer",
                            "example": 1396
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "TV show details with torrents",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TvDetailsResponse"}
                            }
                        }
                    },
                    "404": {
                        "description": "TV show not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/details/tv/{tv_id}/season/{season_number}": {
            "get": {
                "tags": ["details"],
                "summary": "Season Details",
                "description": "Get detailed season information with torrent links for that season",
                "parameters": [
                    {
                        "name": "tv_id",
                        "in": "path",
                        "required": True,
                        "description": "TMDB TV show ID",
                        "schema": {
                            "type": "integer",
                            "example": 1396
                        }
                    },
                    {
                        "name": "season_number",
                        "in": "path",
                        "required": True,
                        "description": "Season number",
                        "schema": {
                            "type": "integer",
                            "example": 1
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Season details with torrents",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SeasonDetailsResponse"}
                            }
                        }
                    },
                    "404": {
                        "description": "Season not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        },
        "/details/tv/{tv_id}/season/{season_number}/episode/{episode_number}": {
            "get": {
                "tags": ["details"],
                "summary": "Episode Details",
                "description": "Get detailed episode information with specific episode torrent links",
                "parameters": [
                    {
                        "name": "tv_id",
                        "in": "path",
                        "required": True,
                        "description": "TMDB TV show ID",
                        "schema": {
                            "type": "integer",
                            "example": 1396
                        }
                    },
                    {
                        "name": "season_number",
                        "in": "path",
                        "required": True,
                        "description": "Season number",
                        "schema": {
                            "type": "integer",
                            "example": 1
                        }
                    },
                    {
                        "name": "episode_number",
                        "in": "path",
                        "required": True,
                        "description": "Episode number",
                        "schema": {
                            "type": "integer",
                            "example": 1
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Episode details with torrents",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/EpisodeDetailsResponse"}
                            }
                        }
                    },
                    "404": {
                        "description": "Episode not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "ErrorResponse": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "error"
                    },
                    "message": {
                        "type": "string",
                        "example": "Content not found"
                    }
                },
                "required": ["status", "message"]
            },
            "HealthResponse": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "healthy"
                    },
                    "api_version": {
                        "type": "string",
                        "example": "5.0"
                    },
                    "services": {
                        "type": "object",
                        "properties": {
                            "torrent_scraping": {
                                "type": "string",
                                "example": "active"
                            },
                            "tmdb_integration": {
                                "type": "string",
                                "example": "connected"
                            }
                        }
                    },
                    "features": {
                        "type": "object",
                        "properties": {
                            "intelligent_scoring": {
                                "type": "string",
                                "example": "active"
                            },
                            "quality_filtering": {
                                "type": "string",
                                "example": "active"
                            },
                            "integrated_credits": {
                                "type": "string",
                                "example": "active"
                            }
                        }
                    },
                    "timestamp": {
                        "type": "string",
                        "example": "live"
                    }
                }
            },
            "ApiDocumentation": {
                "type": "object",
                "properties": {
                    "api_name": {
                        "type": "string",
                        "example": "Torrent Search API"
                    },
                    "version": {
                        "type": "string",
                        "example": "5.0"
                    },
                    "description": {
                        "type": "string"
                    },
                    "features": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "endpoints": {
                        "type": "object"
                    }
                }
            },
            "SearchResponse": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "success"
                    },
                    "query": {
                        "type": "string",
                        "example": "breaking bad"
                    },
                    "count": {
                        "type": "integer",
                        "example": 5
                    },
                    "results": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/SearchResult"
                        }
                    }
                },
                "required": ["status", "query", "count", "results"]
            },
            "SearchResult": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 1396
                    },
                    "title": {
                        "type": "string",
                        "example": "Fight Club"
                    },
                    "name": {
                        "type": "string",
                        "example": "Breaking Bad"
                    },
                    "overview": {
                        "type": "string",
                        "example": "Walter White, a New Mexico chemistry teacher..."
                    },
                    "release_date": {
                        "type": "string",
                        "format": "date",
                        "example": "1999-10-15"
                    },
                    "first_air_date": {
                        "type": "string",
                        "format": "date",
                        "example": "2008-01-20"
                    },
                    "vote_average": {
                        "type": "number",
                        "format": "float",
                        "example": 8.9
                    },
                    "popularity": {
                        "type": "number",
                        "format": "float",
                        "example": 61.416
                    },
                    "poster_path": {
                        "type": "string",
                        "format": "uri",
                        "example": "https://image.tmdb.org/t/p/w500/ztkUQFLlC19CCMYHW9o1zWhJRNq.jpg"
                    },
                    "backdrop_path": {
                        "type": "string",
                        "format": "uri",
                        "example": "https://image.tmdb.org/t/p/w500/9faGSFi5jam6pDWGNd0p8JcJgXQ.jpg"
                    },
                    "media_type": {
                        "type": "string",
                        "enum": ["movie", "tv"],
                        "example": "tv"
                    }
                }
            },
            "MovieDetailsResponse": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "success"
                    },
                    "tmdb_details": {
                        "$ref": "#/components/schemas/MovieDetails"
                    },
                    "torrent_count": {
                        "type": "integer",
                        "example": 35
                    },
                    "torrent_results": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/TorrentResult"
                        }
                    }
                },
                "required": ["status", "tmdb_details", "torrent_count", "torrent_results"]
            },
            "TvDetailsResponse": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "success"
                    },
                    "tmdb_details": {
                        "$ref": "#/components/schemas/TvDetails"
                    },
                    "torrent_count": {
                        "type": "integer",
                        "example": 27
                    },
                    "torrent_results": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/TorrentResult"
                        }
                    }
                },
                "required": ["status", "tmdb_details", "torrent_count", "torrent_results"]
            },
            "SeasonDetailsResponse": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "success"
                    },
                    "tv_show_name": {
                        "type": "string",
                        "example": "Breaking Bad"
                    },
                    "season_details": {
                        "$ref": "#/components/schemas/SeasonDetails"
                    },
                    "torrent_count": {
                        "type": "integer",
                        "example": 95
                    },
                    "torrent_results": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/TorrentResult"
                        }
                    }
                },
                "required": ["status", "tv_show_name", "season_details", "torrent_count", "torrent_results"]
            },
            "EpisodeDetailsResponse": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "success"
                    },
                    "tv_show_name": {
                        "type": "string",
                        "example": "Breaking Bad"
                    },
                    "episode_details": {
                        "$ref": "#/components/schemas/EpisodeDetails"
                    },
                    "torrent_count": {
                        "type": "integer",
                        "example": 17
                    },
                    "torrent_results": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/TorrentResult"
                        }
                    }
                },
                "required": ["status", "tv_show_name", "episode_details", "torrent_count", "torrent_results"]
            },
            "MovieDetails": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 550
                    },
                    "title": {
                        "type": "string",
                        "example": "Fight Club"
                    },
                    "overview": {
                        "type": "string",
                        "example": "A ticking-time-bomb insomniac and a slippery soap salesman..."
                    },
                    "release_date": {
                        "type": "string",
                        "format": "date",
                        "example": "1999-10-15"
                    },
                    "vote_average": {
                        "type": "number",
                        "format": "float",
                        "example": 8.438
                    },
                    "vote_count": {
                        "type": "integer",
                        "example": 26280
                    },
                    "popularity": {
                        "type": "number",
                        "format": "float",
                        "example": 61.416
                    },
                    "runtime": {
                        "type": "integer",
                        "example": 139
                    },
                    "status": {
                        "type": "string",
                        "example": "Released"
                    },
                    "tagline": {
                        "type": "string",
                        "example": "Mischief. Mayhem. Soap."
                    },
                    "original_language": {
                        "type": "string",
                        "example": "en"
                    },
                    "original_title": {
                        "type": "string",
                        "example": "Fight Club"
                    },
                    "adult": {
                        "type": "boolean",
                        "example": False
                    },
                    "imdb_id": {
                        "type": "string",
                        "example": "tt0137523"
                    },
                    "homepage": {
                        "type": "string",
                        "format": "uri",
                        "example": "http://www.foxmovies.com/movies/fight-club"
                    },
                    "poster_path": {
                        "type": "string",
                        "format": "uri",
                        "example": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg"
                    },
                    "backdrop_path": {
                        "type": "string",
                        "format": "uri",
                        "example": "https://image.tmdb.org/t/p/w500/fCayJrkfRaCRCTh8GqN30f8oyQF.jpg"
                    },
                    "genres": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/Genre"
                        }
                    },
                    "spoken_languages": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/SpokenLanguage"
                        }
                    },
                    "credits": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/Credit"
                        },
                        "description": "Top 20 cast and crew members sorted by popularity"
                    }
                },
                "required": ["id", "title", "overview"]
            },
            "TvDetails": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 1396
                    },
                    "name": {
                        "type": "string",
                        "example": "Breaking Bad"
                    },
                    "overview": {
                        "type": "string",
                        "example": "Walter White, a New Mexico chemistry teacher..."
                    },
                    "first_air_date": {
                        "type": "string",
                        "format": "date",
                        "example": "2008-01-20"
                    },
                    "last_air_date": {
                        "type": "string",
                        "format": "date",
                        "example": "2013-09-29"
                    },
                    "vote_average": {
                        "type": "number",
                        "format": "float",
                        "example": 8.9
                    },
                    "vote_count": {
                        "type": "integer",
                        "example": 12345
                    },
                    "popularity": {
                        "type": "number",
                        "format": "float",
                        "example": 123.456
                    },
                    "number_of_episodes": {
                        "type": "integer",
                        "example": 62
                    },
                    "number_of_seasons": {
                        "type": "integer",
                        "example": 5
                    },
                    "episode_run_time": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        },
                        "example": [45, 47]
                    },
                    "in_production": {
                        "type": "boolean",
                        "example": False
                    },
                    "status": {
                        "type": "string",
                        "example": "Ended"
                    },
                    "type": {
                        "type": "string",
                        "example": "Scripted"
                    },
                    "original_language": {
                        "type": "string",
                        "example": "en"
                    },
                    "original_name": {
                        "type": "string",
                        "example": "Breaking Bad"
                    },
                    "adult": {
                        "type": "boolean",
                        "example": False
                    },
                    "homepage": {
                        "type": "string",
                        "format": "uri"
                    },
                    "poster_path": {
                        "type": "string",
                        "format": "uri"
                    },
                    "backdrop_path": {
                        "type": "string",
                        "format": "uri"
                    },
                    "genres": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/Genre"
                        }
                    },
                    "spoken_languages": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/SpokenLanguage"
                        }
                    },
                    "seasons": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/Season"
                        }
                    }
                },
                "required": ["id", "name", "overview"]
            },
            "SeasonDetails": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 3572
                    },
                    "name": {
                        "type": "string",
                        "example": "Season 1"
                    },
                    "overview": {
                        "type": "string",
                        "example": "High school chemistry teacher Walter White's life is suddenly transformed..."
                    },
                    "season_number": {
                        "type": "integer",
                        "example": 1
                    },
                    "episode_count": {
                        "type": "integer",
                        "example": 7
                    },
                    "air_date": {
                        "type": "string",
                        "format": "date",
                        "example": "2008-01-20"
                    },
                    "poster_path": {
                        "type": "string",
                        "format": "uri"
                    },
                    "episodes": {
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/Episode"
                        }
                    }
                },
                "required": ["id", "name", "season_number"]
            },
            "EpisodeDetails": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 62085
                    },
                    "name": {
                        "type": "string",
                        "example": "Pilot"
                    },
                    "overview": {
                        "type": "string",
                        "example": "Walter White, a struggling high school chemistry teacher..."
                    },
                    "episode_number": {
                        "type": "integer",
                        "example": 1
                    },
                    "season_number": {
                        "type": "integer",
                        "example": 1
                    },
                    "air_date": {
                        "type": "string",
                        "format": "date",
                        "example": "2008-01-20"
                    },
                    "vote_average": {
                        "type": "number",
                        "format": "float",
                        "example": 7.7
                    },
                    "runtime": {
                        "type": "integer",
                        "example": 58
                    },
                    "still_path": {
                        "type": "string",
                        "format": "uri"
                    }
                },
                "required": ["id", "name", "episode_number", "season_number"]
            },
            "TorrentResult": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "example": "Fight.Club.1999.REMASTERED.1080p.BluRay.DDP5.1.x265.10bit-Galaxy"
                    },
                    "magnet": {
                        "type": "string",
                        "example": "magnet:?xt=urn:btih:..."
                    },
                    "size": {
                        "type": "string",
                        "example": "4.01 GiB"
                    },
                    "seeders": {
                        "type": "integer",
                        "example": 252
                    },
                    "leechers": {
                        "type": "integer",
                        "example": 15
                    },
                    "quality": {
                        "type": "string",
                        "example": "1080p"
                    }
                },
                "required": ["title", "magnet", "size", "seeders", "leechers"]
            },
            "Credit": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 287
                    },
                    "name": {
                        "type": "string",
                        "example": "Brad Pitt"
                    },
                    "character": {
                        "type": "string",
                        "nullable": True,
                        "example": "Tyler Durden"
                    },
                    "job": {
                        "type": "string",
                        "example": "Actor"
                    },
                    "department": {
                        "type": "string",
                        "example": "Acting"
                    },
                    "popularity": {
                        "type": "number",
                        "format": "float",
                        "example": 15.1539
                    },
                    "profile_path": {
                        "type": "string",
                        "format": "uri",
                        "nullable": True,
                        "example": "https://image.tmdb.org/t/p/w500/cckcYc2v0yh1tc9QjRelptcOBko.jpg"
                    },
                    "order": {
                        "type": "integer",
                        "example": 1
                    }
                },
                "required": ["id", "name", "job", "department", "popularity"]
            },
            "Genre": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 18
                    },
                    "name": {
                        "type": "string",
                        "example": "Drama"
                    }
                },
                "required": ["id", "name"]
            },
            "SpokenLanguage": {
                "type": "object",
                "properties": {
                    "iso_639_1": {
                        "type": "string",
                        "example": "en"
                    },
                    "name": {
                        "type": "string",
                        "example": "English"
                    }
                },
                "required": ["iso_639_1", "name"]
            },
            "Season": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 3572
                    },
                    "name": {
                        "type": "string",
                        "example": "Season 1"
                    },
                    "season_number": {
                        "type": "integer",
                        "example": 1
                    },
                    "episode_count": {
                        "type": "integer",
                        "example": 7
                    },
                    "air_date": {
                        "type": "string",
                        "format": "date",
                        "example": "2008-01-20"
                    },
                    "overview": {
                        "type": "string",
                        "example": "High school chemistry teacher Walter White's life is suddenly transformed..."
                    },
                    "poster_path": {
                        "type": "string",
                        "format": "uri",
                        "nullable": True
                    }
                },
                "required": ["id", "name", "season_number"]
            },
            "Episode": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "example": 62085
                    },
                    "name": {
                        "type": "string",
                        "example": "Pilot"
                    },
                    "episode_number": {
                        "type": "integer",
                        "example": 1
                    },
                    "season_number": {
                        "type": "integer",
                        "example": 1
                    },
                    "air_date": {
                        "type": "string",
                        "format": "date",
                        "example": "2008-01-20"
                    },
                    "overview": {
                        "type": "string",
                        "example": "Walter White, a struggling high school chemistry teacher..."
                    },
                    "vote_average": {
                        "type": "number",
                        "format": "float",
                        "example": 7.7
                    },
                    "runtime": {
                        "type": "integer",
                        "example": 58
                    },
                    "still_path": {
                        "type": "string",
                        "format": "uri",
                        "nullable": True
                    }
                },
                "required": ["id", "name", "episode_number", "season_number"]
            }
        }
    }
}

def get_api_schema():
    """Return the complete OpenAPI schema"""
    return API_SCHEMA 