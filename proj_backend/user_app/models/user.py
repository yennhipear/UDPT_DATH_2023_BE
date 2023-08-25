from django.db import models
# import jsonfield
# khai báo đối tượng dữ liệu User

class User(models.Model):
    class Meta:
        db_table = 'UserAccount'

    ID = models.AutoField(primary_key=True)
    DisplayName = models.CharField(max_length=512)
    Email = models.CharField(max_length=512)
    Password = models.CharField(max_length=512)
    AboutMe = models.TextField()
    Location = models.CharField(max_length=512)
    RoleID = models.IntegerField()
    RoleName = models.CharField(max_length=512)
    Status = models.IntegerField()
    Level = models.CharField(max_length=512)
    CreatedDate = models.DateTimeField()

    def __str__(self):
        return self.DisplayName
