/**
 * Streamy API Service
 * Connects to the backend API for movie and TV show data
 */

const API_BASE_URL = "http://172.16.0.102:8001";

export interface SearchResult {
  id: number;
  title?: string;
  name?: string;
  overview: string;
  release_date?: string;
  first_air_date?: string;
  vote_average: number;
  popularity: number;
  poster_path: string;
  backdrop_path: string;
  media_type: "movie" | "tv";
}

export interface TorrentResult {
  title: string;
  magnet: string;
  size: string;
  seeders: number;
  leechers: number;
  quality?: string;
}

export interface Credit {
  id: number;
  name: string;
  character?: string;
  job: string;
  department: string;
  popularity: number;
  profile_path?: string;
  order?: number;
}

export interface Genre {
  id: number;
  name: string;
}

export interface MovieDetails {
  id: number;
  title: string;
  overview: string;
  release_date: string;
  vote_average: number;
  vote_count: number;
  popularity: number;
  runtime: number;
  status: string;
  tagline?: string;
  original_language: string;
  original_title: string;
  adult: boolean;
  imdb_id?: string;
  homepage?: string;
  poster_path: string;
  backdrop_path: string;
  genres: Genre[];
  credits: Credit[];
}

export interface TvDetails {
  id: number;
  name: string;
  overview: string;
  first_air_date: string;
  last_air_date?: string;
  vote_average: number;
  vote_count: number;
  popularity: number;
  number_of_episodes: number;
  number_of_seasons: number;
  episode_run_time: number[];
  in_production: boolean;
  status: string;
  type: string;
  original_language: string;
  original_name: string;
  adult: boolean;
  homepage?: string;
  poster_path: string;
  backdrop_path: string;
  genres: Genre[];
}

export interface SearchResponse {
  status: string;
  query: string;
  count: number;
  results: SearchResult[];
}

export interface MovieDetailsResponse {
  status: string;
  tmdb_details: MovieDetails;
  torrent_count: number;
  torrent_results: TorrentResult[];
}

export interface TvDetailsResponse {
  status: string;
  tmdb_details: TvDetails;
  torrent_count: number;
  torrent_results: TorrentResult[];
}

class StreamyAPI {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async request<T>(endpoint: string): Promise<T> {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // Search endpoints
  async multiSearch(query: string): Promise<SearchResponse> {
    return this.request<SearchResponse>(`/search/${encodeURIComponent(query)}`);
  }

  async searchMovies(query: string): Promise<SearchResponse> {
    return this.request<SearchResponse>(`/movies/${encodeURIComponent(query)}`);
  }

  async searchTvShows(query: string): Promise<SearchResponse> {
    return this.request<SearchResponse>(
      `/tv-shows/${encodeURIComponent(query)}`
    );
  }

  // Detail endpoints
  async getMovieDetails(tmdbId: number): Promise<MovieDetailsResponse> {
    return this.request<MovieDetailsResponse>(`/details/movie/${tmdbId}`);
  }

  async getTvDetails(tmdbId: number): Promise<TvDetailsResponse> {
    return this.request<TvDetailsResponse>(`/details/tv/${tmdbId}`);
  }

  async getSeasonDetails(tvId: number, seasonNumber: number): Promise<any> {
    return this.request(`/details/tv/${tvId}/season/${seasonNumber}`);
  }

  async getEpisodeDetails(
    tvId: number,
    seasonNumber: number,
    episodeNumber: number
  ): Promise<any> {
    return this.request(
      `/details/tv/${tvId}/season/${seasonNumber}/episode/${episodeNumber}`
    );
  }

  // Utility endpoints
  async getApiHealth(): Promise<any> {
    return this.request("/health");
  }

  async getApiDocs(): Promise<any> {
    return this.request("/");
  }

  // Helper methods for trending/popular content
  async getTrendingContent(): Promise<SearchResult[]> {
    try {
      // Search for different popular movies and shows, take first result from each
      const [
        inceptionResponse,
        breakingBadResponse,
        darkKnightResponse,
        gameOfThronesResponse,
        interstellarResponse,
        strangerthingsResponse,
      ] = await Promise.all([
        this.searchMovies("inception"),
        this.searchTvShows("breaking bad"),
        this.searchMovies("the dark knight"),
        this.searchTvShows("game of thrones"),
        this.searchMovies("interstellar"),
        this.searchTvShows("stranger things"),
      ]);

      // Take first result from each search for diversity
      const results = [
        inceptionResponse.results[0],
        breakingBadResponse.results[0],
        darkKnightResponse.results[0],
        gameOfThronesResponse.results[0],
        interstellarResponse.results[0],
        strangerthingsResponse.results[0],
      ].filter(Boolean);

      return results;
    } catch (error) {
      console.error("Failed to get trending content:", error);
      return [];
    }
  }

