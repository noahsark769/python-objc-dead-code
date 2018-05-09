from unittest import TestCase

from parsers.enum import parse

class EnumSymbolParserTest(TestCase):
    def test_regular_enum(self):
        content = """
        typedef NS_OPTIONS(NSUInteger, MyCheckInsViewControllerSection) {
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



        typedef NS_OPTIONS(NSUInteger, MyCheckInsViewControllerSection) {
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
        typedef NS_OPTIONS(NSUInteger, YPWeeklyYelpRequestSource) {
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
        typedef NS_OPTIONS(NSUInteger, YPWeeklyYelpRequestSource) {
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
        NS_OPTIONS(NSUInteger, AccountPaymentMethodsSection){
            AccountPaymentMethodsSectionAllMethods = 0,
            AccountPaymentMethodsSectionAddNewCard};
        """
        self.assertItemsEqual(
            ["AccountPaymentMethodsSection", "AccountPaymentMethodsSectionAllMethods", "AccountPaymentMethodsSectionAddNewCard"],
            parse(content)
        )

    def test_badly_formatted_first_line_value(self):
        content = """
        NS_OPTIONS(NSUInteger, AccountPaymentMethodsSection){ AccountPaymentMethodsSectionAllMethods = 0,
            AccountPaymentMethodsSectionAddNewCard};
        """
        self.assertItemsEqual(
            ["AccountPaymentMethodsSection", "AccountPaymentMethodsSectionAllMethods", "AccountPaymentMethodsSectionAddNewCard"],
            parse(content)
        )

    def test_badly_formatted_inline(self):
        content = """
        NS_OPTIONS(NSUInteger, AccountPaymentMethodsSection){ AccountPaymentMethodsSectionAllMethods = 0, AccountPaymentMethodsSectionAddNewCard};
        """
        self.assertItemsEqual(
            ["AccountPaymentMethodsSection", "AccountPaymentMethodsSectionAllMethods", "AccountPaymentMethodsSectionAddNewCard"],
            parse(content)
        )

    def test_forward_declaration(self):
        content = """
        typedef NS_OPTIONS(NSUInteger, YPSearchFilterTableViewGroupIdentifier);
        """
        self.assertItemsEqual(
            [],
            parse(content)
        )

    def test_two_definitions(self):
        content = """
        typedef NS_OPTIONS(NSUInteger, YPWeeklyYelpRequestSource) {
            YPWeeklyYelpRequestSourceUnknown = 0,
            YPWeeklyYelpRequestSourceDiscover,
            YPWeeklyYelpRequestSourceMoreMenu,
        };

        NS_OPTIONS(NSUInteger, AccountPaymentMethodsSection){ AccountPaymentMethodsSectionAllMethods = 0,
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


    def test_bitwise_values(self):
        content = """
        typedef NS_OPTIONS(NSUInteger, MyCheckInsViewControllerSection) {
            kStatusCellSection = 0,
            kCheckInsSection = 1 << 2,
            kActivityViewSection = 1 << 3
        };
        """
        self.assertItemsEqual(
            ["MyCheckInsViewControllerSection", "kStatusCellSection", "kCheckInsSection", "kActivityViewSection"],
            parse(content)
        )

    def test_bitwise_values_parentheses(self):
        content = """
        typedef NS_OPTIONS(NSUInteger, MyCheckInsViewControllerSection) {
            kStatusCellSection = 0,
            kCheckInsSection = (1 << 2),
            kActivityViewSection = (1 << 3)
        };
        """
        self.assertItemsEqual(
            ["MyCheckInsViewControllerSection", "kStatusCellSection", "kCheckInsSection", "kActivityViewSection"],
            parse(content)
        )
