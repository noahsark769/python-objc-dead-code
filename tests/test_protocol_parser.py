from unittest import TestCase
from parsers.protocol import parse

class ProtocolSymbolParserTest(TestCase):
    def _assertParse(self, expected, content):
        self.assertItemsEqual(
            expected,
            parse(content)
        )

    def test_normal_protocol(self):
        content = """
        @protocol BookmarksTableViewDataSourceDelegate <NSObject>

        - (void)bookmarkTableViewDataSourceDidSelectLoadMore:(BookmarksTableViewDataSource *)bookmarkTableViewDataSource;

        @end
        """
        self._assertParse(["BookmarksTableViewDataSourceDelegate"], content)

    def test_comments(self):
        content = """
        /*!
        * This is a comment about the protocol.
        */
        @protocol BookmarksTableViewDataSourceDelegate <NSObject> /* Inline *sweet* comment/tip! */

        - (void)bookmarkTableViewDataSourceDidSelectLoadMore:(BookmarksTableViewDataSource *)bookmarkTableViewDataSource; // do *something* here/don't do anything

        /*
        Random multiline
        */

        @end
        """
        self._assertParse(["BookmarksTableViewDataSourceDelegate"], content)

    def test_multiple(self):
        content = """
        @protocol BookmarksTableViewDataSourceDelegate <NSObject>

        - (void)bookmarkTableViewDataSourceDidSelectLoadMore:(BookmarksTableViewDataSource *)bookmarkTableViewDataSource;

        @end

        @protocol VersionCheckRequestDelegate <NSObject>
        - (void)versionCheckRequest:(VersionCheckRequest *)request didGetDFPAccountID:(NSString *)dfpAccountID;
        - (void)versionCheckRequest:(VersionCheckRequest *)request didGetVersionInfo:(NSDictionary *)response;
        - (void)versionCheckRequest:(VersionCheckRequest *)request didError:(YKError *)error;
        - (void)versionCheckRequestDidCancel:(VersionCheckRequest *)request;
        - (void)versionCheckRequest:(VersionCheckRequest *)request didGetFeatureInfo:(NSDictionary *)features;
        - (void)versionCheckRequest:(VersionCheckRequest *)request didGetExperimentsDict:(NSDictionary *)experimentsDict;
        @end
        """
        self._assertParse(["BookmarksTableViewDataSourceDelegate", "VersionCheckRequestDelegate"], content)

    def test_no_forward_declaration(self):
        content = """
        @protocol YPMapBusinessAnnotation;

        @protocol BookmarksTableViewDataSourceDelegate <NSObject>

        - (void)bookmarkTableViewDataSourceDidSelectLoadMore:(BookmarksTableViewDataSource *)bookmarkTableViewDataSource;

        @end
        """
        self._assertParse(["BookmarksTableViewDataSourceDelegate"], content)

    def test_complicated_inline_function_conforming(self):
        content = """
        @class VersionCheckRequest;

        @protocol SomeProtocol <NSObject>
        @end

        @protocol VersionCheckRequestDelegate <NSObject>
        - (void)versionCheckRequest:(VersionCheckRequest *)request didGetDFPAccountID:(NSString *)dfpAccountID;
        - (void)versionCheckRequest:(VersionCheckRequest *)request didGetVersionInfo:(NSDictionary *)response;
        - (void)versionCheckRequest:(VersionCheckRequest *)request didError:(YKError *)error;
        - (void)versionCheckRequestDidCancel:(VersionCheckRequest *)request;
        - (void)versionCheckRequest:(VersionCheckRequest *)request didGetFeatureInfo:(NSDictionary *)features;
        - (void)versionCheckRequest:(VersionCheckRequest *)request didGetExperimentsDict:(NSDictionary *)experimentsDict;
        @end

        @interface VersionCheckRequest : YPAPIRequest

        @property (weak, nonatomic) id<VersionCheckRequestDelegate> delegate;
        /*!
         Initiates a request to check for a new version of the Yelp app.
         If a new version is available, prompts the user to upgrade, possibly
         forcing them to if the response indicates.

         @param currentVersionString The string of the current version of this app, such as what would be in the Info.plist
         */
        - (void)checkForNewVersion:(NSString *)currentVersionString;

        @end

        inline BOOL YPConforms(VersionCheckRequest *request) {
          return [request conformsToProtocol:@protocol(SomeProtocol)];
        };
        """
        self._assertParse(["SomeProtocol", "VersionCheckRequestDelegate"], content)

    def test_no_inheritance(self):
        content = """
        @protocol TipsViewControllerDelegate_iPad
        - (void)tipsViewController:(TipsViewController_iPad *)tipsViewController didEditTip:(Tip *)tip;
        - (void)tipsViewController:(TipsViewController_iPad *)tipsViewController didDeleteTip:(Tip *)tip;
        - (void)tipsViewController:(TipsViewController_iPad *)tipsViewController didLikeTip:(Tip *)tip;
        @end
        """
        self._assertParse(["TipsViewControllerDelegate_iPad"], content)

    def test_many(self):
        content = """
        @class YPUITabBarViewController_iPad;

        @protocol YPTabBarRootViewController;

        @protocol YPUITabBarViewController_iPad_Selection
        - (void)willDeselectViewControllerForTabBarViewController_iPad:(YPUITabBarViewController_iPad *)tabBarViewController;
        @end

        @protocol YPUITabBarViewController_iPad_TabBarSelection
        - (void)didSelectFromTabBarChanged:(BOOL)changed;
        @end

        @protocol YPUITabBarViewController_iPadDelegate <NSObject>

        @end
        """
        self._assertParse([
            "YPUITabBarViewController_iPad_Selection",
            "YPUITabBarViewController_iPad_TabBarSelection",
            "YPUITabBarViewController_iPadDelegate"
        ], content)

    def test_large(self):
        content = """
        @protocol BusinessViewController <NSObject>

        @property (copy, nonatomic) ActionBlock businessDidLoadBlock;

        /*!
         Set business.
         @param business
         */
        - (void)setBusiness:(Business *)business;

        /*!
         Set business.
         @param business
         @param selectedReviewId
         */
        - (void)setBusiness:(Business *)business selectedReviewId:(NSString *)selectedReviewId;

        /*!
         Set business.
         @param business
         @param platformConfirmation
         @param promotedFilter
         */
        - (void)setBusiness:(Business *)business platformConfirmation:(YPPlatformConfirmation *)platformConfirmation promotedFilter:(YPDisplaySearchFilter *)promotedFilter;

        /*!
         Open business with identifier.
         @param businessId
         */
        - (void)openBusinessId:(NSString *)businessId;

        /*!
         Open business with identifier.
         @param businessId
         @param platformConfirmation
         */
        - (void)openBusinessId:(NSString *)businessId platformConfirmation:(YPPlatformConfirmation *)platformConfirmation;

        /*!
         Open business with identifier.
         @param businessId
         @param selectedReviewId
         */
        - (void)openBusinessId:(NSString *)businessId selectedReviewId:(NSString *)selectedReviewId;

        - (void)openBusinessId:(NSString *)businessId businessDidLoadBlock:(ActionBlock)actionBlock;

        /*!
         Open business with identifier from specified external provider who launched the app.
         @param businessId
         @param provider External prover who launched the app. (optional, currently "google")
         */
        - (void)openBusinessId:(NSString *)businessId provider:(NSString *)provider;

        /*!
         Set search query.
         @param searchQuery Search query that found the business, may be nil
         */
        - (void)setSearchQuery:(NSString *)searchQuery;

        - (void)openMap;
        - (void)openMenu;

        @end
        """
        self._assertParse(["BusinessViewController"], content)
