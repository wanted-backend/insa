from django.urls import path

from .views import CompanyRegister, CompanyPosition, PositionList, DetailView, \
         PositionBookmarkView, PositionApplyView, LikedMatchupResume, LikedMatchupList, \
         UnreadMatchup , ThemeTop , ThemeList , HomeView

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
    path('/theme', ThemeTop.as_view()),
    path('/theme/list', ThemeList.as_view()),
    path('/home', HomeView.as_view()),
]
