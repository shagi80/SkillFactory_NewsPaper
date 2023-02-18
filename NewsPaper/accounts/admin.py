"""экспорт классов в админку"""
from django.contrib import admin
from .models import Author


class AuthorAdmin(admin.ModelAdmin):
    """ класс администрирования авторов"""

    list_display = ('id', 'user', 'rating',)
    list_display_links = ('id', 'user', 'rating',)


admin.site.register(Author, AuthorAdmin)
