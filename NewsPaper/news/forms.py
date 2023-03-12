""" формы редактирования форм """
from django import forms
from .models import Post


class EditPost(forms.ModelForm):
    """ создание и зименение формы """

    class Meta():
        model = Post
        fields = ('title', 'category', 'text', 'author')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введите заголовок новости ..."}),
            'category': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Введите текст новости ...", 'rows' : 7}),
            'author': forms.HiddenInput(),
        }

    def __init__(self,  *args, author=None, **kwargs):
        """ устанавливаем автора """
        super(EditPost, self).__init__(*args, **kwargs)
        if author:
            self.initial['author'] = author
