from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models.tag import Tag

# khai báo các hàm thao tác với dữ liệu 
class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"
