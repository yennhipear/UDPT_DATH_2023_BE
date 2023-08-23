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

from .views.user_views import *
from .views.post_views import *
from .views.tag_views import *
from .views.comment_views import CommentListViewInOnePost


urlpatterns = [
    # path("admin/", admin.site.urls),
    # api for post 
    # get all : http://127.0.0.1:8000/user-app/posts/
    # get by id : http://127.0.0.1:8000/user-app/posts/?postID=3
    path("posts/all", PostListView.as_view({'get': 'getAllPost'})),
    path("posts/byID", PostListView.as_view({'get': 'getPostByID'})),
    path("posts/pagi", PostListView.as_view({'get': 'getPostPagination'})),
    path("posts/updateStatus", PostListView.as_view({'post': 'PostUpdateStatus'})), #update status in many post: http://127.0.0.1:8000/user-app/posts/updateStatus?postIDs=1,2,3&status=1 - status = 1 là duyệt, -1 là cancel, 0 là đang chờ duyệt 
    path("posts/insertPost", PostListView.as_view({'post': 'post'})),  
    path("posts/updatedataapi", update_data_api , name='update-data-api'),   



    # api for tag 
    # get all : http://127.0.0.1:8000/user-app/tags/
    # get by id : http://127.0.0.1:8000/user-app/tags/?tagID=3
    path("tags/all", TagListView.as_view({'get': 'getAllTag'})),
    path("tags/byID", TagListView.as_view({'get': 'getTagByID'})), 
    path("tags/pagi", TagListView.as_view({'get': 'getTagPagination'})), 

    path("tags/createListTags", TagInsert.as_view(), name='tags-insert'),
    
    
    # api for comment
    # get all : http://127.0.0.1:8000/user-app/comments/
    # get by post id : http://127.0.0.1:8000/user-app/comments/?postID=2&pageSize=1&page=2
    path("comments/", CommentListViewInOnePost.as_view(), name='comments'), 

    # api for user 
    path('users/all', UserListView.as_view({'get': 'getAllUser'})),  #example: http://127.0.0.1:8000/user-app/users/all , không có page_size lấy mặc định là 10 
    path('users/pagi', UserListView.as_view({'get': 'getUserPagination'}))  #example: http://127.0.0.1:8000/user-app/users/pagi , không có page_size lấy mặc định là 10 

]