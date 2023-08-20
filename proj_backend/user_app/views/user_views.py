from datetime import datetime
from datetime import timedelta

from django.shortcuts import render 
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import generics
from django.http import HttpResponse
from rest_framework.views import APIView

from ..models.user import User
from ..serializers.user_serializers import UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

@api_view(["GET"]) 
def getAllUser(seft, pageSize = 3, pageNo = 1): 
    userList = User.objects.all()
    serializer = UserSerializer(userList, many =True) #mean multiple object 
    return Response(serializer.data)
    # return HttpResponse( pageNo)

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000

# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 5
#     page_size_query_param = 'page_size'
#     max_page_size = 1000

class UserListView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):

        if self.request.query_params.get('pageSize') != "0": # nếu là 0 thì lấy mặc định trong setting là 10 
            PageNumberPagination.page_size = self.request.query_params.get('pageSize', 10)  # Lấy giá trị tham số truy vấn, mặc định là 10
        
        users = User.objects.all()
        page = self.pagination_class().paginate_queryset(users, request, view=self)  # Thực hiện phân trang với số lượng phần tử trên mỗi trang được truyền vào
        
        serializer = UserSerializer(page, many=True)
        return Response(serializer.data)
        # return PageNumberPagination.get_paginated_response(PageNumberPagination, serializer.data)