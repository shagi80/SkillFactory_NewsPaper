"""регистрация моделей в админке"""
from django.contrib import admin
from .models import Post, Category, Comment


class CategoryAdmin(admin.ModelAdmin):
    """класс администрирования категорий"""
    list_display = ('title',)
    list_display_links = ('title',)


class PostAdmin(admin.ModelAdmin):
    """класс администрирования новостей"""
    list_display = ('id', 'title', 'content_type', 'author', 'rating')
    list_display_links = ('id', 'title')
    list_filter = ('author',)


class CommentAdmin(admin.ModelAdmin):
    """класс администрирования комментариев"""
    list_display = ('id', 'text', 'author','rating')
    list_display_links = ('id', 'text',)


admin.site.register(Category,CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
