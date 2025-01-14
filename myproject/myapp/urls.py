
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   
    path("home/", views.home,name="home"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup,name="signup"),
    path("recommendations/", views.recommendations,name="recommendations"),
    # path("", views,name="home")
]
