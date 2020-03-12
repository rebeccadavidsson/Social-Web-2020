from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.personal_view, name='profile'),
    path('settings/<int:pk>/', views.settings_view, name='settings'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('mainpage/', views.index, name='mainpage'),
    path('searchprofile/<str:user>', views.searchprofile, name='searchprofile'),
    path('follow/<str:username>', views.follow, name="follow"),
    path('unfollow/<str:username>', views.unfollow, name="unfollow"),
    path("addschedule", views.addschedule, name="addschedule"),
    path("add/<int:event_id>", views.add, name="add"),
    path("review.<int:event_id>", views.review, name="review"),
    path("delete_profile/<str:username>", views.delete_profile, name="delete"),
    path("comment", views.comment, name="comment"),
    path("deleteevent/<int:event_id>", views.deleteevent, name="delete"),
    path("schedule2", views.schedule2, name="schedule2"),
    path("delete_rating/<int:pk>", views.delete_rating, name="delete_rating"),
    path("like/<int:event_id>", views.like, name="like"),
    path("heart/<int:event_id>", views.heart, name="heart"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
