from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models.user import User

# khai báo các hàm thao tác với dữ liệu 
class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
