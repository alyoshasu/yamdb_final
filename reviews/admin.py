from django.contrib import admin
# из файла models импортируем модель Review
from .models import Review
# из файла models импортируем модель Comment
from .models import Comment


class ReviewAdmin(admin.ModelAdmin):
    # добавим в начало столбец pk
    list_display = ("pk", "text", "pub_date", "author", "title", "score")
    # search_fields = ("text",)
    # list_filter = ("pub_date",)
    # empty_value_display = "-пусто-"
    # это свойство сработает для всех колонок: где пусто - там будет эта строка


class CommentAdmin(admin.ModelAdmin):
    # добавим в начало столбец pk
    list_display = ("pk", "review", "author", "text", "pub_date")


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
