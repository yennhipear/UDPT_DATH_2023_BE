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

from ..models.tag import Tag
from ..serializers.tag_serializers import TagSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


class TagListView(ViewSet):
    pagination_class = PageNumberPagination

    def getAllTag(self, request):
        try:
            tags = Tag.objects.all()
            serializer = TagSerializer(tags, many=True)
                
            return Response(serializer.data)
        except: 
            return Response({'statusCode': 404, 'message': 'data connection not ok'}, status.HTTP_200_OK)

    def getTagByID(self, request):
        try:
            if self.request.query_params.get('tagID'): 
                tagID = self.request.query_params.get('tagID')
                tags = Tag.objects.get(ID= tagID)
                serializer = TagSerializer(tags, many =False) #mean single object 
                return Response(serializer.data)
            else: return Response({'statusCode': 404, 'message': 'Invalid Tag ID'}, status.HTTP_200_OK)
        except: 
            return Response({'statusCode': 404, 'message': 'data connection not ok'}, status.HTTP_200_OK)
    def getTagPagination(self, request):
        try:    
            # if  self.request.query_params.get('pageSize') is not None: # nếu là 0 thì lấy mặc định trong setting 
                # return HttpResponse(self.request.query_params.get('pageSize'))
            PageNumberPagination.page_size = self.request.query_params.get('pageSize', 1000000)  # Lấy giá trị tham số truy vấn, mặc định là 10
            tags = Tag.objects.all()
            page = self.pagination_class().paginate_queryset(tags, request, view=self)  # Thực hiện phân trang với số lượng phần tử trên mỗi trang được truyền vào
            
            serializer = TagSerializer(page, many=True)

            return Response(serializer.data)
        except: 
            return Response({'statusCode': 404, 'message': 'data connection not ok'}, status.HTTP_200_OK)


    def post(self, request):
        # b = Tag(id=10, Title="All the latest Beatles news.")
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagInsert(APIView):
    def post(self, request):
        # b = Tag(id=10, Title="All the latest Beatles news.")
        return Response(1)
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
