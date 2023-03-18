from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Author

# Create your views here.


@login_required
def SetAuthor(request):
    """ делаем юзера автором """

    # если по каким-то причинам юзер еще не в группке коммон
    common_group = Group.objects.get(name='common')
    if not request.user.groups.filter(name = 'common').exists():
        common_group.user_set.add(request.user)

    # добавляем в группу авторы
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name = 'authors').exists():
        authors_group.user_set.add(request.user)

    # добавляем в таблицу Авторы
    if not Author.objects.filter(user=request.user):
        new_author = Author.objects.create(user=request.user, rating = 0)
        new_author.save()
        
    return redirect(reverse_lazy('postList'))

