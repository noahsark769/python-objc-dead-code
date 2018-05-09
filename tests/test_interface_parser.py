from unittest import TestCase

from parsers.interface import parse

class InterfaceSymbolParserTest(TestCase):
    def test_normal_interface(self):
        content = """
        @interface YPWeeklyYelpView : UIView

        @property (weak, nonatomic) id<YPWeeklyYelpViewDelegate> delegate;
        @property (strong, nonatomic) YLTableView *tableView;

        - (instancetype)initWithDelegate:(id<YPWeeklyYelpViewDelegate>)delegate;
        - (void)setDataSource:(YPWeeklyYelpViewDataSource *)dataSource;

        @end
        """
        self.assertItemsEqual(
            ["YPWeeklyYelpView"],
            parse(content)
        )

    def test_with_comments(self):
        content = """
        /*!
         * @brief The view which contains the feed of businesses for the Weekly Yelp. Similarly to
         * YPBusinessViewController, this view pretty much wraps around a YLTableView which contains
         * a row for each of the table items in the weekly yelp view. Refer to YPWeeklyYelpViewDataSource
         * for how the table is constructed.
         *
         * Note: This is not the view for the Weekly Yelp item on the Activity Feed.
         */
        @interface YPWeeklyYelpView : UIView

        @property (weak, nonatomic) id<YPWeeklyYelpViewDelegate> delegate;
        @property (strong, nonatomic) YLTableView *tableView; // comment here

        - (instancetype)initWithDelegate:(id<YPWeeklyYelpViewDelegate>)delegate;
        /*
        Multiline comment
        */
        - (void)setDataSource:(YPWeeklyYelpViewDataSource *)dataSource; /*! Inline multiline comment */

        @end
        """
        self.assertItemsEqual(
            ["YPWeeklyYelpView"],
            parse(content)
        )

    def test_empty(self):
        content = """
        @interface YPWeeklyYelpView : UIView
        @end
        """
        self.assertItemsEqual(
            ["YPWeeklyYelpView"],
            parse(content)
        )

    def test_with_protocol(self):
        content = """
        @interface UserReviewsViewController : YPUITableViewController <YPTextContentDataSourceDelegate>

        - (instancetype)initWithUser:(User *)user;

        @property (readonly, nonatomic) User *user;

        @end
        """
        self.assertItemsEqual(
            ["UserReviewsViewController"],
            parse(content)
        )

    def test_multiple(self):
        content = """
        @interface UserReviewsViewController : YPUITableViewController <YPTextContentDataSourceDelegate>

        - (instancetype)initWithUser:(User *)user;

        @property (readonly, nonatomic) User *user;

        @end

        @interface UserReviewCellDataSource : BusinessPassportViewDataSource

        @property (strong, nonatomic) Review *review;

        @end
        """
        self.assertItemsEqual(
            ["UserReviewsViewController", "UserReviewCellDataSource"],
            parse(content)
        )

    def test_with_class_forward_delcaration(self):
        content = """
        @class Review;
        @class User;

        @interface UserReviewsViewController : YPUITableViewController <YPTextContentDataSourceDelegate>
        - (instancetype)initWithUser:(User *)user;
        @end
        """
        self.assertItemsEqual(
            ["UserReviewsViewController"],
            parse(content)
        )

    def test_complicated(self):
        content = """
        @interface ApproveFriendRequestViewController : YPUIViewController <ApproveFriendRequestViewDelegate, FriendRequestApproveRequestDelegate,
                                                                            FriendRequestIgnoreRequestDelegate, FriendRequestListRequestDelegate> {
          ApproveFriendRequestView *_approveFriendRequestView;
          YPUIViewController<UserViewController> *_userViewController;
          FriendApproveRequest *_friendApproveRequest;
          FriendIgnoreRequest *_friendIgnoreRequest;

          // For when loading friend request by identifier
          FriendRequestListRequest *_friendRequestListRequest;
        }

        @property (strong, nonatomic) FriendRequest *friendRequest;
        @property (weak, nonatomic) id<ApproveFriendRequestViewControllerDelegate> delegate;
        // The default (no block set) behavior is for iPhone only
        @property (copy, nonatomic) SelectUserIdBlock selectUserIdBlock;

        - (void)loadForUserId:(NSString *)userId;

        - (void)cancel;

        @end
        """
        self.assertItemsEqual(
            ["ApproveFriendRequestViewController"],
            parse(content)
        )

    def test_subclass_override(self):
        content = """
        @interface YPUsersListViewController () <YPUsersListTableViewDataSourceDelegate, YPSearchBarDelegate>

        @property (strong, nonatomic) YPUINavigationBarBackgroundView *redBackgroundView;

        @property (strong, nonatomic) YPSearchBarView *searchBarView;
        @property (strong, nonatomic) NSString *searchBarPlaceholder;

        //! If searchEnabled is YES, subclasses may override this to change which navigation bar the search bar will be attached to. See example in YPUserFriendsViewController.
        @property (readonly, nonatomic) YPUINavigationBar *navigationBarForSearchBarAnchoring;

        @property (strong, nonatomic) YPUsersListTableViewDataSource *dataSource;

        @end
        """
        self.assertItemsEqual(
            [],
            parse(content)
        )

    def test_category(self):
        content = """
        //! @abstract The logic for when to send analytics for a user allowing or denying access to a locked device service (contacts, photos, location, etc.) is pretty much the same everywhere. This class wraps that logic up into a helper object, so that we keep that logic consistent.
        @interface AnalyticsManager (YPDevicePermissionAnalytics)

        /*!
         @abstract Sends an analytic for the current authorization status
         @param currentStatus NSInteger status value representing the current authorization status for the service
         @param defaultsKey NSString key used to save (to YPUserDefaults) the last authorization status
         @param allowedIRI NSString IRI analytic to send if the status is one that means the service was authorized by the user
         @param deniedIRI NSString IRI analytic to send if the status is one that means the service was denied by the user
         @param allowedValue NSInteger If the authorization status matches this one, then allowedIRI is sent as an analytic
         @param deniedValue NSInteger If the authorization status matches this one, then deniedIRI is sent as an analytic
         @discussion An analytic is only sent if currentStatus matches allowedValue or deniedValue and currentStatus is not the value that was reported as the authorization status for this service previously. This is based on the value stored in YPUserDefaults, which is keyed by the defaultsKey passed into initialization of this object.
         */
        - (void)sendAnalyticForAuthorizationStatus:(NSInteger)currentStatus
                                  usingDefaultsKey:(NSString *)defaultsKey
                                        allowedIRI:(NSString *)allowedIRI
                                         deniedIRI:(NSString *)deniedIRI
                                      allowedValue:(NSInteger)allowedValue
                                       deniedValue:(NSInteger)deniedValue;

        @end
        """
        self.assertItemsEqual(
            [],
            parse(content)
        )

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
            ["AnalyticsManager"],
            parse(content)
        )
