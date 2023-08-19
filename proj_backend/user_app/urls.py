"""
URL configuration for proj_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework import generics

from .views import post_views
from .views.user_views import UserListView

urlpatterns = [
    # path("admin/", admin.site.urls),
    # Lấy tất cả bài post
    path("all-posts/", post_views.getAllPost, name='posts'),
    path("post/<int:post_id>/", post_views.getDetailPost, name='detail'),

    # api for user 
    path('users/', UserListView.as_view(), name='user-list')  #example: http://127.0.0.1:8000/user-app/users/?page_size=4&page=2 , không có page_size lấy mặc định là 10 
]

