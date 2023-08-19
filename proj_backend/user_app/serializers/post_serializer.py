from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models.post import Post
from .tag_serializers import TagSerializer
from ..models.tag import Tag

# khai báo các hàm thao tác với dữ liệu 
class PostSerializer(ModelSerializer):
    # postId = serializers.IntegerField(source="ID")
    # title = serializers.CharField(source="Title")
    # content = serializers.CharField(source="Content")
    # Tagsinpost = serializers.CharField(source="TagID")
    
    # Tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Post
        fields = '__all__'
