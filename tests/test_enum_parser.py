from unittest import TestCase

from parsers.enum import parse

class EnumSymbolParserTest(TestCase):
    def test_regular_enum(self):
        content = """
        typedef NS_ENUM(NSInteger, MyCheckInsViewControllerSection) {
            kStatusCellSection = 0, kCheckInsSection = 1,
            kActivityViewSection = 2
        };
        """
        self.assertItemsEqual(
            ["MyCheckInsViewControllerSection", "kStatusCellSection", "kCheckInsSection", "kActivityViewSection"],
            parse(content)
        )

    def test_whitespace(self):
        content = """



        typedef NS_ENUM(NSInteger, MyCheckInsViewControllerSection) {
            kStatusCellSection = 0, kCheckInsSection = 1,

            
            kActivityViewSection = 2
        };



        """
        self.assertItemsEqual(
            ["MyCheckInsViewControllerSection", "kStatusCellSection", "kCheckInsSection", "kActivityViewSection"],
            parse(content)
        )

    def test_trailing_comma(self):
        content = """
        typedef NS_ENUM(NSInteger, YPWeeklyYelpRequestSource) {
          YPWeeklyYelpRequestSourceUnknown = 0,
          YPWeeklyYelpRequestSourceDiscover,
          YPWeeklyYelpRequestSourceMoreMenu,
        };
        """
        self.assertItemsEqual(
            ["YPWeeklyYelpRequestSource", "YPWeeklyYelpRequestSourceUnknown", "YPWeeklyYelpRequestSourceDiscover", "YPWeeklyYelpRequestSourceMoreMenu"],
            parse(content)
        )

    def test_comments(self):
        content = """
        /*!
         * Places in the app where we might request the Weekly from. These are necessary in order to send
         * back Weekly issues in different places based on the source: for example, a logged in user will
         * see the weekly from their primary location (set by the user), but *only* when accessing the Weekly
         * from the more menu (other places might show the current location instead of the primary location).
         */
        typedef NS_ENUM(NSInteger, YPWeeklyYelpRequestSource) {
          YPWeeklyYelpRequestSourceUnknown = 0, /* we don't *know* the/source */
          YPWeeklyYelpRequestSourceDiscover, // request weekly from the discover tab
          YPWeeklyYelpRequestSourceMoreMenu, // request weekly from the weekly button in the more menu
        };
        """
        self.assertItemsEqual(
            ["YPWeeklyYelpRequestSource", "YPWeeklyYelpRequestSourceUnknown", "YPWeeklyYelpRequestSourceDiscover", "YPWeeklyYelpRequestSourceMoreMenu"],
            parse(content)
        )

    def test_badly_formatted(self):
        content = """
        NS_ENUM(NSInteger, AccountPaymentMethodsSection){
            AccountPaymentMethodsSectionAllMethods = 0,
            AccountPaymentMethodsSectionAddNewCard};
        """
        self.assertItemsEqual(
            ["AccountPaymentMethodsSection", "AccountPaymentMethodsSectionAllMethods", "AccountPaymentMethodsSectionAddNewCard"],
            parse(content)
        )

    def test_badly_formatted_first_line_value(self):
        content = """
        NS_ENUM(NSInteger, AccountPaymentMethodsSection){ AccountPaymentMethodsSectionAllMethods = 0,
            AccountPaymentMethodsSectionAddNewCard};
        """
        self.assertItemsEqual(
            ["AccountPaymentMethodsSection", "AccountPaymentMethodsSectionAllMethods", "AccountPaymentMethodsSectionAddNewCard"],
            parse(content)
        )

    def test_badly_formatted_inline(self):
        content = """
        NS_ENUM(NSInteger, AccountPaymentMethodsSection){ AccountPaymentMethodsSectionAllMethods = 0, AccountPaymentMethodsSectionAddNewCard};
        """
        self.assertItemsEqual(
            ["AccountPaymentMethodsSection", "AccountPaymentMethodsSectionAllMethods", "AccountPaymentMethodsSectionAddNewCard"],
            parse(content)
        )

    def test_forward_declaration(self):
        content = """
        typedef NS_ENUM(NSInteger, YPSearchFilterTableViewGroupIdentifier);
        """
        self.assertItemsEqual(
            [],
            parse(content)
        )

    def test_two_definitions(self):
        content = """
        typedef NS_ENUM(NSInteger, YPWeeklyYelpRequestSource) {
            YPWeeklyYelpRequestSourceUnknown = 0,
            YPWeeklyYelpRequestSourceDiscover,
            YPWeeklyYelpRequestSourceMoreMenu,
        };

        NS_ENUM(NSInteger, AccountPaymentMethodsSection){ AccountPaymentMethodsSectionAllMethods = 0,
            AccountPaymentMethodsSectionAddNewCard};
        """
        self.assertItemsEqual(
            [
                "YPWeeklyYelpRequestSource",
                "YPWeeklyYelpRequestSourceUnknown",
                "YPWeeklyYelpRequestSourceDiscover",
                "YPWeeklyYelpRequestSourceMoreMenu",
                "AccountPaymentMethodsSection",
                "AccountPaymentMethodsSectionAllMethods",
                "AccountPaymentMethodsSectionAddNewCard",
            ],
            parse(content)
        )

    def test_old_style(self):
        content = """
        typedef enum {
          YPKeyKahuna,
        } YPKey;

        typedef enum {
          CompressionModeZlib,
          CompressionModeGzip,
          CompressionModeRaw,
        } CompressionMode;
        """
        self.assertItemsEqual(
            [
                "YPKey",
                "YPKeyKahuna",
                "CompressionMode",
                "CompressionModeZlib",
                "CompressionModeGzip",
                "CompressionModeRaw",
            ],
            parse(content)
        )

    def test_old_style_no_name(self):
        content = """
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
        self.assertItemsEqual(
            [
                "YPReviewActivityNone",
                "YPReviewActivityNotStarted",
                "YPReviewActivityDrafted",
                "YPReviewActivityFinishedRecently",
                "YPReviewActivityNotFinishedRecently",
            ],
            parse(content)
        )

    def test_bitwise_values(self):
        content = """
        typedef NS_ENUM(NSInteger, MyCheckInsViewControllerSection) {
            kStatusCellSection = 0,
            kCheckInsSection = 1 << 2,
            kActivityViewSection = 1 << 3
        };
        """
        self.assertItemsEqual(
            ["MyCheckInsViewControllerSection", "kStatusCellSection", "kCheckInsSection", "kActivityViewSection"],
            parse(content)
        )

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

    def test_defines_inside(self):
        content = """
        typedef NS_ENUM(NSInteger, YPMoreMenuSecondarySectionRow) {
          YPMoreMenuSecondarySectionMonocleRow = 0,
          YPMoreMenuSecondarySectionFindFriendsRow,
          YPMoreMenuSecondarySectionAddBusinessRow,
          YPMoreMenuSecondarySectionWeeklyRow,
          YPMoreMenuSecondarySectionSettingsRow,
          YPMoreMenuSecondarySectionAppRateRow,
          YPMoreMenuSecondarySectionBugReportRow,
          YPMoreMenuSecondarySectionSupportRow,
        #if YP_DEBUG
          YPMoreMenuSecondarySectionDebugRow,
        #endif
        };
        """
        self.assertItemsEqual(
            [
            "YPMoreMenuSecondarySectionRow",
            "YPMoreMenuSecondarySectionMonocleRow",
            "YPMoreMenuSecondarySectionFindFriendsRow",
            "YPMoreMenuSecondarySectionAddBusinessRow",
            "YPMoreMenuSecondarySectionWeeklyRow",
            "YPMoreMenuSecondarySectionSettingsRow",
            "YPMoreMenuSecondarySectionAppRateRow",
            "YPMoreMenuSecondarySectionBugReportRow",
            "YPMoreMenuSecondarySectionSupportRow",
            "YPMoreMenuSecondarySectionDebugRow",
            ],
            parse(content)
        )
