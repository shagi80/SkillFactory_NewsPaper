""" контроллер для приложения News """
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from accounts.models import Author
from .models import Post, Category
from .filters import PostFilter
from .forms import EditPost

PAGINATOR_RANGE = 5


def send_creation_notice(post, path):
    """ Отправка уведомления о новой новости """
    print(post)
    print(post.pk)
    # составляем список адресов
    for category in post.category.all():
        for user in category.subscribers.all():
            if user.email:
                # рендеринг HTML шаблона
                html_content = render_to_string(
                    'news/post_mail.html',
                    {'post': post, 'path': f'http://{path}/news/post/{str(post.pk)}',
                     'category': category, 'user': user}
                )
                # подготовка сообщения
                msg = EmailMultiAlternatives(
                    subject = post.title,
                    body=f'Здравствуй, {user.username}. Новая статья в твоём любимом разделе!',
                    from_email = 'shagi80@yandex.ru',
                    to = [user.email,]
                )
                # привязка HTML и отправка
                msg.attach_alternative(html_content, "text/html")
                msg.send()



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


class CreatePost(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Добавление новости """
    template_name = 'news/editPost.html'
    form_class = EditPost
    extra_context = {'title': 'Добавление новости'}
    permission_required = ('news.add_post')

    def get_form_kwargs(self):
        """ инициализация поля -автор- формы  """
        kwargs = super().get_form_kwargs()
        kwargs['author'] = get_object_or_404(
            Author, user__pk=self.request.user.pk)
        return kwargs

    def get_success_url(self):
        # отправка уведомления по электронной почте
        send_creation_notice(self.object, self.request.META["HTTP_HOST"])
        return super().get_success_url()
    

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
        return redirect('postList', category_pk=request.POST['category'])
    return redirect('postList')
