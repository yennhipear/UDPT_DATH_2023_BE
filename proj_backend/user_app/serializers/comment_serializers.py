from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from ..serializers.tag_serializers import TagSerializer
from ..serializers.user_serializers import UserSerializer
from ..models.comment import Comment
from ..models.tag import Tag

# khai báo các hàm thao tác với dữ liệu 
class CommentSerializer(ModelSerializer):

    UserAccountID = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'


   # ChildComment = serializers.SerializerMethodField(
    #     read_only=True, method_name="get_child_comments")
    
    # def get_child_comments(self, obj):
    #     # """ self referral field """
    #     childComments = Tag.objects.raw('SELECT a.* FROM "Tag" a where "ID" = "" ') 
    #     serializer = TagSerializer(
    #         childComments,
    #         many=True
    #     )
    #     return (serializer.data)