from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email address")
    phone_number = models.CharField(max_length=35, verbose_name="Телефон", **NULLABLE, help_text="Введите номер телефона")
    country = models.CharField(max_length=100, verbose_name="Страна", **NULLABLE)
    avatar = models.ImageField(upload_to="users/photo", verbose_name="Аватар", help_text="Загрузите свой аватар")

    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
