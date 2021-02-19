import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=40,
        unique=True,
    )

    def __str__(self):
        return self.slug

    class Meta:
        ordering = (
            '-name',
        )


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название жанра',
        blank=False,
    )
    slug = models.SlugField(
        max_length=40,
        unique=True,
    )

    def __str__(self):
        return self.slug

    class Meta:
        ordering = (
            '-name',
        )


class Title(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения',
    )
    year = models.PositiveIntegerField(
        default=datetime.datetime.now().year,
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10, 'Рейтинг не может быть выше 10'),
            MinValueValidator(1),
        ],
        null=True,
        verbose_name="Рейтинг",
    )
    description = models.TextField(
        max_length=1000,
        verbose_name='Краткое описание',
        null=True,
    )
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
    )
    slug = models.SlugField(
        null=True,
        max_length=40,
    )

    class Meta:
        ordering = (
            '-rating',
        )
