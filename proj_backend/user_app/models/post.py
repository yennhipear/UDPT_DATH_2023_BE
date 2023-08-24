from django.db import models
from .tag import Tag
from .comment import Comment
from .user import User
# import jsonfield
# khai báo đối tượng dữ liệu post 


class Post(models.Model): # sau mỗi field không có dấu phẩy  
    class Meta:
        db_table = 'Post'

    ID = models.AutoField(primary_key=True)
    UserAccountID = models.ForeignKey(User, on_delete=models.CASCADE, db_column = 'UserAccountID')
    Title = models.CharField(max_length=512)
    Content = models.TextField()
    # AnswerID = models.CharField(max_length=512)
    TagID = models.ManyToManyField(
        Tag,
        related_name='Posts_Title', 
        through='Posts_Tags', 
        through_fields = ('Post', 'Tag')
    ) # Many-to-Many relationship
    CommentID = models.ManyToManyField(
        Comment,
        related_name='Posts_Comment', 
        through='Posts_Comments', 
        through_fields = ('Post', 'Comment')
    )

    totalAnswer = models.IntegerField()

    Like = models.IntegerField()
    # DisLike = models.IntegerField()
    View = models.IntegerField()
    Status = models.IntegerField()
    
    CreatedDate = models.DateTimeField(auto_now_add=True)
    LastModifiedDate = models.DateTimeField(auto_now_add=True)
    LastModifiedBy = models.IntegerField()
    

    def __str__(self):
        return self.Title

class Posts_Tags(models.Model):
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    Tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Posts_Tags'
        constraints = [
            models.UniqueConstraint(
                fields=('Post', 'Tag'),
                name='unique_Post_Tag'
            )
        ]

class Posts_Comments(models.Model):
    Post = models.ForeignKey(Post, on_delete=models.CASCADE)
    Comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Posts_Comments'
        constraints = [
            models.UniqueConstraint(
                fields=('Post', 'Comment'),
                name='unique_Post_Comment'
            )
        ]
