from django.contrib import admin
# из файла models импортируем модель User
from .models import User

admin.site.register(User)
