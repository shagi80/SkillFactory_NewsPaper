""" фильтр приложения News """
from django import forms
from django_filters import FilterSet, CharFilter, DateTimeFilter, ModelChoiceFilter
from accounts.models import Author
from .models import Post


class PostFilter(FilterSet):
    """ фильтр новостей """
    title = CharFilter(
        lookup_expr = 'iregex',
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    created = DateTimeFilter(
        lookup_expr = 'gt',
        widget = forms.DateInput(attrs={'class':'form-control', 'type': 'date', })
    )
    author = ModelChoiceFilter(
        queryset = Author.objects.all(),
        empty_label = "Все авторы",
        widget = forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta():
        """  """
        model = Post
        fields = ['title', 'created', 'author']