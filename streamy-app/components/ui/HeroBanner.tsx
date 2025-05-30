import React from "react";
import {
  View,
  Text,
  Image,
  StyleSheet,
  Pressable,
  Dimensions,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
// import { View } from "expo-blur";
import { Ionicons } from "@expo/vector-icons";
import { SearchResult } from "../../services/api";

const { width: screenWidth, height: screenHeight } = Dimensions.get("window");

interface HeroBannerProps {
  item: SearchResult;
  onPress?: () => void;
  onPlayPress?: () => void;
  onInfoPress?: () => void;
}

export const HeroBanner: React.FC<HeroBannerProps> = ({
  item,
  onPress,
  onPlayPress,
  onInfoPress,
}) => {
  const title = item.title || item.name || "Unknown Title";
  const year = item.release_date || item.first_air_date;
  const yearString = year ? new Date(year).getFullYear().toString() : "";

  return (
    <Pressable style={styles.container} onPress={onPress}>
      {/* Background Image with Vibrant Effects */}
      <Image
        source={{ uri: item.backdrop_path }}
        style={styles.backgroundImage}
        resizeMode="cover"
      />

      {/* Clean Professional Gradients */}
      <LinearGradient
        colors={[
          "rgba(0,0,0,0.1)",
          "rgba(0,0,0,0.3)",
          "rgba(0,0,0,0.6)",
          "rgba(0,0,0,0.8)",
        ]}
        locations={[0, 0.3, 0.7, 1]}
        style={styles.mainGradient}
      />

      {/* Bottom Gradient to make it fade in with the next section */}
      <LinearGradient
        colors={["rgba(0,0,0,1)", "rgba(0,0,0,0.1)", "transparent"]}
        start={{ x: 0, y: 1 }}
        end={{ x: 0, y: 0 }}
        style={styles.bottomGradient}
      />

      {/* Clean Side Gradient */}
      <LinearGradient
        colors={["rgba(0,0,0,0.9)", "rgba(0,0,0,0.4)", "transparent"]}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
        style={styles.sideGradient}
      />

      {/* Content Container */}
      <View style={styles.contentContainer}>
        {/* Featured Badge with Clean Blur */}
        <View style={styles.badgeContainer}>
          <View>
            <LinearGradient
              colors={["rgba(255,215,0,1)", "rgba(255,193,7,0.9)"]}
              style={styles.featuredGradient}
            >
              <Ionicons name="star" size={14} color="#000000" />
              <Text style={styles.featuredText}>FEATURED</Text>
            </LinearGradient>
          </View>
        </View>

        {/* Title with Better Contrast */}
        <Text style={styles.title}>{title}</Text>

        {/* Metadata with Vibrant Effects */}
        <View style={styles.metaContainer}>
          <View style={styles.metaItem}>
            <Text style={styles.year}>{yearString}</Text>
          </View>

          <View style={styles.separator} />

          <View style={styles.metaItem}>
            <View style={styles.typeBlur}>
              <LinearGradient
                colors={
                  item.media_type === "movie"
                    ? ["rgba(255,87,34,1)", "rgba(255,87,34,0.8)"]
                    : ["rgba(76,175,80,1)", "rgba(76,175,80,0.8)"]
                }
                style={styles.typeBadge}
              >
                <Text style={styles.typeText}>
                  {item.media_type === "movie" ? "MOVIE" : "SERIES"}
                </Text>
              </LinearGradient>
            </View>
          </View>

          <View style={styles.separator} />

          <View style={styles.ratingContainer}>
            <View style={styles.ratingBlur}>
              <Ionicons name="star" size={14} color="#FFD700" />
              <Text style={styles.rating}>{item.vote_average.toFixed(1)}</Text>
            </View>
          </View>
        </View>

        {/* Description with Better Readability */}
        <Text style={styles.description} numberOfLines={3}>
          {item.overview}
        </Text>

        {/* Action Buttons with Vibrant Effects */}
        <View style={styles.buttonContainer}>
          <Pressable style={styles.playButton} onPress={onPlayPress}>
            <View style={styles.playBlur}>
              <LinearGradient
                colors={["rgba(255,255,255,1)", "rgba(255,255,255,0.95)"]}
                style={styles.playGradient}
              >
                <Ionicons name="play" size={18} color="#000000" />
                <Text style={styles.playText}>Play</Text>
              </LinearGradient>
            </View>
          </Pressable>

          <Pressable style={styles.infoButton} onPress={onInfoPress}>
            <View style={styles.infoBlur}>
              <LinearGradient
                colors={["rgba(255,255,255,0.3)", "rgba(255,255,255,0.2)"]}
                style={styles.infoGradient}
              >
                <Ionicons
                  name="information-circle-outline"
                  size={18}
                  color="#FFFFFF"
                />
                <Text style={styles.infoText}>More Info</Text>
              </LinearGradient>
            </View>
          </Pressable>
        </View>
      </View>

      {/* Crisp Poster - NO BLUR */}
      <View style={styles.posterContainer}>
        <View style={styles.posterWrapper}>
          <Image
            source={{ uri: item.poster_path }}
            style={styles.posterImage}
            resizeMode="cover"
          />
          {/* Subtle gradient only */}
          <LinearGradient
            colors={["transparent", "rgba(0,0,0,0.2)"]}
            style={styles.posterGradient}
          />
          {/* Colorful glow effect */}
          <View style={styles.posterGlow} />
        </View>
      </View>
    </Pressable>
  );
};

const styles = StyleSheet.create({
  container: {
    width: screenWidth,
    height: screenHeight * 0.9,
    position: "relative",
    marginTop: 0,
  },
  backgroundImage: {
    width: "100%",
    height: "150%",
    resizeMode: "cover",
    position: "absolute",
    top: 0,
  },
  mainGradient: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
  sideGradient: {
    position: "absolute",
    top: 0,
    left: 0,
    bottom: 0,
    width: "65%",
  },
  contentContainer: {
    position: "absolute",
    top: 140,
    left: 48,
    right: screenWidth * 0.4,
    zIndex: 2,
  },
  badgeContainer: {
    marginBottom: 16,
    borderRadius: 20,
    overflow: "hidden",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.3)",
    alignSelf: "flex-start",
  },

  featuredGradient: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    paddingVertical: 6,
    gap: 4,
  },
  featuredText: {
    color: "#000000",
    fontSize: 11,

    fontFamily: "Urbanist_800ExtraBold",
    letterSpacing: 1.1,
  },
  title: {
    color: "#FFFFFF",
    fontSize: 48,
    fontWeight: undefined,

    fontFamily: "Urbanist_800ExtraBold",
    marginBottom: 16,
    lineHeight: 52,
    letterSpacing: -1,
  },
  metaContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 20,
    gap: 12,
  },
  metaItem: {
    flexDirection: "row",
    alignItems: "center",
  },
  year: {
    color: "#FFFFFF",
    fontSize: 16,

    fontFamily: "Urbanist_500Medium",
    letterSpacing: -0.2,
  },
  separator: {
    width: 3,
    height: 3,
    borderRadius: 1.5,
    backgroundColor: "rgba(255,255,255,0.7)",
  },
  typeBlur: {
    borderRadius: 12,
    overflow: "hidden",
  },
  typeBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  typeText: {
    color: "#FFFFFF",
    fontSize: 11,

    fontFamily: "Urbanist_700Bold",
    letterSpacing: 0.5,
  },
  ratingContainer: {
    borderRadius: 12,
    overflow: "hidden",
  },
  ratingBlur: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.3)",
  },
  rating: {
    color: "#FFFFFF",
    fontSize: 14,

    fontFamily: "Urbanist_600SemiBold",
  },
  description: {
    color: "#FFFFFF",
    fontSize: 14,
    fontFamily: "Urbanist_400Regular",
    lineHeight: 22,
    marginBottom: 24,
  },
  buttonContainer: {
    flexDirection: "row",
    gap: 16,
  },
  playButton: {
    borderRadius: 24,
    overflow: "hidden",
  },
  playBlur: {
    borderRadius: 24,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.4)",
  },
  playGradient: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 24,
    paddingVertical: 12,
    gap: 8,
  },
  playText: {
    color: "#000000",
    fontSize: 16,

    fontFamily: "Urbanist_700Bold",
  },
  infoButton: {
    borderRadius: 24,
    overflow: "hidden",
  },
  infoBlur: {
    borderRadius: 24,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.4)",
  },
  infoGradient: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 24,
    paddingVertical: 12,
    gap: 8,
  },
  infoText: {
    color: "#FFFFFF",
    fontSize: 16,

    fontFamily: "Urbanist_600SemiBold",
  },
  posterContainer: {
    position: "absolute",
    right: 48,
    bottom: 80,
    zIndex: 1,
  },
  posterWrapper: {
    width: 200,
    height: 300,
    borderRadius: 16,
    overflow: "hidden",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.6,
    shadowRadius: 20,
    elevation: 20,
  },
  posterImage: {
    width: "100%",
    height: "100%",
  },
  posterGradient: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    height: "30%",
  },
  posterGlow: {
    position: "absolute",
    top: -1,
    left: -1,
    right: -1,
    bottom: -1,
    borderRadius: 17,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.1)",
  },
  bottomGradient: {
    position: "absolute",
    bottom: -10,
    left: 0,
    right: 0,
    height: 150,
    zIndex: 1,
  },
});

export default HeroBanner;
