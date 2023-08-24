from datetime import datetime
from datetime import timedelta

from django.shortcuts import render 
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import generics
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet


from ..models.user import User
from ..serializers.user_serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .post_views import CustomPagination


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 5
#     page_size_query_param = 'page_size'
#     max_page_size = 1000

class UserListView(ViewSet):
    pagination_class = PageNumberPagination

    def getAllUser(self, request):
        status = self.request.query_params.get('Status') 
        if status is not None:
            users = User.objects.filter(Status = status) # xài filter thay cho get(), get chỉ lấy được 1 object thôi
        else:
            users = User.objects.all() 
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def getTagByID(self, request):
        try:
            if self.request.query_params.get('userID'): 
                userID = self.request.query_params.get('userID')
                users = User.objects.get(ID= userID)
                serializer = UserSerializer(tags, many = False) #mean single object 
                return Response(serializer.data)
            else: return Response({'statusCode': 404, 'message': 'Invalid User ID'}, status.HTTP_200_OK)
        except: 
            return Response({'statusCode': 404, 'message': 'data connection not ok'}, status.HTTP_200_OK)
    
    def getUserPagination(self, request):
        # if self.request.query_params.get('pageSize') is not None: # nếu là 0 thì lấy mặc định trong setting là 10 
        PageNumberPagination.page_size = self.request.query_params.get('pageSize', 1000000)  # Lấy giá trị tham số truy vấn, mặc định là 10
        
        status = self.request.query_params.get('Status') 
        if status is not None:
            users = User.objects.filter(Status = status)
        else:
            users = User.objects.all() 
        
        paginator = CustomPagination()
        page = paginator.paginate_queryset(users, request, view=self)  # Thực hiện phân trang với số lượng phần tử trên mỗi trang được truyền vào
    
        serializer = UserSerializer(page, many=True)

        data = {
                    'totalPage': paginator.page.paginator.num_pages,
                    'currentPage': paginator.page.number,
                    'data': serializer.data
                }
        
        return Response(data)
        
    def searchByDisplayname(self, request):
        # if self.request.query_params.get('pageSize') is not None: # nếu là 0 thì lấy mặc định trong setting là 10 
        PageNumberPagination.page_size = self.request.query_params.get('pageSize', 1000000)  # Lấy giá trị tham số truy vấn, mặc định là 10
        
        paginator = CustomPagination()
        keyWord = self.request.query_params.get('keyWord') 
        users = User.objects.filter(DisplayName__icontains = keyWord).order_by("-CreatedDate")
        
        page = paginator.paginate_queryset(users, request, view=self)  # Thực hiện phân trang với số lượng phần tử trên mỗi trang được truyền vào
    
        serializer = UserSerializer(page, many=True)

        data = {
                    'totalPage': paginator.page.paginator.num_pages,
                    'currentPage': paginator.page.number,
                    'data': serializer.data
                }
        return Response(data)
        # return PageNumberPagination.get_paginated_response(PageNumberPagination, serializer.data)
    
    def UserUpdateStatus(self, request):
        userIDs = self.request.query_params.get('userIDs')
        status = self.request.query_params.get('status')

        with connection.cursor() as cursor:
            # cursor.execute('UPDATE "Post" SET "Status" = %s WHERE "ID" = %s', [status], [postIDs] )
            cursor.execute('UPDATE "User" SET "Status" = %s where "ID" in (SELECT unnest(string_to_array(%s, '','')) as id  )' , (status, userIDs))
            row = cursor.fetchone()
        return Response({'statusCode': 200, 'message': 'data connection ok'}, status.HTTP_200_OK)
    
    