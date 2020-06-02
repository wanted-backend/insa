from django.urls import path

from .views import CompanyRegister, CompanyPosition, PositionList, DetailView, PositionBookmarkView, PositionApplyView

urlpatterns = [
    path('/register', CompanyRegister.as_view()),
    path('/positions/create', CompanyPosition.as_view()),
    path('/positions', PositionList.as_view()),
    path('/position/<int:position_id>', DetailView.as_view()),
    path('/position/<int:position_id>/bookmark', PositionBookmarkView.as_view()),
    path('/position/<int:position_id>/apply', PositionApplyView.as_view())
]
