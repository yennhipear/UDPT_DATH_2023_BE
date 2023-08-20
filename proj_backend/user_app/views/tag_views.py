from datetime import datetime
from datetime import timedelta

from django.shortcuts import render 
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework import generics
from django.http import HttpResponse
from rest_framework.views import APIView

from ..models.tag import Tag
from ..serializers.tag_serializers import TagSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


class TagListView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        if self.request.query_params.get('tagID'): 
            tagID = self.request.query_params.get('tagID')
            tags = Tag.objects.get(ID= tagID)
            serializer = TagSerializer(tags, many =False) #mean single object 
            # return Response(serializer.data)
        else: 
            if self.request.query_params.get('pageSize') != "0": # nếu là 0 thì lấy mặc định trong setting là 10 
                PageNumberPagination.page_size = self.request.query_params.get('pageSize', 10)  # Lấy giá trị tham số truy vấn, mặc định là 10
            
            tags = Tag.objects.all()
            page = self.pagination_class().paginate_queryset(tags, request, view=self)  # Thực hiện phân trang với số lượng phần tử trên mỗi trang được truyền vào
            
            serializer = TagSerializer(page, many=True)
            
        return Response(serializer.data)
            # return PageNumberPagination.get_paginated_response(PageNumberPagination, serializer.data)

