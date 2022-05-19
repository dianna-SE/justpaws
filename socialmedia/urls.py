from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render

from vue_app import views as vue_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vue_views.index, name='index'),
    path('profile', vue_views.profile, name="profile"),
]

