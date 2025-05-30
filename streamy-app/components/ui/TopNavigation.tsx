import React from "react";
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  Dimensions,
  Platform,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";

const { width: screenWidth } = Dimensions.get("window");

interface TopNavigationProps {
  onSearchPress?: () => void;
  onProfilePress?: () => void;
}

export const TopNavigation: React.FC<TopNavigationProps> = ({
  onSearchPress,
  onProfilePress,
}) => {
  return (
    <View style={styles.container}>
      <LinearGradient
        colors={[
          "rgba(0,0,0,0.95)",
          "rgba(0,0,0,0.8)",
          "rgba(0,0,0,0.6)",
          "rgba(0,0,0,0.3)",
          "transparent",
        ]}
        locations={[0, 0.3, 0.6, 0.8, 1]}
        style={styles.gradient}
      >
        <View style={styles.content}>
          {/* Logo/Brand */}
          <View style={styles.brandContainer}>
            <View style={styles.logoContainer}>
              <LinearGradient
                colors={["#E50914", "#B20710"]}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={styles.logoGradient}
              >
                <Text style={styles.logoText}>S</Text>
              </LinearGradient>
            </View>
            <Text style={styles.brandText}>Streamy</Text>
          </View>

          {/* Navigation Items */}
          <View style={styles.navContainer}>
            <Pressable
              style={styles.navButton}
              tvParallaxProperties={{
                enabled: true,
                magnification: 1.05,
                pressMagnification: 1.02,
              }}
            >
              <LinearGradient
                colors={["rgba(255,255,255,0.15)", "rgba(255,255,255,0.05)"]}
                style={styles.navGradient}
              >
                <Text style={[styles.navItem, styles.activeNavItem]}>
                  For you
                </Text>
              </LinearGradient>
            </Pressable>

            <Pressable
              style={styles.navItemButton}
              tvParallaxProperties={{
                enabled: true,
                magnification: 1.05,
                pressMagnification: 1.02,
              }}
            >
              <Text style={styles.navItem}>Movies</Text>
            </Pressable>

            <Pressable
              style={styles.navItemButton}
              tvParallaxProperties={{
                enabled: true,
                magnification: 1.05,
                pressMagnification: 1.02,
              }}
            >
              <Text style={styles.navItem}>Shows</Text>
            </Pressable>

            <Pressable
              style={styles.navItemButton}
              tvParallaxProperties={{
                enabled: true,
                magnification: 1.05,
                pressMagnification: 1.02,
              }}
            >
              <Text style={styles.navItem}>Library</Text>
            </Pressable>
          </View>

          {/* Right Side Actions */}
          <View style={styles.actionsContainer}>
            {/* Search Button */}
            <Pressable
              style={styles.searchButton}
              onPress={onSearchPress}
              tvParallaxProperties={{
                enabled: true,
                magnification: 1.1,
                pressMagnification: 1.05,
              }}
            >
              <LinearGradient
                colors={["rgba(255,255,255,0.25)", "rgba(255,255,255,0.15)"]}
                style={styles.searchGradient}
              >
                <Ionicons name="search" size={18} color="#FFFFFF" />
              </LinearGradient>
            </Pressable>

            {/* Profile Button */}
            <Pressable
              style={styles.profileButton}
              onPress={onProfilePress}
              tvParallaxProperties={{
                enabled: true,
                magnification: 1.1,
                pressMagnification: 1.05,
              }}
            >
              <LinearGradient
                colors={["#4CAF50", "#45A049"]}
                style={styles.profileGradient}
              >
                <Text style={styles.profileInitial}>V</Text>
              </LinearGradient>
            </Pressable>
          </View>
        </View>
      </LinearGradient>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    zIndex: 100,
    height: 90,
    paddingTop: Platform.OS === "ios" ? 40 : 20,
  },
  gradient: {
    flex: 1,
  },
  content: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 48,
    paddingVertical: 8,
    height: "100%",
  },
  brandContainer: {
    flexDirection: "row",
    alignItems: "center",
    flex: 0,
  },
  logoContainer: {
    marginRight: 12,
    borderRadius: 8,
    overflow: "hidden",
    shadowColor: "#E50914",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 6,
  },
  logoGradient: {
    width: 32,
    height: 32,
    borderRadius: 8,
    justifyContent: "center",
    alignItems: "center",
  },
  logoText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontFamily: "Urbanist_800ExtraBold",
  },
  brandText: {
    color: "#FFFFFF",
    fontSize: 20,
    fontFamily: "Urbanist_700Bold",
    letterSpacing: -0.5,
  },
  navContainer: {
    flexDirection: "row",
    alignItems: "center",
    flex: 1,
    justifyContent: "center",
    gap: 24,
    paddingHorizontal: 20,
  },
  navButton: {
    borderRadius: 16,
    overflow: "hidden",
    minWidth: 80,
  },
  navGradient: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.25)",
    alignItems: "center",
  },
  navItemButton: {
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    minWidth: 60,
    alignItems: "center",
  },
  navItem: {
    color: "rgba(255,255,255,0.8)",
    fontSize: 14,
    fontFamily: "Urbanist_500Medium",
    letterSpacing: -0.2,
    textAlign: "center",
  },
  activeNavItem: {
    color: "#FFFFFF",
    fontFamily: "Urbanist_600SemiBold",
  },
  actionsContainer: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    flex: 0,
  },
  searchButton: {
    borderRadius: 18,
    overflow: "hidden",
  },
  searchGradient: {
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.3)",
  },
  profileButton: {
    borderRadius: 16,
    overflow: "hidden",
  },
  profileGradient: {
    width: 32,
    height: 32,
    borderRadius: 16,
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.2)",
  },
  profileInitial: {
    color: "#FFFFFF",
    fontSize: 12,
    fontFamily: "Urbanist_600SemiBold",
  },
});

export default TopNavigation;
