from django.contrib import admin
from .models import Category
from .models import Genre
from .models import Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")


class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "year",
        "description",
        "category",
        "slug"
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
