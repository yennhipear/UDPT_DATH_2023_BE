from datetime import datetime
from datetime import timedelta

from django.shortcuts import render 
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse

from ..models.post import Post
from ..models.comment import Comment

from ..serializers.post_serializer import PostSerializer
from ..serializers.comment_serializers import CommentSerializer

from rest_framework.views import APIView


class CommentListViewInOnePost(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        if self.request.query_params.get('postID'):  #lấy id của post
            post_id = self.request.query_params.get('postID')
            comments = Comment.objects.raw('SELECT a.* FROM "Comment" a join "Posts_Comments" b on a."ID" = b."Comment_id" WHERE b."Post_id" = %s', [post_id] ) 
        else:  
            comments = Comment.objects.raw('SELECT a.* FROM "Comment" a join "Posts_Comments" b on a."ID" = b."Comment_id" ') 
            
        if self.request.query_params.get('pageSize') != "0": # nếu là 0 thì lấy mặc định trong setting là 10 
            PageNumberPagination.page_size = self.request.query_params.get('pageSize', 10)  # Lấy giá trị tham số truy vấn, mặc định là 10
        page = self.pagination_class().paginate_queryset(comments, request, view=self)  # Thực hiện phân trang với số lượng phần tử trên mỗi trang được truyền vào
        
        serializer = CommentSerializer(page, many=True)
        return Response(serializer.data)
        

