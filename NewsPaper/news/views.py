""" контроллер для приложения News """
from django.views.generic import ListView, DetailView
from .models import Post
from .filters import PostFilter

PAGINATOR_RANGE = 10


class PostList(ListView):
    """ контроллер представления списка новостей """
    model = Post
    template_name = 'news/postList.html'
    context_object_name = 'posts'
    ordering = ['-created']
    paginate_by = PAGINATOR_RANGE


class OnePost(DetailView):
    """ контроллер представления единичной новости """
    model = Post
    template_name = 'news/onePost.html'
    context_object_name = 'post'
    extra_context = {'title': str(model.title)[:10], }


class PostSearch(ListView):
    """ контроллер представления поиска новостей """
    model = Post
    template_name = 'news/searchPost.html'
    ordering = ['-created']
    context_object_name = 'posts'
    paginate_by = PAGINATOR_RANGE


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context