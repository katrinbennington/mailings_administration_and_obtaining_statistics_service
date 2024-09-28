from django.db import models
from django.utils import timezone
from phone_field import PhoneField

from config import settings
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    phone = PhoneField(blank=True, verbose_name="Телефон", help_text='Введите номер телефона')
    email = models.EmailField(unique=True, verbose_name="Электронная почта", **NULLABLE)
    FIO = models.CharField(max_length=100, verbose_name="Ф.И.О.", help_text="Введите свои Фамилию, Имя и Отчество")
    comment = models.CharField(max_length=250, verbose_name="Комментарий")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f"{self.FIO} {self.email} {self.phone} {self.comment} {self.user}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("FIO",)


class Messages(models.Model):
    topic = models.CharField(max_length=40, verbose_name='Тема письма', help_text="Укажите тему письма")
    text = models.CharField(max_length=150, verbose_name='Тело письма',)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return (
            f"{self.topic} {self.text} {self.user} ")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("topic",)


class Subscription(models.Model):
    clients = models.ManyToManyField(
        Client,
        related_name="subscription",
        verbose_name="клиент",
    )
    message = models.ForeignKey(
        Messages,
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name="subscription",
        verbose_name="сообщение",
    )
    name = models.CharField(max_length=100, verbose_name="Название рассылки", help_text="Введите название рассылки", **NULLABLE)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата и время первой рассылки")
    intervals = models.CharField(max_length=40, verbose_name='Периодичность',
                                       choices=(('daily', 'раз в день'),
                                                ('weekly', 'раз в неделю'),
                                                ('monthly', 'раз в месяц')))
    status = models.CharField(max_length=40, verbose_name='Статус рассылки',
                                       choices=(('created', 'Создана'),
                                                ('in process', 'Запущена'),
                                                ('finished', 'Завершена')))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return (
            f"{self.created_at} {self.intervals} {self.status} {self.user} ")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("status",)
        # permissions = [
        #     ("can_cancel_publication", "Can cancel publication of product"),
        #     ("can_change_description", "Can change description of product"),
        #     ("can_change_product_category", "Can change product category"),
        #  ]


class Mailing(models.Model):
    last_attempt = models.CharField(default=timezone.now, verbose_name='Дата и время последней рассылки')
    status_attempt = models.CharField(max_length=40, verbose_name='Статус рассылки',
                                       choices=(('success', 'успешно'),
                                                ('failure ', 'не успешно')))
    is_active = models.BooleanField(default=True)
    report = models.CharField(max_length=40, verbose_name='Ответ почтового сервера, если он был')

    def __str__(self):
        return (
            f"{self.last_attempt} {self.status_attempt} {self.report}")

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ("last_attempt",)