from datetime import datetime
from datetime import timedelta

from django.shortcuts import render 
from rest_framework.response import response
from rest_framework.decorators import api_view
# from rest_framework.deuser_appators import api_view
from django.http import HttpResponse

from ..models.post import Post
# from ..serializers import PostSerializer

#  @api_view(["GET"]) 
def getAllPost(seft, code = None): 
    # return response()
    # return HttpResponse("You are at the main page where display all posts.", )
    latest_post_list = Post.objects.order_by("ID")
    output = ", ".join([q.Content for q in latest_post_list])
    return HttpResponse(output)
    # try:
    #     queryset = post.objects.get(emp_code=code)
    #     serializer = PostSerializer(queryset)
    #     return serializer.data
    # except:
    #     return None

def getDetailPost(request, post_id):
    return HttpResponse("You're looking at post %s." % post_id)
