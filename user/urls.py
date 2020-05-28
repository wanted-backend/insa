from django.urls import path

from .views import SignUpView, LogInView

urlpatterns = [
	path('sign-up', SignUpView.as_view()),
	path('login', LogInView.as_view()),
]
