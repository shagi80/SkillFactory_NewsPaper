""" теги и фильтры """
from django import template
import os
from accounts.models import Author
from NewsPaper.settings import STATICFILES_DIRS


register = template.Library()


@register.filter(name="censor")
def censor(value):
    """ цензурирование нежелательных слов """
    file_name = os.path.join(STATICFILES_DIRS[0], 'dictionaries', 'censor.txt')
    if not os.path.exists(file_name):
        return value
    with open(file_name, "r", encoding='utf8') as file:
        censor_dict = file.read().split(', ')
    for word in censor_dict:
        value = str(value).replace(word, '*'*3)
        #value = str(value).replace(word, word[0] + "*"*(len(word)-2) + word[-1])
    return value


@register.inclusion_tag('news/tag_show_post.html')
def show_post(post):
    """ отображение заголовка новости """
    return {"post": post}


@register.simple_tag
def get_filters(request):
    """ получение параметров GET-запроса для корректной пагинации """
    res = ''
    for itm in request.GET:
        if itm != 'page':
            res = res + '&' + itm + '=' + request.GET.get(itm)
    return res


@register.filter()
def is_author(user):
    """ проверка не является ли пользователь автором """
    return user.groups.filter(name = 'authors').exists()


@register.filter()
def have_subscription(user, category):
    """ проверка подписки на категорию """
    return user and category and  category.subscribers.filter(pk=user.pk)
