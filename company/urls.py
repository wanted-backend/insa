from django.urls import path

from .views import CompanyRegister, CompanyPosition, PositionList, DetailView, ThemeTop, ThemeList, PositionBookmarkView

urlpatterns = [
    path('/register', CompanyRegister.as_view()),
    path('/positions/create', CompanyPosition.as_view()),
    path('/themetop/<int:theme_id>',ThemeTop.as_view()),
    path('/themelist/<int:theme_id>',ThemeList.as_view()),
    path('/positions', PositionList.as_view()),
    path('/position/<int:position_id>', DetailView.as_view()),
    path('/bookmark/<int:position_id>', PositionBookmarkView.as_view())
]
