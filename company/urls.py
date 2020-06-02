from django.urls import path

from .views import CompanyRegister, CompanyPosition, PositionList, DetailView, PositionBookmarkView, LikedMatchupResume

urlpatterns = [
	path('/register', CompanyRegister.as_view()),
	path('/positions/create', CompanyPosition.as_view()),
    path('/positions', PositionList.as_view()),
    path('/position/<int:position_id>', DetailView.as_view()),
    path('/bookmark/<int:position_id>', PositionBookmarkView.as_view()),
    path('/like', LikedMatchupResume.as_view()),
]
