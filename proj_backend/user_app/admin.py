from django.contrib import admin

# Register your models here, to admin can modified.
from .models.post import Post

admin.site.register(Post) 