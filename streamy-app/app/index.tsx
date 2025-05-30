import React, { useState, useEffect, useRef } from "react";
import {
  View,
  FlatList,
  StyleSheet,
  StatusBar,
  ActivityIndicator,
  Text,
  Alert,
  Dimensions,
  Animated as RNAnimated,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withRepeat,
  withSequence,
  interpolate,
  runOnJS,
} from "react-native-reanimated";

import TopNavigation from "../components/ui/TopNavigation";
import HeroBanner from "../components/ui/HeroBanner";
import HorizontalSection from "../components/ui/HorizontalSection";
import { SearchResult } from "../services/api";
import api from "../services/api";

const { height: screenHeight, width: screenWidth } = Dimensions.get("window");

interface SectionData {
  key: string;
  title: string;
  data: SearchResult[];
}

export default function HomeScreen() {
  const [featuredContent, setFeaturedContent] = useState<SearchResult[]>([]);
  const [currentHeroIndex, setCurrentHeroIndex] = useState(0);
  const [sections, setSections] = useState<SectionData[]>([]);
  const [loading, setLoading] = useState(true);

  const flatListRef = useRef<FlatList>(null);
  const scrollY = useRef(new RNAnimated.Value(0)).current;

  // Hero carousel animation values
  const heroTranslateX = useSharedValue(0);
  const heroOpacity = useSharedValue(1);

  useEffect(() => {
    loadContent();
  }, []);

  // Auto-scroll hero carousel
  useEffect(() => {
    if (featuredContent.length > 1) {
      const interval = setInterval(() => {
        setCurrentHeroIndex((prevIndex) => {
          const nextIndex = (prevIndex + 1) % featuredContent.length;

          // Animate with combined fade and slide transition
          heroOpacity.value = withTiming(0, { duration: 300 }, () => {
            runOnJS(setCurrentHeroIndex)(nextIndex);
            heroTranslateX.value = 50;
            heroOpacity.value = withTiming(1, { duration: 400 });
            heroTranslateX.value = withTiming(0, { duration: 400 });
          });

          return nextIndex;
        });
      }, 6000); // Change every 6 seconds

      return () => clearInterval(interval);
    }
  }, [featuredContent.length, heroTranslateX, heroOpacity]);

  const loadContent = async () => {
    try {
      setLoading(true);

      // Load featured content - get multiple items for carousel
      const featured = await api.getFeaturedContent();
      setFeaturedContent(featured);

      // Load all sections with diverse content - taking first result from different searches
      const [
        inceptionResponse,
        darkKnightResponse,
        interstellarResponse,
        fightClubResponse,
        matrixResponse,
        breakingBadResponse,
        gameOfThronesResponse,
        strangerthingsResponse,
        theOfficeResponse,
        friendsResponse,
        godfatherResponse,
        pulpFictionResponse,
        shawshankResponse,
        wireResponse,
        sopranosResponse,
      ] = await Promise.all([
        api.searchMovies("inception"),
        api.searchMovies("the dark knight"),
        api.searchMovies("interstellar"),
        api.searchMovies("fight club"),
        api.searchMovies("the matrix"),
        api.searchTvShows("breaking bad"),
        api.searchTvShows("game of thrones"),
        api.searchTvShows("stranger things"),
        api.searchTvShows("the office"),
        api.searchTvShows("friends"),
        api.searchMovies("the godfather"),
        api.searchMovies("pulp fiction"),
        api.searchMovies("the shawshank redemption"),
        api.searchTvShows("the wire"),
        api.searchTvShows("the sopranos"),
      ]);

      // Create diverse sections by taking first result from each search
      const sectionsData: SectionData[] = [
        {
          key: "top-picks",
          title: "Top picks for you",
          data: [
            inceptionResponse.results[0],
            darkKnightResponse.results[0],
            interstellarResponse.results[0],
            fightClubResponse.results[0],
            matrixResponse.results[0],
            godfatherResponse.results[0],
          ].filter(Boolean), // Remove any undefined results
        },
        {
          key: "continue-watching",
          title: "Continue watching for you",
          data: [
            breakingBadResponse.results[0],
            gameOfThronesResponse.results[0],
            strangerthingsResponse.results[0],
            wireResponse.results[0],
          ].filter(Boolean),
        },
        {
          key: "action-movies",
          title: "Action movies",
          data: [
            darkKnightResponse.results[0],
            matrixResponse.results[0],
            inceptionResponse.results[0],
            fightClubResponse.results[0],
          ].filter(Boolean),
        },
        {
          key: "drama-content",
          title: "Award-winning dramas",
          data: [
            godfatherResponse.results[0],
            shawshankResponse.results[0],
            pulpFictionResponse.results[0],
            sopranosResponse.results[0],
          ].filter(Boolean),
        },
        {
          key: "comedy-shows",
          title: "Comedy shows",
          data: [
            theOfficeResponse.results[0],
            friendsResponse.results[0],
          ].filter(Boolean),
        },
      ];

      setSections(sectionsData);
    } catch (error) {
      console.error("Failed to load content:", error);
      Alert.alert(
        "Connection Error",
        "Unable to load content. Please make sure the API server is running.",
        [{ text: "Retry", onPress: loadContent }, { text: "Cancel" }]
      );
    } finally {
      setLoading(false);
    }
  };

  const handleItemPress = (item: SearchResult) => {
    // TODO: Navigate to detail screen
    console.log("Item pressed:", item.title || item.name);
  };

  const handlePlayPress = () => {
    // TODO: Implement play functionality
    console.log("Play pressed");
  };

  const handleInfoPress = () => {
    // TODO: Navigate to detail screen
    console.log("Info pressed");
  };

  const handleSeeAll = (category: string) => {
    // TODO: Navigate to category screen
    console.log("See all pressed for:", category);
  };

  const handleSearchPress = () => {
    // TODO: Navigate to search screen
    console.log("Search pressed");
  };

  const handleProfilePress = () => {
    // TODO: Navigate to profile screen
    console.log("Profile pressed");
  };

  const renderSection = ({ item }: { item: SectionData }) => (
    <HorizontalSection
      title={item.title}
      data={item.data}
      onItemPress={handleItemPress}
      onSeeAll={() => handleSeeAll(item.key)}
      sectionKey={item.key}
    />
  );

  const ListHeaderComponent = () => {
    const heroAnimatedStyle = useAnimatedStyle(() => {
      return {
        opacity: heroOpacity.value,
        transform: [
          {
            translateX: heroTranslateX.value,
          },
        ],
      };
    });

    return (
      <>
        <TopNavigation
          onSearchPress={handleSearchPress}
          onProfilePress={handleProfilePress}
        />
        {/* Animated Hero Banner with Carousel */}
        {featuredContent.length > 0 && (
          <View style={styles.heroContainer}>
            <Animated.View style={heroAnimatedStyle}>
              <HeroBanner
                item={featuredContent[currentHeroIndex]}
                onPress={() =>
                  handleItemPress(featuredContent[currentHeroIndex])
                }
                onPlayPress={handlePlayPress}
                onInfoPress={handleInfoPress}
              />
            </Animated.View>

            {/* Carousel Indicators */}
            {featuredContent.length > 1 && (
              <View style={styles.indicatorContainer}>
                {featuredContent.map((_, index) => (
                  <View
                    key={index}
                    style={[
                      styles.indicator,
                      index === currentHeroIndex && styles.activeIndicator,
                    ]}
                  />
                ))}
              </View>
            )}
          </View>
        )}
        <View style={styles.sectionsSpacing} />
      </>
    );
  };

  const ListFooterComponent = () => <View style={styles.bottomSpacing} />;

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <LinearGradient
          colors={["#000000", "#111111", "#000000"]}
          style={styles.loadingGradient}
        >
          <View style={styles.loadingContent}>
            <LinearGradient
              colors={["#E50914", "#B20710"]}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
              style={styles.loadingIcon}
            >
              <Text style={styles.loadingIconText}>S</Text>
            </LinearGradient>
            <ActivityIndicator
              size="large"
              color="#FFFFFF"
              style={styles.spinner}
            />
            <Text style={styles.loadingText}>Loading Streamy</Text>
            <Text style={styles.loadingSubtext}>
              Preparing your entertainment
            </Text>
          </View>
        </LinearGradient>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <StatusBar
        barStyle="light-content"
        backgroundColor="transparent"
        translucent
      />

      {/* Main Content */}
      <RNAnimated.FlatList
        ref={flatListRef}
        data={sections}
        renderItem={renderSection}
        keyExtractor={(item) => item.key}
        showsVerticalScrollIndicator={false}
        bounces={false}
        keyboardShouldPersistTaps="handled"
        removeClippedSubviews={false}
        ListHeaderComponent={ListHeaderComponent}
        ListFooterComponent={ListFooterComponent}
        contentContainerStyle={styles.flatListContent}
        onScroll={RNAnimated.event(
          [{ nativeEvent: { contentOffset: { y: scrollY } } }],
          { useNativeDriver: false }
        )}
        scrollEventThrottle={16}
        scrollEnabled={true}
        nestedScrollEnabled={false}
        automaticallyAdjustContentInsets={false}
        maintainVisibleContentPosition={{
          minIndexForVisible: 0,
          autoscrollToTopThreshold: 10,
        }}
      />

      {/* Bottom Gradient */}
      <LinearGradient
        colors={["transparent", "rgba(0,0,0,0.8)", "#000000"]}
        style={styles.bottomGradient}
        pointerEvents="none"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#000000",
  },
  loadingContainer: {
    flex: 1,
  },
  loadingGradient: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  loadingContent: {
    alignItems: "center",
    gap: 20,
  },
  loadingIcon: {
    width: 64,
    height: 64,
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 8,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  loadingIconText: {
    color: "#FFFFFF",
    fontSize: 28,
    fontFamily: "Urbanist_800ExtraBold",
  },
  spinner: {
    transform: [{ scale: 1.2 }],
  },
  loadingText: {
    color: "#FFFFFF",
    fontSize: 22,
    fontFamily: "Urbanist_600SemiBold",
    letterSpacing: -0.3,
  },
  loadingSubtext: {
    color: "rgba(255,255,255,0.6)",
    fontSize: 14,
    fontFamily: "Urbanist_400Regular",
    letterSpacing: -0.1,
  },
  sectionsSpacing: {
    height: 48,
  },
  bottomSpacing: {
    height: 80,
  },
  bottomGradient: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    height: 120,
    pointerEvents: "none",
  },
  flatListContent: {
    paddingTop: 0,
  },
  heroContainer: {
    position: "relative",
    overflow: "hidden",
  },
  indicatorContainer: {
    position: "absolute",
    bottom: 20,
    left: 0,
    right: 0,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 10,
  },
  indicator: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: "rgba(255,255,255,0.4)",
    marginHorizontal: 4,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.2)",
  },
  activeIndicator: {
    backgroundColor: "#FFFFFF",
    borderColor: "#FFFFFF",
    transform: [{ scale: 1.2 }],
  },
});
