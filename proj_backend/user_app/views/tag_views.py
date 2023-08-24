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
from django.db import connection

from ..models.tag import Tag
from ..serializers.tag_serializers import TagSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .post_views import CustomPagination


class TagListView(ViewSet):
    pagination_class = PageNumberPagination

    def getAllTag(self, request):
        try:
            status = self.request.query_params.get('Status') 
            if status is not None:
                tags = Tag.objects.filter(Status = status) # xài filter thay cho get(), get chỉ lấy được 1 object thôi
            else:
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
            paginator = CustomPagination()

            status = self.request.query_params.get('Status') 
            if status is not None:
                tags = Tag.objects.filter(Status = status) # xài filter thay cho get(), get chỉ lấy được 1 object thôi
            else:
                tags = Tag.objects.all() 

            page = paginator.paginate_queryset(tags, request, view=self)  # Thực hiện phân trang với số lượng phần tử trên mỗi trang được truyền vào
            
            serializer = TagSerializer(page, many=True)

            data = {
                    'totalPage': paginator.page.paginator.num_pages,
                    'currentPage': paginator.page.number,
                    'data': serializer.data
                }

            return Response(data)
        except: 
            return Response({'statusCode': 404, 'message': 'data connection not ok'}, status.HTTP_200_OK)


    def post(self, request):
        # b = Tag(id=10, Title="All the latest Beatles news.")
        names = self.request.query_params.get('Names')
        commaChar = ','
        with connection.cursor() as cursor:
            # cursor.execute('UPDATE "Post" SET "Status" = %s WHERE "ID" = %s', [status], [postIDs] )
            cursor.execute('insert into  "Tag" ("Name", "Status") select list.name, 1 from (SELECT unnest(string_to_array(%s, %s)) as name) List left join "Tag" b on list.name = b."Name" where b."ID" IS NULL ' , (names, commaChar))
            
        tags = Tag.objects.raw('SELECT b.* from (SELECT unnest(string_to_array(%s, %s)) as name) List left join "Tag" b on list.name = b."Name" ', (names, commaChar))
        serializer = TagSerializer(tags, many =True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