  async getFeaturedContent(): Promise<SearchResult[]> {
    try {
      // Get diverse featured content by searching specific popular movie/show titles
      const [
        inceptionResponse,
        breakingBadResponse,
        darkKnightResponse,
        gameOfThronesResponse,
        interstellarResponse,
        strangerthingsResponse,
        godfatherResponse,
        theOfficeResponse,
        pulpFictionResponse,
        friendsResponse,
        fightClubResponse,
        theWireResponse,
      ] = await Promise.all([
        this.searchMovies("inception"),
        this.searchTvShows("breaking bad"),
        this.searchMovies("the dark knight"),
        this.searchTvShows("game of thrones"),
        this.searchMovies("interstellar"),
        this.searchTvShows("stranger things"),
        this.searchMovies("the godfather"),
        this.searchTvShows("the office"),
        this.searchMovies("pulp fiction"),
        this.searchTvShows("friends"),
        this.searchMovies("fight club"),
        this.searchTvShows("the wire"),
      ]);

      // Take first result from each search for a diverse hero carousel
      const results = [
        inceptionResponse.results[0],
        breakingBadResponse.results[0],
        darkKnightResponse.results[0],
        gameOfThronesResponse.results[0],
        interstellarResponse.results[0],
        strangerthingsResponse.results[0],
        godfatherResponse.results[0],
        theOfficeResponse.results[0],
        pulpFictionResponse.results[0],
        friendsResponse.results[0],
        fightClubResponse.results[0],
        theWireResponse.results[0],
      ].filter(Boolean);

      return results;
    } catch (error) {
      console.error("Failed to get featured content:", error);
      return [];
    }
  }

  // Additional helper methods for specific content categories
  async getActionContent(): Promise<SearchResult[]> {
    try {
      const [
        johnWickResponse,
        madMaxResponse,
        dieHardResponse,
        terminatorResponse,
        matrixResponse,
      ] = await Promise.all([
        this.searchMovies("john wick"),
        this.searchMovies("mad max fury road"),
        this.searchMovies("die hard"),
        this.searchMovies("terminator 2"),
        this.searchMovies("the matrix"),
      ]);

      // Take first result from each search for variety
      const results = [
        johnWickResponse.results[0],
        madMaxResponse.results[0],
        dieHardResponse.results[0],
        terminatorResponse.results[0],
        matrixResponse.results[0],
      ].filter(Boolean);

      return results;
    } catch (error) {
      console.error("Failed to get action content:", error);
      return [];
    }
  }

  async getComedyContent(): Promise<SearchResult[]> {
    try {
      const [
        officeResponse,
        friendsResponse,
        brooklynResponse,
        parksResponse,
        seinfeldResponse,
      ] = await Promise.all([
        this.searchTvShows("the office"),
        this.searchTvShows("friends"),
        this.searchTvShows("brooklyn nine nine"),
        this.searchTvShows("parks and recreation"),
        this.searchTvShows("seinfeld"),
      ]);

      // Take first result from each search for variety
      const results = [
        officeResponse.results[0],
        friendsResponse.results[0],
        brooklynResponse.results[0],
        parksResponse.results[0],
        seinfeldResponse.results[0],
      ].filter(Boolean);

      return results;
    } catch (error) {
      console.error("Failed to get comedy content:", error);
      return [];
    }
  }

  async getSciFiContent(): Promise<SearchResult[]> {
    try {
      const [
        bladeRunnerResponse,
        interstellarResponse,
        matrixResponse,
        alienResponse,
        starWarsResponse,
      ] = await Promise.all([
        this.searchMovies("blade runner 2049"),
        this.searchMovies("interstellar"),
        this.searchMovies("the matrix"),
        this.searchMovies("alien"),
        this.searchMovies("star wars"),
      ]);

      // Take first result from each search for variety
      const results = [
        bladeRunnerResponse.results[0],
        interstellarResponse.results[0],
        matrixResponse.results[0],
        alienResponse.results[0],
        starWarsResponse.results[0],
      ].filter(Boolean);

      return results;
    } catch (error) {
      console.error("Failed to get sci-fi content:", error);
      return [];
    }
  }

  async getDramaContent(): Promise<SearchResult[]> {
    try {
      const [
        godfatherResponse,
        shawshankResponse,
        breakingBadResponse,
        sopranosResponse,
        goodfellasResponse,
      ] = await Promise.all([
        this.searchMovies("the godfather"),
        this.searchMovies("the shawshank redemption"),
        this.searchTvShows("breaking bad"),
        this.searchTvShows("the sopranos"),
        this.searchMovies("goodfellas"),
      ]);

      // Take first result from each search for variety
      const results = [
        godfatherResponse.results[0],
        shawshankResponse.results[0],
        breakingBadResponse.results[0],
        sopranosResponse.results[0],
        goodfellasResponse.results[0],
      ].filter(Boolean);

      return results;
    } catch (error) {
      console.error("Failed to get drama content:", error);
      return [];
    }
  }
}

export const api = new StreamyAPI();
export default api;
