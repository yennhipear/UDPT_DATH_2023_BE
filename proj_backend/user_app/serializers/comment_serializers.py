from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models.comment import Comment

# khai báo các hàm thao tác với dữ liệu 
class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
