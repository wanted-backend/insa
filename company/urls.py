from django.urls import path

from .views import CompanyRegister

urlpatterns = [
	path('companyregister', CompanyRegister.as_view()),
]
