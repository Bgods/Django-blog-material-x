from django.contrib import admin
from .models import Comment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'post_id',
        'reply_id',
        'content',
        'comment_type',
        'add_time',
        'mail',
        'nick',
        'to_mail',
        'to_nick',
        'browser',
        'client',
        'is_show',
    ]

