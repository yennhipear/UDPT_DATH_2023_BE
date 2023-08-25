from django.db import models

# khai báo đối tượng dữ liệu comment 


class Comment(models.Model):
    class Meta:
        db_table = 'Comment'

    ID = models.AutoField(primary_key=True)
    UserAccountID = models.IntegerField()
    PostID = models.IntegerField()
    Content = models.TextField()
    
    Status = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    LastModifiedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Content

