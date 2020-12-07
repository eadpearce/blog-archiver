from django.contrib import admin
from post.models import Post, Reblog, Block


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('summary', 'post_url', 'id')


@admin.register(Reblog)
class ReblogAdmin(admin.ModelAdmin):
    list_display = ('id', 'post')


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'reblog', 'text', 'url', 'image')
