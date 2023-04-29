""" контроллер для приложения News """
from datetime import timedelta
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.cache import cache
from accounts.models import Author
from .models import Post, Category
from .filters import PostFilter
from .forms import EditPost

PAGINATOR_RANGE = 5

class MyView(PermissionRequiredMixin, View):
    """ оганичеие прав """
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')


class PostList(ListView):
    """ контроллер представления списка новостей """
    model = Post
    template_name = 'news/postList.html'
    context_object_name = 'posts'
    # ordering = ['-created']
    paginate_by = PAGINATOR_RANGE

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        if 'category_pk' in self.kwargs:
            context['current_category'] = Category.objects.get(
                pk=self.kwargs['category_pk'])
        return (context)

    def get_queryset(self):
        posts = Post.objects.all().order_by('-created')
        if 'category_pk' in self.kwargs:
            posts = posts.filter(category__pk=self.kwargs['category_pk'])
        return posts


class OnePost(DetailView):
    """ контроллер представления единичной новости """
    model = Post
    template_name = 'news/onePost.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.get_object().title[:10]} ...'
        return context

    def get_object(self):
        # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset) 
            cache.set(f'post-{self.kwargs["pk"]}', obj)       
        return obj


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


class CreatePost(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Добавление новости """
    template_name = 'news/editPost.html'
    form_class = EditPost
    extra_context = {'title': 'Добавление новости'}
    permission_required = ('news.add_post')

    def dispatch(self, request, *args, **kwargs):
        """ провека возможности добавить новость """
        if request.user.is_authenticated:
            post_count = Post.objects.filter(author__user=request.user,
                                            created__gte=(timezone.now() - timedelta(days=1))).count()
            if post_count == 3:
                messages.error(request, 'Вы можете добавить не более 3-х статей за сутки.')
                return redirect('postList')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """ инициализация поля -автор- формы  """
        kwargs = super().get_form_kwargs()
        kwargs['author'] = get_object_or_404(
            Author, user__pk=self.request.user.pk)
        return kwargs
    

class UpdatePost(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ редактирование новости """
    template_name = 'news/editPost.html'
    form_class = EditPost
    extra_context = {'title': 'Редактирование новости'}
    permission_required = ('news.change_post')

    def get_object(self, **kwargs):
        return get_object_or_404(Post, pk=self.kwargs.get('pk'))

    def get_form_kwargs(self):
        """ поле -автор- формы нужно снова инициализировать иначе будет создан новый объект """
        kwargs = super().get_form_kwargs()
        kwargs['author'] = self.object.author
        return kwargs

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его


class DeletePost(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'news/deletePost.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('postList')
    permission_required = ('news.delete_post')


@login_required
def subscribers(request):
    """ подписка пользователя на категорию новостей """
    if request.method == 'POST' and request.POST['category']:
        category = get_object_or_404(Category, pk=request.POST['category'])
        user = get_object_or_404(User, pk=request.POST['user_pk'])
        if not category.subscribers.filter(pk=user.pk):
            category.subscribers.add(user)
            category.save()
            messages.success(request, f'Вы успешно подписались на категорию "{category}" !')
        else:
            messages.error(request, 'Вы подписывались на эту категорию ранее !')
        return redirect('postListCategory', category_pk=request.POST['category'])
    return redirect('postList')
