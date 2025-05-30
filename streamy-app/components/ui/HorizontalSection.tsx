import React, { useRef, forwardRef } from "react";
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  Pressable,
  Dimensions,
  TVFocusGuideView,
  Animated,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { BlurView } from "expo-blur";
import { Ionicons } from "@expo/vector-icons";
import { SearchResult } from "../../services/api";
import Card from "./Card";

const { width: screenWidth } = Dimensions.get("window");

interface HorizontalSectionProps {
  title: string;
  data: SearchResult[];
  onItemPress?: (item: SearchResult) => void;
  onSeeAll?: () => void;
  cardWidth?: number;
  cardHeight?: number;
  showSeeAll?: boolean;
  sectionKey: string;
}

export const HorizontalSection = forwardRef<View, HorizontalSectionProps>(
  (props, ref) => {
    const {
      title,
      data,
      onItemPress,
      onSeeAll,
      cardWidth = 320,
      cardHeight = 180,
      showSeeAll = true,
      sectionKey,
    } = props;

    const flatListRef = useRef<FlatList>(null);

    const renderItem = ({
      item,
      index,
    }: {
      item: SearchResult;
      index: number;
    }) => (
      <Card
        item={item}
        onPress={() => onItemPress?.(item)}
        //onFocus={() => handleCardFocus(index)}
        width={cardWidth}
        height={cardHeight}
      />
    );

    return (
      <View ref={ref} style={styles.container}>
        {/* Section Header with Modern Design */}
        <View style={styles.header}>
          <LinearGradient
            colors={["rgba(0,0,0,0)", "rgba(0,0,0,0)", "rgba(0,0,0,0)"]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.headerGradient}
          >
            <Text style={styles.title}>{title}</Text>
            {showSeeAll && data.length > 0 && (
              <Pressable
                onPress={onSeeAll}
                style={styles.seeAllButton}
                tvParallaxProperties={{
                  enabled: true,
                  magnification: 1.1,
                  pressMagnification: 1.05,
                }}
              >
                <BlurView style={styles.seeAllBlur}>
                  <Text style={styles.seeAllText}>See all</Text>
                  <Ionicons
                    name="chevron-forward"
                    size={16}
                    color="rgba(255,255,255,0.9)"
                  />
                </BlurView>
              </Pressable>
            )}
          </LinearGradient>
        </View>

        {/* Content List */}
        {data.length > 0 ? (
          <TVFocusGuideView autoFocus>
            <FlatList
              ref={flatListRef}
              data={data}
              renderItem={renderItem}
              keyExtractor={(item) => `${item.media_type}-${item.id}`}
              horizontal
              showsHorizontalScrollIndicator={false}
              contentContainerStyle={styles.listContainer}
              decelerationRate="fast"
              snapToInterval={cardWidth + 12}
              snapToAlignment="start"
            />
          </TVFocusGuideView>
        ) : (
          <View style={styles.emptyContainer}>
            <BlurView style={styles.emptyBlur}>
              <LinearGradient
                colors={["rgba(255,255,255,0.05)", "rgba(255,255,255,0.02)"]}
                style={styles.emptyGradient}
              >
                <Ionicons
                  name="film-outline"
                  size={32}
                  color="rgba(255,255,255,0.3)"
                />
                <Text style={styles.emptyText}>No content available</Text>
              </LinearGradient>
            </BlurView>
          </View>
        )}

        {/* Side Gradients for Scrolling Indication */}
        <LinearGradient
          colors={["rgba(0,0,0,0.8)", "rgba(0,0,0,0)"]}
          start={{ x: 0, y: 0 }}
          end={{ x: 0.1, y: 0 }}
          style={styles.leftGradient}
          pointerEvents="none"
        />
        <LinearGradient
          colors={["rgba(0,0,0,0)", "rgba(0,0,0,0.8)"]}
          start={{ x: 0.9, y: 0 }}
          end={{ x: 1, y: 0 }}
          style={styles.rightGradient}
          pointerEvents="none"
        />
      </View>
    );
  }
);

const styles = StyleSheet.create({
  container: {
    marginBottom: 40,
    position: "relative",
  },
  header: {
    marginBottom: 16,
    position: "relative",
  },
  headerGradient: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 48,
    paddingVertical: 8,
  },
  title: {
    color: "#FFFFFF",
    fontSize: 26,
    fontFamily: "Urbanist_700Bold",
    letterSpacing: -0.7,
    textShadowColor: "rgba(0, 0, 0, 0.7)",
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 3,
  },
  seeAllButton: {
    borderRadius: 20,
    overflow: "hidden",
  },
  seeAllBlur: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 16,
    paddingVertical: 8,
    gap: 4,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.15)",
    backgroundColor: "rgba(255,255,255,0.05)",
  },
  seeAllText: {
    color: "rgba(255,255,255,0.9)",
    fontSize: 14,
    fontFamily: "Urbanist_600SemiBold",
    letterSpacing: -0.2,
  },
  listContainer: {
    paddingHorizontal: 42,
    paddingBottom: 50,
    paddingTop: 20,
    gap: 12,
    overflow: "visible",
  },
  emptyContainer: {
    height: 180,
    marginHorizontal: 48,
    borderRadius: 16,
    overflow: "hidden",
  },
  emptyBlur: {
    flex: 1,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.05)",
    backgroundColor: "rgba(0,0,0,0.3)",
  },
  emptyGradient: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    gap: 12,
    borderRadius: 16,
  },
  emptyText: {
    color: "rgba(255,255,255,0.4)",
    fontSize: 14,
    fontFamily: "Urbanist_400Regular",
    letterSpacing: -0.1,
  },
  leftGradient: {
    position: "absolute",
    left: 0,
    top: 0,
    bottom: 0,
    width: 60,
    pointerEvents: "none",
    zIndex: 1,
  },
  rightGradient: {
    position: "absolute",
    right: 0,
    top: 0,
    bottom: 0,
    width: 60,
    pointerEvents: "none",
    zIndex: 1,
  },
});

export default HorizontalSection;
