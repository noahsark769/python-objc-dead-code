from unittest import TestCase
from parsers.define import parse

class DefineSymbolParserTest(TestCase):
    def _assertParse(self, expected, content):
        self.assertItemsEqual(
            expected,
            parse(content)
        )

    def test_regular_defines(self):
        content = """
        #define YPDistanceInMetersInvalid DBL_MAX
        #define kButtonHeight 37
        #define YPRangeZero NSMakeRange(0, 0)
        #define kBusinessUpdaterDaysStale -7 // Days before business becomes stale and needs update
        #define kFromThisBusinessBackgroundColor YKRGBAColorMake(244, 245, 240, 1.0)
        #define YPDebugSearch(...) [[YPDebug searchLogger] logFuncDebug:__func__ line:__LINE__ msg:__VA_ARGS__]
        #define YPDemoMode (YES)
        #define YPAlternatingOffset(__OFFSET__) -((__OFFSET__ + 1) % 2) * ((int)round((__OFFSET__ + 1) / 2)) + (((__OFFSET__ + 1) + 1) % 2) * ((int)round((__OFFSET__ + 1) / 2))
        #define PROPERTY(propName) NSStringFromSelector(@selector(propName))
        """
        self._assertParse([
            "YPDistanceInMetersInvalid",
            "kButtonHeight",
            "YPRangeZero",
            "kBusinessUpdaterDaysStale",
            "kFromThisBusinessBackgroundColor",
            "YPDebugSearch",
            "YPDemoMode",
            "YPAlternatingOffset",
            "PROPERTY",
        ], content)

    def test_long_function(self):
        content = """
        #define YKLocalizedStringWithGender(__MALE_KEY__, __FEMALE_KEY__, gender) (gender == YPGenderFemale ? [YKLocalized localize:__FEMALE_KEY__ tableName:nil value:nil] : [YKLocalized localize:__MALE_KEY__ tableName:nil value:nil])
        """
        self._assertParse(["YKLocalizedStringWithGender"], content)

    def test_multiline_function(self):
        content = """
        #define YP_GA_SET_DIMENSION_AND_CLEAR_VALUE(gaTracker, customDimensionValue, dimension)       \\
          do {                                                                                        \\
            [gaTracker set:[GAIFields customDimensionForIndex:dimension] value:customDimensionValue]; \\
            if (customDimensionValue) {                                                               \\
              [self.customDimensionsToBeCleared addObject:@(dimension)];                              \\
            }                                                                                         \\
          } while (0)
        """
        self._assertParse(["YP_GA_SET_DIMENSION_AND_CLEAR_VALUE"], content)

    def test_ignores_properties(self):
        content = """
        @interface YPWeeklyYelp : NSObject

        @property (readonly, copy, nonatomic) NSString *marketId;
        @property (readonly, copy, nonatomic) NSString *marketName;
        @property (readonly, copy, nonatomic) NSString *marketLocale;
        @property (readonly, copy, nonatomic) NSString *publishDate;
        @property (readonly, copy, nonatomic) NSString *text;
        @property (readonly, copy, nonatomic) NSString *headlinePhotoCreditName;
        @property (readonly, copy, nonatomic) NSString *headlinePhotoTitle;
        @property (readonly, copy, nonatomic) NSString *headlinePhotoUrl;
        @property (readonly, copy, nonatomic) NSString *shareUrl;
        @property (readonly, copy, nonatomic) NSArray *businesses;
        @property (readonly, copy, nonatomic) NSArray *events;
        @property (readonly, copy, nonatomic) NSArray *reviews;
        @property (readonly, assign, nonatomic) BOOL isStub;

        @property (readonly, copy, nonatomic) NSArray<YPWeeklyYelpFeature *> *features;

        + (YPWeeklyYelp *)weeklyYelpFromJSONDictionary:(NSDictionary *)dict request:(YPWeeklyYelpRequest *)request;

        @end
        """
        self.assertItemsEqual(
            [],
            parse(content)
        )

    def test_while(self):
        content = """
        #define YPDebug(fmt, ...) \\
          do {                    \\
          } while (0)
        """
        self._assertParse(["YPDebug"], content)
