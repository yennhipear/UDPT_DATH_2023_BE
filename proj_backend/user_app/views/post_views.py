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
from rest_framework.viewsets import ViewSet

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pageSize'
    max_page_size = 100

class PostListView(ViewSet):

    pagination_class = PageNumberPagination

    def getAllPost(self, request):

        posts = Post.objects.prefetch_related('TagID')
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
        posts = Post.objects.prefetch_related('TagID')
        page = paginator.paginate_queryset(posts, request, view=self)  # Thực hiện phân trang với số lượng phần tử trên mỗi trang được truyền vào
        
        serializer = PostSerializer(page, many=True)

        data = {
                    'totalPage': paginator.page.paginator.num_pages,
                    'currentPage': paginator.page.number,
                    'data': serializer.data
                }

        return Response(data)
        # return PageNumberPagination.get_paginated_response(PageNumberPagination, serializer.data)

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
            cursor.execute('UPDATE "Post" SET "Status" = %s where "ID" in (SELECT unnest(string_to_array(%s, '','')) as id  )' , [status],  [postIDs]  )
            row = cursor.fetchone()
        return Response({'statusCode': 200, 'message': 'data connection ok'}, status.HTTP_200_OK)

@api_view(['POST'])
def update_data_api(request):
    # Xử lý dữ liệu request.data và thực hiện truy vấn cập nhật vào cơ sở dữ liệu
    return Response({"message": "Dữ liệu đã được cập nhật"})

# class PostUpdateStatus(APIView):
#     def post(self, request):
        
#         postIDs = self.request.query_params.get('postIDs')
#         status = self.request.query_params.get('status')

#         with connection.cursor() as cursor:
#             cursor.execute('UPDATE "Post" SET "Status" = %s WHERE "ID" = %s', [status], [postIDs] )
#             row = cursor.fetchone()
#         return Response({'statusCode': 200, 'message': 'data connection ok'}, status.HTTP_200_OK)

# @api_view(['PUT'])
# def PostUpdateStatus(self, request):
    
#     postIDs = self.request.query_params.get('postIDs')
#     status = self.request.query_params.get('status')

#     with connection.cursor() as cursor:
#         cursor.execute('UPDATE "Post" SET "Status" = %s WHERE "ID" = %s', [status], [postIDs] )
#         row = cursor.fetchone()
#     return Response({'statusCode': 200, 'message': 'data connection ok'}, status.HTTP_200_OK)



# @api_view(["GET"]) 
# def getDetailPost(request, post_id):
#     # return HttpResponse("You're looking at post %s." % post_id)
#     latest_post_list = Post.objects.get(ID = post_id)
#     serializer = PostSerializer(latest_post_list, many = False) #mean single object 
#     return Response(serializer.data)

