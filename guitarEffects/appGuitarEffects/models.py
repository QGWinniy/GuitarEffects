from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название группы")
    description = models.TextField(blank=True, default="", verbose_name="Описание")

    def __str__(self):
        return self.name

class Song(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа", related_name='songs')
    title = models.CharField(max_length=255, verbose_name="Название песни")
    effects = models.TextField(blank=True, verbose_name="Используемые эффекты")
    guitar_model = models.CharField(max_length=100, blank=True, verbose_name="Модель гитары")
    amplifier = models.CharField(max_length=100, blank=True, verbose_name="Усилитель")
    description = models.TextField(blank=True, verbose_name="Дополнительное описание")

    def __str__(self):
        return f"{self.title} - {self.group.name}"

    