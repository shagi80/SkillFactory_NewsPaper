"""  маршрутизатор приложения News """
from django.urls import path
from .views import PostList, OnePost, PostSearch, CreatePost, UpdatePost, DeletePost, subscribers

urlpatterns = [
    path('<int:category_pk>', PostList.as_view(), name = 'postListCategory'),
    path('', PostList.as_view(), name = 'postList'),
    path('search/', PostSearch.as_view(), name = 'postSearch'),
    path('post/<int:pk>', OnePost.as_view(), name = 'onePost'),
    path('create/', CreatePost.as_view(), name = 'createPost'),
    path('update/<int:pk>', UpdatePost.as_view(), name = 'updatePost'),
    path('delete/<int:pk>', DeletePost.as_view(), name = 'deletePost'),
    path('subscribers/', subscribers, name = 'subscribersUser'),
]
