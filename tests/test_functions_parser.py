from unittest import TestCase

from parsers.functions import parse

class FunctionSymbolParserTest(TestCase):
    def _assertParse(self, expected, content):
        self.assertItemsEqual(
            expected,
            parse(content)
        )

    def test_regular_function(self):
        content = """
        NSString *YPNSStringFromYPGender(YPGender gender);
        """
        self.assertItemsEqual(
            ["YPNSStringFromYPGender"],
            parse(content)
        )

    def test_generics_function(self):
        content = """
        NSArray<NSString *> YPGenderNames();
        """
        self.assertItemsEqual(
            ["YPGenderNames"],
            parse(content)
        )

    def test_inline_functions(self):
        content = """
        static inline void Fix();
        """
        self.assertItemsEqual(
            ["Fix"],
            parse(content)
        )

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

    def test_ignores_block_typedefs(self):
        content = """
        @class YKError;

        typedef void (^YPWatchReviewsReplyBlock)(NSArray * /*of NSDictionary*/ reviews, YKError *error);

        @interface YPWatchReviewsController : NSObject

        + (instancetype)sharedController;
        - (void)listWithBusinessId:(NSString *)businessId completionBlock:(YPWatchReviewsReplyBlock)completion;
        - (void)cancel;

        @end
        """
        self.assertItemsEqual(
            [],
            parse(content)
        )

    def test_enum(self):
        content = """
        typedef NS_ENUM(NSInteger, YPWatchErrorType) {
          YPWatchErrorTypeGeneric = 0,
          YPWatchErrorTypeLocationAccessNotDetermined,
          YPWatchErrorTypeLocationAccessDenied,
          YPWatchErrorTypeLocationNotFound,
          YPWatchErrorTypeServerError,
          YPWatchErrorTypeConnectionError,
          YPWatchErrorTypeSearchError,
          YPWatchErrorTypeUnknown
        };
        """
        # will be parsed by enum parser
        self._assertParse([], content)

    def test_while(self):
        content = """
        #define YPDebug(fmt, ...) \\
          do {                    \\
          } while (0)
        """
        self._assertParse([], content)

    def test_category_same_file(self):
        content = """
        @interface AnalyticsManager : NSObject

        - (void)aMethod;

        @end

        @interface AnalyticsManager (YPDevicePermissionAnalytics)
        - (void)sendAnalyticForAuthorizationStatus;
        @end
        """
        self.assertItemsEqual(
            [],
            parse(content)
        )
