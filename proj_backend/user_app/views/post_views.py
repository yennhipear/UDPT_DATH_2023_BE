from datetime import datetime
from datetime import timedelta

from django.shortcuts import render 
from rest_framework.response import Response

from rest_framework.decorators import api_view
# from rest_framework.deuser_appators import api_view
from django.http import HttpResponse

from ..models.post import Post
from ..serializers.post_serializer import PostSerializer

@api_view(["GET"]) 
def getAllPost(seft, code = None): 
    # return response()
    # return HttpResponse("You are at the main page where display all posts.", )
    
    latest_post_list = Post.objects.all()

    # latest_post_list = Post.objects.prefetch_related('TagID')
    
    # latest_post_list = Post.objects.select_related().all()
    serializer = PostSerializer(latest_post_list, many =True) #mean multiple object 
    return Response(serializer.data)
    # try:
    #     queryset = post.objects.get(emp_code=code)
    #     serializer = PostSerializer(queryset)
    #     return serializer.data
    # except:
    #     return None

@api_view(["GET"]) 
def getDetailPost(request, post_id):
    # return HttpResponse("You're looking at post %s." % post_id)
    latest_post_list = Post.objects.get(ID = post_id)
    serializer = PostSerializer(latest_post_list, many = False) #mean single object 
    return Response(serializer.data)

