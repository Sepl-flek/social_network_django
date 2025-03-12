from django.contrib import admin
from django.contrib.admin import ModelAdmin

from post.models import Post, UserPostRelation


# Register your models here.
@admin.register(Post)
class PostAdmin(ModelAdmin):
    pass

@admin.register(UserPostRelation)
class UserPostRelationAdmin(ModelAdmin):
    pass