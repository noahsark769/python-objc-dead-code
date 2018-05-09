from unittest import TestCase

from parsers.constant import parse

class ConstantSymbolParserTest(TestCase):
    def _assertParse(self, expected, content):
        self.assertItemsEqual(
            expected,
            parse(content)
        )

    def test_regular_constants(self):
        content = """
        NSString *const YPAnnouncementTypeUnknown;
        """
        self._assertParse(["YPAnnouncementTypeUnknown"], content)

    def test_extern(self):
        content = """
        extern NSString *const BusinessDidViewNotification;
        """
        self._assertParse(["BusinessDidViewNotification"], content)

    def test_many_with_function(self):
        content = """
        // Announcement types
        extern NSString *const YPAnnouncementTypeUnknown;
        extern NSString *const YPAnnouncementTypeOther;
        extern NSString *const YPAnnouncementTypeHappyHour;
        extern NSString *const YPAnnouncementTypeLiveMusic;
        extern NSString *const YPAnnouncementTypeTriviaNight;
        extern NSString *const YPAnnouncementTypeUpcomingEvent;
        extern NSString *const YPAnnouncementTypeSpecialOffer;
        extern NSString *const YPAnnouncementTypeSale;
        extern NSString *const YPAnnouncementTypeNewMerchandise;
        extern NSString * YPAnnouncementTypeSomethingElse;

        extern NSString *YPAnnouncementTypeFromNSString(NSString *complimentName);
        """
        self._assertParse([
            "YPAnnouncementTypeUnknown",
            "YPAnnouncementTypeOther",
            "YPAnnouncementTypeHappyHour",
            "YPAnnouncementTypeLiveMusic",
            "YPAnnouncementTypeTriviaNight",
            "YPAnnouncementTypeUpcomingEvent",
            "YPAnnouncementTypeSpecialOffer",
            "YPAnnouncementTypeSale",
            "YPAnnouncementTypeNewMerchandise",
            "YPAnnouncementTypeSomethingElse",
        ], content)

    def test_ignores_define(self):
        content = """
        #define YPDistanceInMetersInvalid DBL_MAX
        """
        self._assertParse([], content)

    def test_ignores_define_semicolon(self):
        content = """
        #define DoReturn return self;
        """
        self._assertParse([], content)

    def test_ignores_typedef(self):
        content = """
        typedef NSInteger YPReviewActivity;
        """
        self._assertParse([], content)

    def test_ignores_function(self):
        content = """
        NSString *YPNSStringFromYPReviewActivity(YPReviewActivity reviewState);
        """
        self._assertParse([], content)

    def test_ignores_enum(self):
        content = """
        /*!
         @typedef ReviewTranslationProvider
         @brief Providers for machine-translated reviews.
         @field ReviewTranslationProviderNone Used if the provider is unknown
         @field ReviewTranslationProviderBing Bing Translate
         @field ReviewTranslationProviderGoogle Google Translate
         */
        typedef NS_ENUM(NSInteger, ReviewTranslationProvider) {
          ReviewTranslationProviderNone = 0,
          ReviewTranslationProviderBing = 1,
          ReviewTranslationProviderGoogle = 2,
        };

        typedef enum {
          YPVoteButtonTypeUseful = 1,
          YPVoteButtonTypeFunny = 2,
          YPVoteButtonTypeCool = 3
        } YPVoteButtonType;

        // Review State.
        enum {
          YPReviewActivityNone = 0,
          YPReviewActivityNotStarted,
          YPReviewActivityDrafted,
          YPReviewActivityFinishedRecently,
          YPReviewActivityNotFinishedRecently
        };
        typedef NSInteger YPReviewActivity;
        """
        self._assertParse([], content)

    def test_ignores_forward_declarations(self):
        content = """
        @class Reivew;
        @protocol SomeProtocolp
        NS_ENUM(NSInteger, YPEnumType);
        NS_OPTIONS(NSInteger, YPOptionsType);
        """
        self._assertParse([], content)

    def test_large_ignores_interface_keywords(self):
        content = """
        @interface YPUserBadgeView : UIView <YKImageLoaderDelegate> {
          YKImageLoader *_imageLoader;
          NSString *_userName;
          NSString *_userLocation;
          NSString *_imageURL;
          NSString *_reviewCountString;
          NSString *_friendCountString;
          UIColor *_textColor;

          CGSize _imageSize;
          CGSize _userNameSize;

          UIEdgeInsets _insets;
          YPUserBadgeViewStyle _style;

          UILabel *_dateLabel;
          NSString *_warningMessage;
          YPBusinessInteractionBadgeView *_checkInBadgeView;
          YPUserBadgeViewDataSource *_dataSource;

          BOOL _elite;
          NSString *_eliteString;

          UIColor *_shadowColor;
          CGSize _shadowOffset;

          CGFloat _cornerRadius;

          UIImage *_friendsIcon;
          UIImage *_reviewsIcon;
        }

        @property (copy, nonatomic) NSString *userName;
        @property (copy, nonatomic) NSString *userLocation;
        @property (copy, nonatomic) NSString *imageURL;

        //! Size of the user icon image square in pixels.  Default is 60px
        //@property (assign, nonatomic) CGSize imageSize;
        @property (copy, nonatomic) NSString *reviewCountString;
        @property (copy, nonatomic) NSString *friendCountString;

        //! Width to truncate username at if > 0
        @property (assign, nonatomic) CGSize userNameSize;

        @property (strong, nonatomic) UIColor *textColor;

        @property (readonly, nonatomic) YPUserBadgeViewStyle style;

        @property (assign, nonatomic) UIEdgeInsets insets;

        @property (copy, nonatomic) NSString *warningMessage;

        @property (strong, nonatomic) YKImageLoader *imageLoader;

        @property (strong, nonatomic) YPUserBadgeViewDataSource *dataSource;

        @property (strong, nonatomic) UIColor *shadowColor;
        @property (assign, nonatomic) CGSize shadowOffset;

        @property (assign, nonatomic) CGSize imageSize;
        @property (assign, nonatomic) CGFloat cornerRadius;

        - (id)initWithFrame:(CGRect)frame style:(YPUserBadgeViewStyle)style;

        /*!
         Set user with name, location, elite status, and friend and review count.
         */
        - (void)setUser:(User *)user;

        - (void)setDate:(NSDate *)date;
        - (CGPoint)drawInRect:(CGRect)rect;

        @end

        @interface YPUserBadgeCell : YKUITableViewCell {
          YPUserBadgeView *_view;
          id __weak _switchTarget;
          SEL _switchAction;

          YLSwitch *_accessorySwitch;
        }

        @property (readonly, nonatomic) YLSwitch *accessorySwitch;

        - (id)initWithReuseIdentifier:(NSString *)reuseIdentifier;
        - (void)setDate:(NSDate *)date;
        - (void)setDataSource:(YPUserBadgeViewDataSource *)dataSource;

        - (void)enableAccessorySwitchWithTarget:(id)target action:(SEL)action;

        @end
        """
        self._assertParse([], content)

    def test_ignores_structs(self):
        content = """
        // Options for displaying localized distances
        typedef struct {
          unsigned int appendUnits : 1;               // If YES, append units
          unsigned int leadingZero : 1;               // If YES, allow leading zero (0.3 instead of .3)
          unsigned int newlineSeparatorNonMetric : 1; // If YES, add newline in between value and units (Non-metric only)
          unsigned int unicodeFractions : 1;          // If YES, show unicode fractions
          unsigned int useLabels : 1;
          unsigned int hideZero : 1;        // If YES and the value evaluates to 0, then return empty string
          unsigned int abbreviateUnits : 1; // If YES use unit abbreviations (i.e. miles -> mi)
        } YPLocalizationDistanceOptions;
        """
        self.assertItemsEqual(
            [],
            parse(content)
        )

    def test_equal_signs(self):
        content = """
        static const CGFloat kFooterButtonHeight = 44.0;
        """
        self.assertItemsEqual(
            ["kFooterButtonHeight"],
            parse(content)
        )

