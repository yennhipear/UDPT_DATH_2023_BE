from django.db import models
# import jsonfield
# khai báo đối tượng dữ liệu post 

class Post(models.Model):
    class Meta:
        db_table = 'Post'

    ID = models.PositiveBigIntegerField(primary_key=True)
    # author_id = models.CharField( max_length = 20)
    Title = models.CharField(max_length=512)
    Content = models.CharField(max_length=100000)
    # like_num = models.PositiveBigIntegerField()
    # dislike_num = models.PositiveBigIntegerField()
    # tags = jsonfield.JSONField()
    # status = IntegerField()
    # created_date = models.DateTimeField(auto_now_add=True)
    # modified_date = models.DateTimeField()
    # modified_by = models.CharField(max_length = 20)
    

    def __str__(self):
        return self.Title
