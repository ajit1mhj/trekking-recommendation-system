
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.Custom_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('recommendations/', views.recommendations, name='recommendations'),
]
