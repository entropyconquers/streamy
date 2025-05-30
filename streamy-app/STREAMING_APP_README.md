# 🎬 Streamy - TV Streaming App

A modern, sleek streaming app built with Expo and React Native for TV platforms, inspired by Google TV's design language.

## ✨ Features

### 🎨 Modern UI Design

- **Google TV Inspired**: Clean, modern interface with bold typography
- **Urbanist Font**: Beautiful Google font for consistent branding
- **Dark Theme**: Optimized for TV viewing with dark backgrounds
- **Gradients & Animations**: Smooth transitions and visual effects
- **TV-Optimized Layout**: Landscape-first design for television screens

### 🏠 Homepage Components

- **Hero Banner**: Featured content with backdrop images and action buttons
- **Horizontal Sections**: Scrollable rows of content (movies/TV shows)
- **Smart Cards**: Movie/TV show cards with ratings, posters, and metadata
- **Loading States**: Beautiful loading animations with gradients

### 📱 Navigation

- **Tab Navigation**: Home, Search, My List
- **TV-Optimized**: Top navigation for TV, bottom for mobile
- **Focus States**: Proper focus handling for TV remote navigation

### 🔌 API Integration

- **Type-Safe**: Full TypeScript integration with backend API
- **Real-Time Data**: Connects to Streamy backend for live content
- **Error Handling**: Graceful error states and user feedback
- **Smart Loading**: Efficient data fetching and caching

## 🏗️ Architecture

### Component Structure

```
components/
├── ui/
│   ├── Card.tsx              # Content cards with posters
│   ├── HeroBanner.tsx        # Featured content banner
│   └── HorizontalSection.tsx # Scrollable content rows
└── navigation/
    └── TabBarIcon.tsx        # Navigation icons
```

### Services

```
services/
└── api.ts                   # Backend API integration
```

### Screens

```
app/(tabs)/
├── index.tsx               # Homepage with content sections
├── explore.tsx             # Search functionality
└── tv_focus.tsx           # My List / Bookmarks
```

## 🎯 Design System

### Colors

- **Primary**: `#00D4FF` (Bright blue)
- **Background**: `#0A0A0A` (Deep black)
- **Cards**: `#1A1A1A` (Dark gray)
- **Text**: `#FFFFFF` (White)
- **Secondary Text**: `#CCCCCC` (Light gray)
- **Accent**: `#FFD700` (Gold for ratings)

### Typography

- **Font Family**: Urbanist (Google Font)
- **Weights**: 400 (Regular), 500 (Medium), 600 (SemiBold), 700 (Bold), 800 (ExtraBold)
- **Sizes**:
  - Hero Title: 48px
  - Section Title: 28px
  - Card Title: 18px
  - Body Text: 16px

### Layout

- **TV Screen**: Optimized for 1920x1080 landscape
- **Spacing**: Consistent 8px grid system
- **Borders**: 16px border radius for modern look
- **Shadows**: Subtle elevation for depth

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Expo CLI
- Backend API running on `localhost:8001`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm start

# For TV development
EXPO_TV=1 npm start
```

### Backend Connection

Make sure the Streamy backend API is running:

```bash
cd ../backend
python3 app.py
```

## 📺 TV Development

### Focus Management

- Automatic focus handling for TV remotes
- Visual focus indicators
- Smooth navigation between elements

### Platform Detection

- Automatic TV layout detection
- Responsive design for different screen sizes
- Platform-specific optimizations

### Performance

- Optimized for TV hardware
- Smooth scrolling and animations
- Efficient image loading and caching

## 🎬 Content Sections

### Hero Banner

- Featured content with full backdrop
- Play and Info buttons
- Metadata display (year, rating, type)
- Poster image overlay

### Content Rows

- **🔥 Trending Movies**: Popular movie content
- **📺 Popular TV Shows**: Trending television series
- **💥 Action Movies**: Action genre content
- **😂 Comedy Shows**: Comedy television content

### Smart Cards

- High-quality poster images
- Rating badges with star icons
- Year and media type indicators
- Hover/focus effects for interaction

## 🔧 Configuration

### API Endpoints

The app connects to these backend endpoints:

- `/search/{query}` - Multi search
- `/movies/{query}` - Movie search
- `/tv-shows/{query}` - TV show search
- `/details/movie/{id}` - Movie details
- `/details/tv/{id}` - TV show details

### Environment

- Development: `http://localhost:8001`
- Production: Configure in `services/api.ts`

## 🎨 Customization

### Themes

Modify colors in `app/_layout.tsx`:

```typescript
const StreamyDarkTheme = {
  colors: {
    primary: "#00D4FF",
    background: "#0A0A0A",
    // ... other colors
  },
};
```

### Fonts

Add new font weights in `app/_layout.tsx`:

```typescript
import {
  Urbanist_400Regular,
  Urbanist_500Medium,
  // ... add more weights
} from "@expo-google-fonts/urbanist";
```

### Content Sections

Add new sections in `app/(tabs)/index.tsx`:

```typescript
<HorizontalSection
  title="🎭 Drama Series"
  data={dramaShows}
  onItemPress={handleItemPress}
  onSeeAll={() => handleSeeAll("drama")}
/>
```

## 🚀 Deployment

### TV Platforms

- Android TV
- Apple TV
- Fire TV
- Web (TV browsers)

### Build Commands

```bash
# Android TV
npm run android

# iOS/Apple TV
npm run ios

# Web
npm run web

# Production build
npx expo build
```

## 🎯 Future Enhancements

### Planned Features

- [ ] Search functionality with voice input
- [ ] User profiles and watchlists
- [ ] Video player integration
- [ ] Offline content support
- [ ] Parental controls
- [ ] Content recommendations
- [ ] Social features (sharing, reviews)

### Technical Improvements

- [ ] Image caching optimization
- [ ] Background data sync
- [ ] Performance monitoring
- [ ] A/B testing framework
- [ ] Analytics integration

## 📱 Platform Support

### TV Platforms

- ✅ Android TV
- ✅ Apple TV
- ✅ Fire TV
- ✅ Web TV browsers

### Mobile (Secondary)

- ✅ iOS
- ✅ Android
- ✅ Web browsers

## 🎬 Screenshots

_Screenshots will be added once the app is running_

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on TV platform
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

---

**Built with ❤️ for the big screen experience**
