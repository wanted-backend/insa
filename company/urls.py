from django.urls import path

from .views import CompanyRegister, CompanyPosition, PositionList

urlpatterns = [
	path('/register', CompanyRegister.as_view()),
	path('/positions/create', CompanyPosition.as_view()),
    path('/positions', PositionList.as_view()),
]
