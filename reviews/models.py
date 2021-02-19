from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from titles.models import Title
from users.models import User


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10, 'Оценка не может превышать 10'),
            MinValueValidator(1),
        ],
        verbose_name='Оценка',
    )

    class Meta:
        ordering = (
            '-pub_date',
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария',
    )

    class Meta:
        ordering = (
            '-pub_date',
        )
