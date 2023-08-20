from django.db import models
from .tag import Tag
# import jsonfield
# khai báo đối tượng dữ liệu post 


class Post(models.Model):
    class Meta:
        db_table = 'Post'

    ID = models.PositiveBigIntegerField(primary_key=True)
    UserAccountID = models.IntegerField()
    Title = models.CharField(max_length=512)
    Content = models.TextField()
    AnswerID = models.CharField(max_length=512)
    TagID = models.ManyToManyField(
        Tag,
        related_name='Posts_title', 
        through='Posts_Tags', 
        through_fields = ('Post', 'Tag')   
    ) # Many-to-Many relationship
    CommentID = models.CharField(max_length=10000)
    Reaction = models.IntegerField()
    Status = models.IntegerField()
    
    CreatedDate = models.DateTimeField(auto_now_add=True)
    LastModifiedDate = models.DateTimeField()
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
