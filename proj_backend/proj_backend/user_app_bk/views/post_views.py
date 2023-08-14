from datetime import datetime
from datetime import timedelta

from django.shortcuts import render 
# from rest_framework.response import response
# from rest_framework.deuser_appators import api_view
from django.http import HttpResponse

from ..models import post
from ..serializers import PostSerializer

# # @api_view(["POST"]) 
# def getAllPost(seft, code = None): 
#     # return response()
#     # return HttpResponse("Hello, world. You're at the polls index, aaaaa.")
#     try:
#         queryset = post.objects.get(emp_code=code)
#         serializer = PostSerializer(queryset)
#         return serializer.data
#     except:
#         return None