from django.contrib import admin
from blog.models import Post, Tag, Links

# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'author', 'is_top', 'is_show', 'post_type']

@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'is_show']

