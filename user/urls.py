from django.urls import path

from .views import UserEmailExists, UserRegisterView, AdminRegisterView, LogInView, LikedCompanies

urlpatterns = [
    path('/extsis', UserEmailExists.as_view()),
	path('/register', UserRegisterView.as_view()),
	path('/adminregister', AdminRegisterView.as_view()),
	path('/login', LogInView.as_view()),
    path('/matchup/likes', LikedCompanies.as_view()),
]
