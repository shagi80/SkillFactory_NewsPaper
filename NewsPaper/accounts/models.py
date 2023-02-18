"""модели, описывающие пользователей и их аккаунты"""
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from news.models import Post, Comment


class Author(models.Model):
    """модель Aвтор контента"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, help_text="Рейтинг автора")

    def update_rating(self):
        """метод определения рейтинга автора"""
        post_rating = Post.objects.filter(author=self).aggregate(Sum("rating"))
        comment_rating = Comment.objects.filter(author=self.user).aggregate(
            Sum("rating")
        )
        post_comment_rating = Comment.objects.filter(post__author=self).aggregate(
            Sum("rating")
        )
        self.rating = (
            post_rating["rating__sum"] * 3
            + comment_rating["rating__sum"]
            + post_comment_rating["rating__sum"]
        )
        self.save()
        return self.rating

    class Meta:
        """изменение полей модели"""

        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return str(self.user.username)
