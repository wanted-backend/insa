from django.urls import path

from .views import CompanyRegister, CompanyPosition, PositionList, DetailView, \
         PositionBookmarkView, PositionApplyView, LikedMatchupResume, LikedMatchupList, \
         UnreadMatchup , ThemeTop , ThemeList , HomeView , JobAd

urlpatterns = [
    path('/register', CompanyRegister.as_view()),
    path('/positions/create', CompanyPosition.as_view()),
    path('/positions', PositionList.as_view()),
    path('/position/<int:position_id>', DetailView.as_view()),
    path('/bookmark/<int:position_id>', PositionBookmarkView.as_view()),
    path('/like', LikedMatchupResume.as_view()),
    path('/liked/matchup', LikedMatchupList.as_view()),
    path('/position/<int:position_id>/bookmark', PositionBookmarkView.as_view()),
    path('/position/<int:position_id>/apply', PositionApplyView.as_view()),
    path('/unread', UnreadMatchup.as_view()),
    path('/themetop/<int:theme_id>', ThemeTop.as_view()),
    path('/themelist/<int:theme_id>', ThemeList.as_view()),
    path('/home', HomeView.as_view()),
    path('/job-ad', JobAd.as_view()),
]
