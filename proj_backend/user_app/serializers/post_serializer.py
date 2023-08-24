from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models.post import Post
from .tag_serializers import TagSerializer
from .comment_serializers import CommentSerializer
from .user_serializers import UserSerializer

from ..models.tag import Tag

# khai báo các hàm thao tác với dữ liệu 
class PostSerializer(ModelSerializer):  # sau mỗi field không có dấu phẩy  
    TagID = TagSerializer(many=True, read_only=True)
    CommentID = CommentSerializer(many=True, read_only=True)
    UserAccountID = UserSerializer(many=False, read_only=True)
    # Author = serializers.IntegerField(source="UserAccountID")

    class Meta:
        model = Post
        fields = '__all__'
