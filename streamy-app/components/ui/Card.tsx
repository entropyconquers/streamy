import React, { useState } from "react";
import {
  View,
  Text,
  Image,
  StyleSheet,
  Pressable,
  Dimensions,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { BlurView } from "expo-blur";
import { SearchResult } from "../../services/api";

const { width: screenWidth } = Dimensions.get("window");

interface CardProps {
  item: SearchResult;
  onPress?: () => void;
  onFocus?: () => void;
  onBlur?: () => void;
  width?: number;
  height?: number;
  showTitle?: boolean;
  showRating?: boolean;
}

export const Card: React.FC<CardProps> = ({
  item,
  onPress,
  onFocus,
  onBlur,
  width = 320,
  height = 180,
  showTitle = true,
  showRating = true,
}) => {
  const [focused, setFocused] = useState(false);
  const title = item.title || item.name || "Unknown Title";
  const year = item.release_date || item.first_air_date;
  const yearString = year ? new Date(year).getFullYear().toString() : "";

  const handleFocus = () => {
    setFocused(true);
    onFocus?.();
  };

  const handleBlur = () => {
    setFocused(false);
    onBlur?.();
  };

  const voteAverage = item.vote_average || 0;
  const ratingColor =
    voteAverage >= 7
      ? "#4CAF50" // Green for good ratings
      : voteAverage >= 5
      ? "#FFC107" // Yellow for medium ratings
      : "#F44336"; // Red for poor ratings

  return (
    <Pressable
      style={[
        styles.container,
        { width, height },
        focused && styles.focusedContainer,
      ]}
      onPress={onPress}
      onFocus={handleFocus}
      onBlur={handleBlur}
      tvParallaxProperties={{
        enabled: true,
        magnification: 1.1,
        pressMagnification: 1.05,
      }}
    >
      <View style={[styles.cardWrapper, focused && styles.focusedCard]}>
        {/* Background Image - Using backdrop for landscape cards */}
        <Image
          source={{ uri: item.backdrop_path || item.poster_path }}
          style={styles.backgroundImage}
          resizeMode="cover"
        />

        {/* Premium Gradient Overlay */}
        <LinearGradient
          colors={[
            "rgba(0,0,0,0.1)",
            "rgba(0,0,0,0.05)",
            "rgba(0,0,0,0.1)",
            "rgba(0,0,0,0.7)",
          ]}
          locations={[0, 0.3, 0.7, 1]}
          style={styles.overlay}
        />

        {/* Rating Pill */}
        {showRating && voteAverage > 0 && (
          <View
            style={[
              styles.ratingContainer,
              { backgroundColor: `${ratingColor}40` },
            ]}
          >
            <Text style={styles.ratingText}>{voteAverage.toFixed(1)}</Text>
          </View>
        )}

        {/* Media Type Badge */}
        <View style={styles.typeContainer}>
          <LinearGradient
            colors={["rgba(255,255,255,0.2)", "rgba(255,255,255,0.1)"]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={styles.typeGradient}
          >
            <Text style={styles.typeText}>
              {item.media_type === "movie" ? "MOVIE" : "TV"}
            </Text>
          </LinearGradient>
        </View>

        {/* Content Area */}
        {showTitle && (
          <View style={styles.contentContainer}>
            <BlurView intensity={25} style={styles.contentBlur}>
              <Text style={styles.title} numberOfLines={1}>
                {title}
              </Text>
              {yearString && <Text style={styles.year}>{yearString}</Text>}
            </BlurView>
          </View>
        )}

        {/* Focus Effects */}
        {focused && (
          <>
            <LinearGradient
              colors={["rgba(255,255,255,0.3)", "rgba(255,255,255,0)"]}
              start={{ x: 0, y: 0 }}
              end={{ x: 0, y: 1 }}
              style={styles.topHighlight}
            />
            <View style={styles.focusRing} />
          </>
        )}
      </View>
    </Pressable>
  );
};

const styles = StyleSheet.create({
  container: {
    marginHorizontal: 6,
    marginVertical: 8,
  },
  focusedContainer: {
    transform: [{ scale: 1.05 }],
    zIndex: 10,
  },
  cardWrapper: {
    flex: 1,
    borderRadius: 12,
    overflow: "hidden",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.08)",
    backgroundColor: "#1A1A1A",
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 8,
    },
    shadowOpacity: 0.6,
    shadowRadius: 16,
    elevation: 12,
  },
  focusedCard: {
    shadowColor: "#FFFFFF",
    shadowOpacity: 0.2,
    shadowRadius: 20,
    elevation: 15,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.3)",
  },
  backgroundImage: {
    width: "100%",
    height: "100%",
    position: "absolute",
  },
  overlay: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
  ratingContainer: {
    position: "absolute",
    top: 10,
    right: 10,
    minWidth: 36,
    height: 24,
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 8,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.3)",
  },
  ratingText: {
    color: "#FFFFFF",
    fontSize: 12,
    fontFamily: "Urbanist_700Bold",
    textAlign: "center",
    textShadowColor: "rgba(0, 0, 0, 0.5)",
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 2,
  },
  typeContainer: {
    position: "absolute",
    top: 10,
    left: 10,
    borderRadius: 8,
    overflow: "hidden",
  },
  typeGradient: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
    borderWidth: 0.5,
    borderColor: "rgba(255,255,255,0.3)",
  },
  typeText: {
    color: "#FFFFFF",
    fontSize: 10,
    fontFamily: "Urbanist_800ExtraBold",
    letterSpacing: 0.5,
    textShadowColor: "rgba(0, 0, 0, 0.5)",
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 2,
  },
  contentContainer: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    overflow: "hidden",
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
  },
  contentBlur: {
    padding: 12,
    paddingTop: 16,
    backgroundColor: "rgba(0,0,0,0.3)",
  },
  title: {
    color: "#FFFFFF",
    fontSize: 15,
    fontFamily: "Urbanist_600SemiBold",
    marginBottom: 2,
    letterSpacing: -0.2,
    textShadowColor: "rgba(0, 0, 0, 0.7)",
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 2,
  },
  year: {
    color: "rgba(255,255,255,0.8)",
    fontSize: 12,
    fontFamily: "Urbanist_400Regular",
    letterSpacing: -0.1,
  },
  topHighlight: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    height: 2,
  },
  focusRing: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: "rgba(255,255,255,0.7)",
    backgroundColor: "transparent",
  },
});

export default Card;
