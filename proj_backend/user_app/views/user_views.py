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

# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 5
#     page_size_query_param = 'page_size'
#     max_page_size = 1000

class UserListView(ViewSet):
    pagination_class = PageNumberPagination

    def getAllUser(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def getUserPagination(self, request):
        # if self.request.query_params.get('pageSize') is not None: # nếu là 0 thì lấy mặc định trong setting là 10 
        PageNumberPagination.page_size = self.request.query_params.get('pageSize', 1000000)  # Lấy giá trị tham số truy vấn, mặc định là 10
        
        users = User.objects.all()
        page = self.pagination_class().paginate_queryset(users, request, view=self)  # Thực hiện phân trang với số lượng phần tử trên mỗi trang được truyền vào
        
        serializer = UserSerializer(page, many=True)
        return Response(serializer.data)
        # return PageNumberPagination.get_paginated_response(PageNumberPagination, serializer.data)