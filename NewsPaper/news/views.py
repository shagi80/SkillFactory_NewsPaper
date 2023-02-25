""" контроллер для приложения News """
from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    """ контроллер представления списка новостей """
    model = Post
    template_name = 'news/postList.html'
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('-created')


class OnePost(DetailView):
    """ контроллер представления единичной новости """
    model = Post
    template_name = 'news/onePost.html'
    context_object_name = 'post'
    extra_context = {'title': str(model.title)[:10], }

