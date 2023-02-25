"""  маршрутизатор приложения News """
from django.urls import path
from .views import PostList, OnePost

urlpatterns = [
    path('', PostList.as_view(), name='postList'),
    path('<int:pk>', OnePost.as_view(), name='onePost'),
]
