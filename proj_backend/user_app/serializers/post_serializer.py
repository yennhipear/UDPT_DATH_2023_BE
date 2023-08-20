from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models.post import Post
from .tag_serializers import TagSerializer
from ..models.tag import Tag

# khai báo các hàm thao tác với dữ liệu 
class PostSerializer(ModelSerializer):

    TagID = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'
