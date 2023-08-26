from django.db import models
from .user import User
# khai báo đối tượng dữ liệu comment 


class Comment(models.Model):
    class Meta:
        db_table = 'Comment'

    ID = models.AutoField(primary_key=True)
    # UserAccountID = models.ForeignKey(User, on_delete=models.CASCADE, db_column = 'UserAccountID')
    UserAccountID =  models.IntegerField()
    PostID = models.IntegerField()
    Content = models.TextField()
    Like =  models.IntegerField()
    Status = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    LastModifiedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Content