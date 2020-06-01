from django.urls import path

from .views import UserRegisterView, AdminRegisterView, LogInView

urlpatterns = [
	path('userregister', UserRegisterView.as_view()),
	path('adminregister', AdminRegisterView.as_view()),
	path('login', LogInView.as_view()),
]
