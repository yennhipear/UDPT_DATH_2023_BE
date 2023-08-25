from datetime import datetime
from datetime import timedelta

from django.shortcuts import render 
from rest_framework.response import Response

from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse

from ..models.post import Post
from ..models.comment import Comment

from ..serializers.post_serializer import PostSerializer
from ..serializers.comment_serializers import CommentSerializer

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db import connection
from django.http import JsonResponse
import json

from .post_views import CustomPagination


class CommentListViewInOnePost(ViewSet):
    pagination_class = PageNumberPagination

    def get(self, request):
        if self.request.query_params.get('postID'):  #lấy id của post
            post_id = self.request.query_params.get('postID')
            comments = Comment.objects.raw('SELECT a.* FROM "Comment" a join "Posts_Comments" b on a."ID" = b."Comment_id" WHERE b."Post_id" = %s', [post_id] ) 
        else:  
            comments = Comment.objects.raw('SELECT a.* FROM "Comment" a join "Posts_Comments" b on a."ID" = b."Comment_id" ')
            
        if self.request.query_params.get('pageSize') is not None: # nếu là 0 thì lấy mặc định trong setting là 1000000 
            PageNumberPagination.page_size = self.request.query_params.get('pageSize', 1000000)  # Lấy giá trị tham số truy vấn, mặc định là 1000000
        paginator = CustomPagination()
        page = paginator.paginate_queryset(comments, request, view=self)  # Thực hiện phân trang với số lượng phần tử trên mỗi trang được truyền vào
        
        serializer = CommentSerializer(page, many=True)
        return Response(serializer.data)


    def post(self, request):
        data = json.loads(request.body)
        postID = data['PostID']
        serializer = CommentSerializer(data=request.data)
        # author = data['UserAccountID']
        # serializer = CommentSerializer(data=request.data)
        # print(data)
        if serializer.is_valid():
            serializer.save()
            commentID = serializer.data['ID']
            print (serializer.data)
            # print (serializer.data['ID'])
            # print (serializer.data['TagID'])
            print(postID)
            with connection.cursor() as cursor:
                cursor.execute('insert into "Posts_Comments" ("Post_id", "Comment_id") values(%s,%s) ' , (postID, commentID))
            
            # newPost = Post.objects.prefetch_related('TagID').get(ID = postID)
            # serializer2 = PostSerializer(newPost, many=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def likeComment(self, request , format=None):
        commentID = self.request.query_params.get('commentID')
        userID = self.request.query_params.get('userID', '')
        like = self.request.query_params.get('Like')  
        if like is not None: 
            with connection.cursor() as cursor:
                # cursor.execute('if not exists(select 1 from "user_like" where "user_id" = %s and "comment_id" = %s) then insert into "user_like"("user_id", "post_id", "comment_id" , "like", "createdDate") values(%s, null, %s, %s, now() ); else  UPDATE "user_like" SET "like" = %s where "user_id" = %s and comment_id = %s; end if;' , (userID, commentID, userID, commentID, like, like, userID, commentID)   )
                cursor.execute('UPDATE "Comment" SET "Like" = "Like" + %s where "ID" = %s  and not exists (select 1 from "user_like" where "user_id" = %s and "comment_id" = %s and "like" = %s ) ' , (like, commentID, userID, commentID, like)   )
                
                cursor.execute('delete  FROM "user_like" where "user_id" = %s and "comment_id" = %s  ' , (userID, commentID))
                cursor.execute('insert into "user_like"("user_id", "comment_id" , "like", "createdDate") values(%s, %s, %s, now() ) ' , (userID, commentID, like))

                
                
        comment = Comment.objects.get(ID = commentID)
        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data)

        
        

