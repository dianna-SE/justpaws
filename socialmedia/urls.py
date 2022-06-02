from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

from vue_app import views as vue_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vue_views.index, name='index'),
    path('settings', vue_views.settings, name='settings'),
    path('upload', vue_views.upload, name='upload'),
    path('like-post', vue_views.like_post, name='like-post'),
    path('follow', vue_views.follow, name='follow'),
    path('search', vue_views.search, name='search'),
    path('profile/<str:pk>', vue_views.profile, name="profile"),
    path('login', vue_views.login, name='login'),
    path('logout', vue_views.logout, name='logout'),
    path('register', vue_views.register, name='register'),
    path('messages', vue_views.message, name='messages'),
]

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, 
    document_root = settings.MEDIA_ROOT
)

