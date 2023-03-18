from django.urls import path
from .views import SetAuthor

urlpatterns = [
    path('set/', SetAuthor, name = 'setAuthor'),
]
