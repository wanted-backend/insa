from django.urls import path

from .views import UserEmailExists, UserRegisterView, AdminRegisterView, LogInView, LikedCompanies, ResumeView, UserResumeWriteView, ResumeDetailWriteView, ResumeDetailView

urlpatterns = [
	path('/extsis', UserEmailExists.as_view()),
        path('/register', UserRegisterView.as_view()),
	path('adminregister', AdminRegisterView.as_view()),
	path('login', LogInView.as_view()),
        path('/matchup/likes', LikedCompanies.as_view()),
        path('resume', ResumeView.as_view()),
        path('resume/<str:main_resume_id>', UserResumeWriteView.as_view()),
        path('resumeDetailWrite/<str:main_resume_id>', ResumeDetailWriteView.as_view()),
        path('resumeDetail/<str:main_resume_id>', ResumeDetailView.as_view()),
]
