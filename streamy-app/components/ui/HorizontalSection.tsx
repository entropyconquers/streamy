import React, { useRef, forwardRef, useState } from "react";
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  Pressable,
  Dimensions,
  TVFocusGuideView,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { BlurView } from "expo-blur";
import { Ionicons } from "@expo/vector-icons";
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withDelay,
  Easing,
} from "react-native-reanimated";
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
  onSectionFocus?: (sectionKey: string) => void;
  isActive?: boolean;
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
      isActive,
    } = props;

    const flatListRef = useRef<FlatList>(null);
    const titleScale = useSharedValue(1);

    // Create data array with "See all" button as last item if needed
    const listData = React.useMemo(() => {
      const items = [...data];
      if (showSeeAll && data.length > 0) {
        items.push({ id: "see-all", type: "see-all" } as any);
      }
      return items;
    }, [data, showSeeAll]);

    // Animate title scale based on isActive prop
    React.useEffect(() => {
      titleScale.value = withDelay(
        50,
        withTiming(isActive ? 1.2 : 0.7, {
          duration: 300,
          easing: Easing.bezier(0.25, 0.1, 0.25, 1.0),
        })
      );
    }, [isActive, titleScale]);

    // Animated style for the title
    const animatedTitleStyle = useAnimatedStyle(() => {
      return {
        transform: [{ scale: titleScale.value }],
        transformOrigin: "left",
      };
    });

    const handleCardFocus = (index: number) => {
      if (flatListRef.current) {
        const itemWidthWithGap = cardWidth + 12; // 12 is the gap from listContainer styles
        const offset = index * itemWidthWithGap;
        flatListRef.current.scrollToOffset({ offset, animated: true });
      }
    };

    const renderItem = ({
      item,
      index,
    }: {
      item: SearchResult | { id: string; type: string };
      index: number;
    }) => {
      // Render "See all" button as last item
      if ("type" in item && item.type === "see-all") {
        return (
          <TVFocusGuideView
            autoFocus
            onFocus={handleSeeAllFocus}
            onBlur={handleSeeAllBlur}
          >
            <Pressable
              onPress={onSeeAll}
              style={[styles.seeAllCard, seeAllFocused && styles.seeAllFocused]}
              tvParallaxProperties={{
                enabled: true,
                magnification: 1.1,
                pressMagnification: 1.05,
              }}
            >
              <BlurView style={styles.seeAllCardBlur}>
                <LinearGradient
                  colors={
                    seeAllFocused
                      ? ["#FFFFFF", "#F8F9FA"]
                      : [
                          "rgba(255,255,255,0.15)",
                          "rgba(255,255,255,0.05)",
                          "rgba(0,0,0,0.1)",
                        ]
                  }
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 1 }}
                  style={styles.seeAllCardGradient}
                >
                  <View style={styles.seeAllIconContainer}>
                    <LinearGradient
                      colors={
                        seeAllFocused
                          ? ["#000000", "#333333"]
                          : ["rgba(255,255,255,0.2)", "rgba(255,255,255,0.1)"]
                      }
                      style={styles.seeAllIconGradient}
                    >
                      <Ionicons
                        name="chevron-forward"
                        size={24}
                        color={
                          seeAllFocused ? "#FFFFFF" : "rgba(255,255,255,0.9)"
                        }
                      />
                    </LinearGradient>
                  </View>
                  <Text
                    style={[
                      styles.seeAllCardText,
                      seeAllFocused && styles.seeAllTextFocused,
                    ]}
                  >
                    See all
                  </Text>
                  <Text
                    style={[
                      styles.seeAllSubtext,
                      seeAllFocused && styles.seeAllSubtextFocused,
                    ]}
                  >
                    View more content
                  </Text>
                </LinearGradient>
              </BlurView>
            </Pressable>
          </TVFocusGuideView>
        );
      }

      // Render regular card
      return (
        <Card
          item={item as SearchResult}
          onPress={() => onItemPress?.(item as SearchResult)}
          onFocus={() => {
            props.onSectionFocus?.(sectionKey);
            handleCardFocus(index);
          }}
          width={cardWidth}
          height={cardHeight}
        />
      );
    };

    const [seeAllFocused, setSeeAllFocused] = useState(false);

    const handleSeeAllBlur = () => {
      setSeeAllFocused(false);
    };

    const handleSeeAllFocus = () => {
      setSeeAllFocused(true);
    };

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
            <Animated.Text style={[styles.title, animatedTitleStyle]}>
              {title}
            </Animated.Text>
          </LinearGradient>
        </View>

        {/* Content List */}
        {data.length > 0 ? (
          <TVFocusGuideView autoFocus>
            <FlatList
              ref={flatListRef}
              data={listData}
              renderItem={renderItem}
              keyExtractor={(item) =>
                "type" in item && item.type === "see-all"
                  ? "see-all"
                  : `${(item as SearchResult).media_type}-${
                      (item as SearchResult).id
                    }`
              }
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
    marginBottom: 8,
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
    marginLeft: -10,
  },
  seeAllCard: {
    width: 320,
    height: 180,
    borderRadius: 16,
    overflow: "hidden",
    marginHorizontal: 6,
    marginVertical: 8,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.12)",
    backgroundColor: "rgba(0,0,0,0.4)",
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 8,
    },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 8,
  },
  seeAllFocused: {
    backgroundColor: "rgba(255,255,255,0.65)",
    borderColor: "rgba(255,255,255,0.8)",
    transform: [{ scale: 1.05 }],
    shadowColor: "#FFFFFF",
    shadowOpacity: 0.4,
    shadowRadius: 20,
    elevation: 15,
  },
  seeAllTextFocused: {
    color: "rgba(0,0,0,1)",
  },
  seeAllCardBlur: {
    flex: 1,
    borderRadius: 16,
    backgroundColor: "rgba(0,0,0,0.1)",
  },
  seeAllCardGradient: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    gap: 8,
    borderRadius: 16,
    paddingHorizontal: 24,
    paddingVertical: 20,
    position: "relative",
  },
  seeAllCardText: {
    color: "rgba(255,255,255,0.95)",
    fontSize: 20,
    fontFamily: "Urbanist_700Bold",
    textAlign: "center",
  },
  seeAllSubtext: {
    color: "rgba(255,255,255,0.6)",
    fontSize: 14,
    marginTop: -6,
    fontFamily: "Urbanist_500Medium",
  },
  seeAllSubtextFocused: {
    color: "rgba(0,0,0,1)",
  },
  seeAllIconContainer: {
    position: "absolute",
    top: 12,
    right: 12,
  },
  seeAllIconGradient: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: "center",
    alignItems: "center",
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
