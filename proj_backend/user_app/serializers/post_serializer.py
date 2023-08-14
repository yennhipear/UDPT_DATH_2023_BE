from ..models import Post
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

# khai báo các hàm thao tác với dữ liệu 
class PostSerializer(ModelSerializer):
    postId = serializers.IntegerField(source="ID")
    title = serializers.CharField(source="title")
    content = serializers.CharField(source="content")
    

    class Meta:
        model = Post
        fields = "__all__"
