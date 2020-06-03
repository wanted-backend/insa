from django.urls import path

from .views import UserRegisterView, AdminRegisterView, LogInView, ResumeView, UserResumeWriteView, ResumeDetailWriteView, ResumeDetailView

urlpatterns = [
	path('userregister', UserRegisterView.as_view()),
	path('adminregister', AdminRegisterView.as_view()),
	path('login', LogInView.as_view()),
        path('resume', ResumeView.as_view()),
        path('resume/<str:main_resume_id>', UserResumeWriteView.as_view()),
        path('resumeDetailWrite/<str:main_resume_id>', ResumeDetailWriteView.as_view()),
        path('resumeDetail/<str:main_resume_id>', ResumeDetailView.as_view()),
]
