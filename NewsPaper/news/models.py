""" модели, описывающие контент"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.cache import cache


class Category(models.Model):
    """список категории"""

    title = models.CharField(
        max_length=150, unique=True, null=False, help_text="Категория новостей"
    )
    subscribers = models.ManyToManyField(User)

    class Meta:
        """изменение полей модели"""

        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return str(self.title)[:20]


class Post(models.Model):
    """статьи и новости"""
    NEWS = "NWS"
    ARTICLE = "ART"
    CONTENT_TYPES = [
        (NEWS, "новость"),
        (ARTICLE, "статья"),
    ]

    title = models.CharField(max_length=255, null=False,
                             help_text="Заголовок новости")
    text = models.TextField(null=False, help_text="Текст новости")
    rating = models.IntegerField(default=0, help_text="Рейтинг новости")
    content_type = models.CharField(
        max_length=3,
        choices=CONTENT_TYPES,
        default=NEWS,
        help_text="Тип контента (новость/статья)",
    )
    created = models.DateTimeField(
        auto_now_add=True, help_text="Дата и время создания")
    author = models.ForeignKey("accounts.Author", on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through="PostCategory")

    class Meta:
        """изменение полей модели"""

        verbose_name = "Новость/статья"
        verbose_name_plural = "Новости/статьи"

    def __str__(self):
        return str(self.title)[:20]

    def like(self):
        """метод повышения рейтинга"""
        self.rating += 1
        self.save()
        return self.rating

    def dislike(self):
        """метод понижения рейтинга"""
        self.rating -= 1
        self.save()
        return self.rating

    def preview(self):
        """превью статьи"""
        return (
            f"{str(self.text)[:80]} ..."
            if (len(str(self.text)) > 80)
            else str(self.text)
        )

    def get_absolute_url(self):
        return reverse_lazy('onePost', args=(self.pk,))

    def save(self, *args, **kwargs):
        # сначала вызываем метод родителя, чтобы объект сохранился
        super().save(*args, **kwargs)
        # затем удаляем его из кэша, чтобы сбросить его
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    """связующая таблица для Post и Category"""

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    poat = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    """комментприи к статьям"""

    text = models.TextField(null=False, help_text="Текст комментария")
    rating = models.IntegerField(default=0, help_text="Рейтинг комментария")
    created = models.DateTimeField(
        auto_now_add=True, help_text="Дата и время создания")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, help_text="Комментируемая новость"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="Пользователь, оставивший комментарий"
    )

    class Meta:
        """изменение полей модели"""

        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return str(self.text)[:20]

    def like(self):
        """метод повышения рейтинга"""
        self.rating += 1
        self.save()
        return self.rating

    def dislike(self):
        """метод понижения рейтинга"""
        self.rating -= 1
        self.save()
        return self.rating
