from django.contrib import admin
from .models import Comment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'content', 'comment_type', 'add_time', 'mail', 'nick', 'to_mail', 'to_nick', 'browser', 'client', 'is_show', 'avatar']
    fieldsets = (
        (None, {'fields': ['post', 'content', 'comment_type', 'mail', 'nick', 'is_show']}),
        ('高级', {
            'fields': ['to_mail', 'to_nick', 'browser', 'client'],
            'classes': ('collapse',)  # 是否折叠显示
        }),
    )