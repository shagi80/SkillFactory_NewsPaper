""" теги и фильтры """
from django import template
import os
from NewsPaper.settings import STATICFILES_DIRS


register = template.Library()


@register.filter(name="censor")
def censor(value):
    """цензурирование нежелательных слов"""
    file_name = os.path.join(STATICFILES_DIRS[0], 'dictionaries', 'censor.txt')
    if not os.path.exists(file_name):
        return value
    with open(file_name, "r", encoding='utf8') as file:
        censor_dict = file.read().split(', ')
    for word in censor_dict:
        value = str(value).replace(word, '*'*3)
    return value
