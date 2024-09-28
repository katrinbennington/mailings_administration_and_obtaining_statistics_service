from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    name = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое статьи', **NULLABLE)
    preview = models.ImageField(upload_to='blog/photo', verbose_name='Изображение', **NULLABLE)
    views_counter = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'