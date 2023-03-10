"""  маршрутизатор приложения News """
from django.urls import path
from .views import PostList, OnePost, PostSearch

urlpatterns = [
    path('', PostList.as_view(), name='postList'),
    path('search/', PostSearch.as_view(), name='postSearch'),
    path('<int:pk>', OnePost.as_view(), name='onePost'),
]
