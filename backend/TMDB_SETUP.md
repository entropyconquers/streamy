# TMDB Setup Guide

## 🎬 Fixing TMDB Connection Errors

If you're seeing errors like:

```
TMDB movie search failed: ('Connection aborted.', ConnectionResetError(54, 'Connection reset by peer'))
```

This means your TMDB API is not properly configured. Here's how to fix it:

## 🚀 Quick Setup

### Option 1: Use the Setup Script (Recommended)

```bash
cd backend
python setup_tmdb.py
```

### Option 2: Manual Setup

1. Create a `.env` file in the `backend` directory
2. Add your TMDB API key:

```env
TMDB_API_KEY=your_actual_api_key_here
```

## 🔑 Getting Your TMDB API Key

1. **Go to TMDB**: Visit [https://www.themoviedb.org/](https://www.themoviedb.org/)
2. **Create Account**: Sign up for a free account
3. **Request API Key**:
   - Go to Settings → API
   - Click "Request an API Key"
   - Choose "Developer"
   - Fill out the form (you can use placeholder info for personal projects)
4. **Copy Your Key**: Copy the API key (v3 auth)

## 🔧 Complete .env File Template

```env
# TMDB API Configuration
TMDB_API_KEY=your_actual_api_key_here
TMDB_BASE_URL=https://api.themoviedb.org/3
TMDB_IMAGE_BASE_URL=https://image.tmdb.org/t/p/w500

# Torrent Site Configuration
TORRENT_SITE_DOMAIN=tpirbay.site

# API Configuration
API_PORT=8001
DEBUG=True
HOST=0.0.0.0
```

## ✅ Testing Your Setup

### 1. Test TMDB Connection

```bash
python setup_tmdb.py test
```

### 2. Check Health Endpoint

```bash
curl http://localhost:8001/health
```

### 3. Try a Search

```bash
curl http://localhost:8001/movies/inception
```

## 🔍 Troubleshooting

### Error: "TMDB service not available - API key not configured"

- **Solution**: Set up your TMDB API key using the steps above

### Error: "TMDB authentication failed - check your API key"

- **Solution**: Your API key is invalid. Double-check it on TMDB website

### Error: "TMDB connection error" or "Connection reset by peer"

- **Possible causes**:
  - Network connectivity issues
  - TMDB API is temporarily down
  - Rate limiting (the new client handles this automatically)
- **Solution**: The improved client now has retry logic and better error handling

### Error: "TMDB request timeout"

- **Solution**: The timeout has been increased to 15 seconds with retry logic

## 🆕 Improvements Made

The TMDB client has been significantly improved with:

1. **Better Error Handling**: Specific error messages for different failure types
2. **Retry Logic**: Automatic retries for network issues and rate limiting
3. **Connection Pooling**: More efficient HTTP connections
4. **Graceful Degradation**: API works without TMDB (returns helpful error messages)
5. **Rate Limit Handling**: Automatically waits and retries when rate limited

## 🎯 API Behavior

### With TMDB Configured ✅

- Full movie/TV metadata
- Poster and backdrop images
- Cast and crew information
- Detailed information for torrents

### Without TMDB Configured ⚠️

- Returns helpful error messages
- Suggests how to enable TMDB
- Torrent search still works (when implemented)

## 📞 Still Having Issues?

1. **Check the logs**: Look for specific error messages in the console
2. **Verify API key**: Make sure it's copied correctly (no extra spaces)
3. **Test connection**: Use `python setup_tmdb.py test`
4. **Check network**: Ensure you can reach `api.themoviedb.org`

## 🔄 Starting the API

After setting up TMDB:

```bash
cd backend
python app.py
```

You should see:

```
🚀 Starting Torrent Search API v4.0...
📁 Modular architecture enabled
🎭 TMDB metadata: ✅ Enabled
🔗 TMDB connection: ✅ Connected
🔍 Torrent site: tpirbay.site
🌐 Server: http://0.0.0.0:8001
```
