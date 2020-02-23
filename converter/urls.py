from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.personal_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('mainpage/', views.index, name='mainpage'),
    path('searchprofile/<str:user>', views.searchprofile, name='searchprofile'),
    path('follow/<str:username>', views.follow, name="follow")
]
