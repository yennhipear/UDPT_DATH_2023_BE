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
from rest_framework_simplejwt import views as jwt_views

from rest_framework import generics

from .views.user_views import *
from .views.post_views import *
from .views.tag_views import *
from .views.comment_views import *
from .views.auth_views import *


urlpatterns = [
    # path("admin/", admin.site.urls),
    # api for post 
    # get all : http://127.0.0.1:8000/user-app/posts?Status=1 : là lấy status =1 tương tự với pagi, và tag, user
    # get by id : http://127.0.0.1:8000/user-app/posts/?postID=3
    path("posts/all", PostListView.as_view({'get': 'getAllPost'})),  
    path("posts/byID", PostListView.as_view({'get': 'getPostByID'})),
    path("posts/pagi", PostListView.as_view({'get': 'getPostPagination'})),
    path("posts/searchByTitleContent", PostListView.as_view({'get': 'getPostByTitleContent'})),  # http://127.0.0.1:8000/user-app/posts/searchByTitleContent?keyWord=sau%20khi  order by CreatedDate desc

    path("posts/updateStatus", PostListView.as_view({'get': 'PostUpdateStatus'})), # update status in many post: http://127.0.0.1:8000/user-app/posts/updateStatus?postIDs=1,2,3&status=1 - status = 1 là duyệt, -1 là cancel, 0 là đang chờ duyệt 
    path("posts/post", PostListView.as_view({'post': 'post'})),  
    path("posts/getTotalObject", PostListView.as_view({'get': 'getTotalObject'})),  #Đếm số lượng post, tag, user ở trạng thái 1 :  http://127.0.0.1:8000/user-app/posts/getTotalObject
    path("posts/updateViewLike", PostListView.as_view({'get': 'updateViewLike'})), #update view hoặc like tùy vào parameter, trả về post sau khi update, http://127.0.0.1:8000/user-app/posts/updateViewLike?postID=3&Like=-1&View=1&Answer=1
    path("posts/postTags", PostListView.as_view({'get': 'postTagsToPosts_Tags'})),  # http://127.0.0.1:8000/user-app/posts/postTags?TagIDs=d,b,a,c&postID=6  insert tag và post vào bảng trung gian
    path("posts/searchPostByTagName", PostListView.as_view({'get': 'searchPostByTagName'})), # http://127.0.0.1:8000/user-app/posts/searchPostByTagName?keyWord=jav

    # api for tag 
    # get all : http://127.0.0.1:8000/user-app/tags/
    # get by id : http://127.0.0.1:8000/user-app/tags/?tagID=3
    path("tags/all", TagListView.as_view({'get': 'getAllTag'})),
    path("tags/byID", TagListView.as_view({'get': 'getTagByID'})), 
    path("tags/pagi", TagListView.as_view({'get': 'getTagPagination'})), 
    path("tags/searchByName", TagListView.as_view({'get': 'searchByName'})), # http://127.0.0.1:8000/user-app/tags/searchByName?keyWord=jav  


    path("tags/createTags", TagListView.as_view({'get': 'post'})), # http://127.0.0.1:8000/user-app/tags/createTags?Names=p,ja,na
    
    
    # api for comment
    # get all : http://127.0.0.1:8000/user-app/comments/
    # get by post id : http://127.0.0.1:8000/user-app/comments/?postID=2&pageSize=1&page=2
    path("comments/", CommentListViewInOnePost.as_view({'get': 'get'})), 
    path("comments/postComment", CommentListViewInOnePost.as_view({'post': 'post'})), 
    # format for comments/postComment
    # {
    #     "UserAccountID": 9,
    #     "PostID": 21,
    #     "Content": "cmt 1 của post 21 xxxx xxx",
    #     "Status": 1,
    #     "CreatedDate": null,
    #     "LastModifiedDate": null
    # }
    path("comments/likeComment", CommentListViewInOnePost.as_view({'get': 'likeComment'})),  # http://127.0.0.1:8000/user-app/comments/likeComment?commentID=1&Like=1

    # api for user 
    path('users/all', UserListView.as_view({'get': 'getAllUser'})),  #example: http://127.0.0.1:8000/user-app/users/all , không có page_size lấy mặc định là 10 
    path('users/pagi', UserListView.as_view({'get': 'getUserPagination'})),  #example: http://127.0.0.1:8000/user-app/users/pagi , không có page_size lấy mặc định là 10 
    path('users/byID', UserListView.as_view({'get': 'getUserByID'})),  #example: http://127.0.0.1:8000/user-app/users/byID?userID=1 , 

    path('users/searchByName', UserListView.as_view({'get': 'searchByDisplayname'})), # http://127.0.0.1:8000/user-app/users/searchByName?keyWord=nhi  order by CreatedDate desc
    path("users/userUpdateStatus", UserListView.as_view({'post': 'UserUpdateStatus'})), # http://127.0.0.1:8000/user-app/users/userUpdateStatus?userIDs=1,2,3&status=1  , status 1 là hoạt động, 0 là bị ban

    #authen
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('users/register', RegisterView.as_view(), name='register'),
    path('users/login', LoginView.as_view(), name='login'),
    path('users/logout', LogoutView.as_view(), name='logout'),
    path('users/view-user', UserView.as_view(), name='user-view'),
    path('users/changePassword', ChangePassWordView.as_view(), name='changePassword'), 
    # {
    
    # "email": "tuan@gmail.com",
    # "password": "kkkkk",
    # "oldPassword": "pbkdf2_sha256$600000$b2QhcIyMv0MsSCAWj79soG$IugcnEYbfBn0g2of25GKOEsh0p+rVlhMMcH0Uo+UqEE="
    
    # }

]