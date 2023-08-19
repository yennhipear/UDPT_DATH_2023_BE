from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models.tag import Tag

# khai báo các hàm thao tác với dữ liệu 
class TagSerializer(ModelSerializer):
    TagId = serializers.IntegerField(source="ID")
    Name = serializers.CharField(source="Name")
    

    class Meta:
        model = Tag
        fields = "__all__"
