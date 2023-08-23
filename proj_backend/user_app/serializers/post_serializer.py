from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models.post import Post
from .tag_serializers import TagSerializer
from .comment_serializers import CommentSerializer

from ..models.tag import Tag

# khai báo các hàm thao tác với dữ liệu 
class PostSerializer(ModelSerializer):  # sau mỗi field không có dấu phẩy  
    TagID = TagSerializer(many=True, read_only=True)
    CommentID = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = '__all__'
