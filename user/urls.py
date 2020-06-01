from django.urls import path

from .views import UserEmailExists, UserRegisterView, AdminRegisterView, LogInView

urlpatterns = [
    path('/extsis', UserEmailExists.as_view()),
	path('/register', UserRegisterView.as_view()),
	path('/adminregister', AdminRegisterView.as_view()),
	path('/login', LogInView.as_view()),
]
