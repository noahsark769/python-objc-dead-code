import pytest

from unittest import TestCase
from parsers.typedef import parse

class TypedefSymbolParserTest(TestCase):
    def _assertParse(self, expected, content):
        self.assertItemsEqual(
            expected,
            parse(content)
        )

    def test_regular_typedefs(self):
        content = """
        typedef NSTimeInterval BookmarksVersion;
        """
        self._assertParse(["BookmarksVersion"], content)

    def test_comments(self):
        content = """
        // Distance in meters
        typedef double YPDistanceInMeters;
        """
        self._assertParse(["YPDistanceInMeters"], content)

    def test_old_enum_no_name(self):
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
        self.assertItemsEqual(["YPReviewActivity"], parse(content))

    def test_block(self):
        content = """
        typedef void (^YPWatchSearchCompletionBlock)(NSArray *businesses, YKError *error);
        """
        self._assertParse(["YPWatchSearchCompletionBlock"], content)

    def test_block_param(self):
        content = """
        - (void)someMethodThatTakesABlock:(void (^)(BOOL))blockName;

        static inline void Func(void (^block)(void)) {}
        """
        self._assertParse([], content)

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

    def test_method_block_argument(self):
        content = """
typedef NS_ENUM(NSInteger, YPAccountBaseViewControllerSource) {
  YPAccountBaseViewControllerSourceNone = 0,
  YPAccountBaseViewControllerSourceWriteReview = 1,
  YPAccountBaseViewControllerSourceOnboarding = 2
};

@protocol YPAccountBaseViewControllerDelegate <NSObject>

- (void)accountViewControllerShouldBeDismissed:(YPAccountBaseViewController *)accountViewController completion:(void (^)(void))completion;
@end
        """
        self.assertItemsEqual(
            [],
            parse(content)
        )

