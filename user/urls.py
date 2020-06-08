from django.urls import path

from .views import UserEmailExists, UserRegisterView, AdminRegisterView, ResumeView, \
         LogInView, UserResumeWriteView, ResumeDetailWriteView, \
         ResumeDetailView, CareerResultView, ResumeMainView, \
         AdminExists, Profile, LikedCompanies, UserMatchUpView, UserBookmark

urlpatterns = [
	path('/exists', UserEmailExists.as_view()),
	path('/admin/exists', AdminExists.as_view()),
    path('/register', UserRegisterView.as_view()),
	path('/adminregister', AdminRegisterView.as_view()),
	path('/login', LogInView.as_view()),
    path('/profile', Profile.as_view()),
    path('/likes', LikedCompanies.as_view()),
    path('/resume', ResumeView.as_view()),
    path('/resume/<str:main_resume_id>', UserResumeWriteView.as_view()),
    path('/resumeDetailWrite/<str:main_resume_id>', ResumeDetailWriteView.as_view()),
    path('/resumeDetail/<str:main_resume_id>', ResumeDetailView.as_view()),
    path('/resumeResult/<str:main_career_id>', CareerResultView.as_view()),
    path('/resumeMain', ResumeMainView.as_view()),
    path('/specList', UserMatchUpView.as_view()),
    # path('/requests', CompanyRequestsResume.as_view()),
    # path('/proposals', CompanyInterviewResume.as_view()),
    path('/requests', CompanyRequestsResume.as_view()),
    path('/proposals', CompanyInterviewResume.as_view()),
    path('/bookmark', UserBookmark.as_view())
]
