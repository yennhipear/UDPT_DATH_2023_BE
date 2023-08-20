from django.db import models
# import jsonfield
# khai báo đối tượng dữ liệu Tag 

# kkk
class Tag(models.Model):
    class Meta:
        db_table = 'Tag'

    ID = models.PositiveBigIntegerField(primary_key=True)
    # author_id = models.CharField( max_length = 20)
    Name = models.CharField(max_length=512)
    #Content = models.CharField(max_length=100000)
    

    def __str__(self):
        return self.Name
