from datetime import datetime
from datetime import timedelta

from django.shortcuts import render 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse
from django.db import connection

from ..models.post import Post
from ..models.user import User
from ..models.tag import Tag


from ..serializers.post_serializer import PostSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from django.db.models import Q
from django.db.models import Count

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pageSize'
    max_page_size = 100

class PostListView(ViewSet):

    pagination_class = PageNumberPagination

    def getAllPost(self, request):
        status = self.request.query_params.get('Status') 
        if status is not None:
            print (status)
            posts = Post.objects.prefetch_related('TagID').filter(Status = status)
        else:
            posts = Post.objects.prefetch_related('TagID')  # xài filter thay cho get(), get chỉ lấy được 1 object thôi
        
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def getPostByID(self, request):
        if self.request.query_params.get('postID'):  #lấy 1 post
            posts = Post.objects.prefetch_related('TagID').get(ID = self.request.query_params.get('postID'))
            serializer = PostSerializer(posts, many=False)
            return Response(serializer.data)
        else: return Response({'statusCode': 404, 'message': 'Invalid Tag ID'}, status.HTTP_200_OK)
        
    def getPostPagination(self, request):
             
        # if self.request.query_params.get('pageSize') is not None: # nếu là 0 thì lấy mặc định trong setting là 10 
        PageNumberPagination.page_size = self.request.query_params.get('pageSize', 1000000)  # Lấy giá trị tham số truy vấn, mặc định là 10
        paginator = CustomPagination()
        
        status = self.request.query_params.get('Status') 
        if status is not None:
            print (status)
            posts = Post.objects.prefetch_related('TagID').filter(Status = status) 
        else:
            posts = Post.objects.prefetch_related('TagID')  # xài filter thay cho get(), get chỉ lấy được 1 object thôi
        
        page = paginator.paginate_queryset(posts, request, view=self)  # Thực hiện phân trang với số lượng phần tử trên mỗi trang được truyền vào
        
        serializer = PostSerializer(page, many=True)

        data = {
                    'totalPage': paginator.page.paginator.num_pages,
                    'currentPage': paginator.page.number,
                    'data': serializer.data
                }

        return Response(data)
        # return PageNumberPagination.get_paginated_response(PageNumberPagination, serializer.data)

    def getPostByTitleContent(self, request):
        PageNumberPagination.page_size = self.request.query_params.get('pageSize', 1000000)  # Lấy giá trị tham số truy vấn, mặc định là 10
        paginator = CustomPagination()
        
        keyWord = self.request.query_params.get('keyWord')
        posts = Post.objects.prefetch_related('TagID').filter( Q(Title__icontains = keyWord) | Q(Content__icontains = keyWord))
        
        page = paginator.paginate_queryset(posts, request, view=self)
        serializer = PostSerializer(page, many=True)

        data = {
                    'totalPage': paginator.page.paginator.num_pages,
                    'currentPage': paginator.page.number,
                    'data': serializer.data
                }

        return Response(data)

    def post(self, request):
        self.http_method_names.append("GET")
        b = Post(ID=10, Title="All the latest Beatles news.")

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print (serializer.data['ID'])
            # print (serializer.data['TagID'])
            # print (serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # serializer = PostSerializer(b, many=False)
        # return Response(11)
    def PostUpdateStatus(self, request , format=None):
        postIDs = self.request.query_params.get('postIDs')
        status = self.request.query_params.get('status')

        with connection.cursor() as cursor:
            # cursor.execute('UPDATE "Post" SET "Status" = %s WHERE "ID" = %s', [status], [postIDs] )
            cursor.execute('UPDATE "Post" SET "Status" = %s where "ID" in (SELECT unnest(string_to_array(%s, '','')) as id  )' , (status, postIDs))
            row = cursor.fetchone()
        return Response({'statusCode': 200, 'message': 'data connection ok'}, status.HTTP_200_OK)
    
    def updateViewLike(self, request , format=None):
        postID = self.request.query_params.get('postID')
        like = self.request.query_params.get('Like')
        view = self.request.query_params.get('View')
        if like is not None or view is not None: 
            with connection.cursor() as cursor:
                if like is not None:
                    cursor.execute('UPDATE "Post" SET "Like" = "Like" + %s where "ID" = %s  ' , (like, postID)   )
                if view is not None:
                    cursor.execute('UPDATE "Post" SET "View" = "View" + 1 where "ID" = %s  ' ,  [postID]  )
                
        posts = Post.objects.prefetch_related('TagID').get(ID = self.request.query_params.get('postID'))
        serializer = PostSerializer(posts, many=False)
        return Response(serializer.data)

    def getTotalObject(self, request):
        posts = Post.objects.filter(Status=1).count()
        users = User.objects.filter(Status=1).count()
        tags = Tag.objects.filter(Status=1).count()

        data = {
                    'totalPost': posts,
                    'totalTag': tags,
                    'totalUser': users
                }
        return Response(data)