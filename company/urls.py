from django.urls import path

from .views import CompanyRegister, CompanyPosition, PositionList, DetailView, \
        PositionBookmarkView, PositionApplyView, CompanyRequestResume, CompanyReadingResume, \
        JobAdPosition, MatchupList, ThemeList, HomeView, CompanyLikedResume, \
        PositionAdvertisement, PositionMain, MainFilter, TagView, TagSearch, JobAdPurchase, \
        JobAdPurchased , MatchUpItem , CompanyProposalsResume, CompanyInfomationModify, \
        NetworkAd, CompanyMatchupSearch

urlpatterns = [
    path('/register', CompanyRegister.as_view()),
    path('/modify', CompanyInfomationModify.as_view()),
    path('/positions/create', CompanyPosition.as_view()),
    path('/positions', PositionList.as_view()),
    path('/position/<int:position_id>', DetailView.as_view()),
    path('/like/resume', CompanyLikedResume.as_view()),
    path('/request/matchup', CompanyRequestResume.as_view()),
    path('/position/<int:position_id>/bookmark', PositionBookmarkView.as_view()),
    path('/position/<int:position_id>/apply', PositionApplyView.as_view()),
    path('/matchup/list', MatchupList.as_view()),
    path('/themelist/<int:theme_id>', ThemeList.as_view()),
    path('/home', HomeView.as_view()),
    path('/job-ad/positions', JobAdPosition.as_view()),
    path('/read/matchup', CompanyReadingResume.as_view()),
    path('/proposals/matchup', CompanyProposalsResume.as_view()),
    path('/position/main', PositionMain.as_view()),
    path('/position/advertisement', PositionAdvertisement.as_view()),
    path('/job-ad/purchase', JobAdPurchase.as_view()),
    path('/position/main/filter', MainFilter.as_view()),
    path('/position/tag', TagView.as_view()),
    path('/position/tag/search', TagSearch.as_view()),
    path('/job-ad/purchased',JobAdPurchased.as_view()),
    path('/network-ad',NetworkAd.as_view()),
    path('/matchup/item',MatchUpItem.as_view()),
    path('/matchup/search', CompanyMatchupSearch.as_view())
]
