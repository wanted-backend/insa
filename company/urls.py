from django.urls import path

from .views import *

urlpatterns = [
	path('companyregister', CompanyRegister.as_view()),
    path('/themetop/<int:theme_id>',ThemeTop.as_view()),
    path('/themelist/<int:theme_id>',ThemeList.as_view()),
]
