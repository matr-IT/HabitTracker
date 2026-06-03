from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    chat_id = models.CharField(
        max_length=100,
        verbose_name="Telegram Chat ID",
        help_text="Введите Ваш Telegram Chat ID для получения уведомлений",
    )
    full_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Полное имя",
        help_text="Введите Ваше полное имя",
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
