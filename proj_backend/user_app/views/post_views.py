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
from ..serializers.post_serializer import PostSerializer
from rest_framework.views import APIView

class PostListView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        if self.request.query_params.get('postID'):  #lấy 1 post
            posts = Post.objects.prefetch_related('TagID').get(ID = self.request.query_params.get('postID'))
            
            serializer = PostSerializer(posts, many=False)
            
        else:     
            if self.request.query_params.get('pageSize') != "0": # nếu là 0 thì lấy mặc định trong setting là 10 
                PageNumberPagination.page_size = self.request.query_params.get('pageSize', 10)  # Lấy giá trị tham số truy vấn, mặc định là 10
            
            posts = Post.objects.prefetch_related('TagID')
            page = self.pagination_class().paginate_queryset(posts, request, view=self)  # Thực hiện phân trang với số lượng phần tử trên mỗi trang được truyền vào
            
            serializer = PostSerializer(page, many=True)
        return Response(serializer.data)
            # return PageNumberPagination.get_paginated_response(PageNumberPagination, serializer.data)
    def post(self, request):
        b = Post(ID=10, Title="All the latest Beatles news.")

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # serializer = PostSerializer(b, many=False)
        # return Response(11)



# class PostUpdateStatus(APIView):
#     def post(self, request):
        
#         postIDs = self.request.query_params.get('postIDs')
#         status = self.request.query_params.get('status')

#         with connection.cursor() as cursor:
#             cursor.execute('UPDATE "Post" SET "Status" = %s WHERE "ID" = %s', [status], [postIDs] )
#             row = cursor.fetchone()
#         return Response({'statusCode': 200, 'message': 'data connection ok'}, status.HTTP_200_OK)

@api_view(['PUT'])
def PostUpdateStatus(self, request):
    
    postIDs = self.request.query_params.get('postIDs')
    status = self.request.query_params.get('status')

    with connection.cursor() as cursor:
        cursor.execute('UPDATE "Post" SET "Status" = %s WHERE "ID" = %s', [status], [postIDs] )
        row = cursor.fetchone()
    return Response({'statusCode': 200, 'message': 'data connection ok'}, status.HTTP_200_OK)



@api_view(["GET"]) 
def getDetailPost(request, post_id):
    # return HttpResponse("You're looking at post %s." % post_id)
    latest_post_list = Post.objects.get(ID = post_id)
    serializer = PostSerializer(latest_post_list, many = False) #mean single object 
    return Response(serializer.data)

