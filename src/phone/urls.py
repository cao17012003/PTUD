from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('phones', views.ListCreatePhoneView.as_view()),
    path('phones/<str:name>', views.UpdateDeletePhoneView.as_view()),
    path('users', views.ListUserView.as_view()),
]