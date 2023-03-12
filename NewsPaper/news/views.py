""" контроллер для приложения News """
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from accounts.models import Author
from .models import Post
from .filters import PostFilter
from .forms import EditPost

PAGINATOR_RANGE = 5


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

    def get_queryset(self):
        qset = super().get_queryset()
        return PostFilter(self.request.GET, queryset=qset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class CreatePost(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """ Добавление новости """
    template_name = 'news/editPost.html'
    form_class = EditPost
    extra_context = {'title': 'Добавление новости'}

    def get_form_kwargs(self):
        """ инициализация поля -автор- формы  """
        kwargs = super().get_form_kwargs()
        kwargs['author'] = get_object_or_404(
            Author, user__pk=self.request.user.pk)
        return kwargs

    def test_func(self):
        """ добавлять новости могут только авторы и суперпользователь """
        return Author.objects.filter(user=self.request.user)


class UpdatePost(UpdateView):
    """ редактирование новости """
    template_name = 'news/editPost.html'
    form_class = EditPost
    extra_context = {'title': 'Редактирование новости'}

    def get_object(self, **kwargs):
        return get_object_or_404(Post, pk=self.kwargs.get('pk'))

    def get_form_kwargs(self):
        """ поле -автор- формы нужно снова инициализировать иначе будет создан новый объект """
        kwargs = super().get_form_kwargs()
        kwargs['author'] = self.object.author
        return kwargs

    def test_func(self):
        """ изменять новость может только ее автор и суперпользователь """
        return (self.object.author.user == self.request.user) or self.request.user.is_superuser


class DeletePost(DeleteView):
    template_name = 'news/deletePost.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('postList')
