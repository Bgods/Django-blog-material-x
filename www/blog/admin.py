from django.contrib import admin
from blog.models import Post, Tag, Links, Advertising, SidebarMusic, Tutorial, SiteSettings
from django.utils.html import format_html


# Register your models here.
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'is_show']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def show_tags(self, obj):
        tag_list = []
        tags = obj.tags.all()
        if tags:
            for tag in tags:
                tag_list.append(tag.name)
            return ','.join(tag_list)
        else:
            return format_html('<span style="color:red;">无标签</span>')

    '''设置表头'''
    show_tags.short_description = '标签'  # 设置表头

    list_display = ['title', 'show_tags', 'tutorial', 'created_time', 'modified_time', 'author', 'post_type', 'views', 'is_top', 'is_show']
    fieldsets = (
        (None, {'fields': ['post_type', 'title', 'body', 'author', 'created_time', 'tags', 'tutorial']}),
        ('高级', {
            'fields': ['views', 'is_show', 'is_top'],
            'classes': ('collapse',)  # 是否折叠显示
        }),
    )
    search_fields = ['title', 'show_tags']

@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'is_show']


@admin.register(Advertising)
class AdvertisingAdmin(admin.ModelAdmin):
    list_display = ['ad_name', 'ad_url', 'img_url', 'is_show']


@admin.register(SidebarMusic)
class SidebarMusicAdmin(admin.ModelAdmin):
    list_display = ['server', 'mode', 'type', 'play_id', 'home_url', 'autoplay', 'enable']

