import os
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from transliterate import translit
from quiz_app.models import Image, Music
from common.models import AbstractBaseModel

User = get_user_model()

class DragDropType(models.Model):
    TYPE_CHOICES = [
        ("classification", "Распределение объектов"),
        ("sequence-completion", "Продолжение последовательности"),
    ]

    type = models.CharField(max_length=50, choices=TYPE_CHOICES, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            self.slug = slugify(translit(self.get_type_display(), 'ru', reversed=True))  # Транслитерация и слаг
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_type_display()
    
    
class DragDropName(models.Model):
    type = models.ForeignKey(DragDropType, on_delete=models.CASCADE, related_name="names")
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class DragDropTask(AbstractBaseModel):
    name = models.ForeignKey(DragDropName, on_delete=models.CASCADE, related_name="tasks", null=True)
    description = models.TextField()
    replacement = models.BooleanField(default=True)
    background_image = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True, related_name="dragdrop_tasks")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dragdrop_tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    music = models.ForeignKey(Music, on_delete=models.SET_NULL, blank=True, null=True, related_name="dragdrop_tasks")
    next_task = models.ManyToManyField("self", blank=True, related_name="previous_tasks", symmetrical=False)

    slug = models.SlugField(max_length=255, unique=True, blank=True)  

    def save(self, *args, **kwargs):
        if not self.pk:  # Если объект ещё не в базе
            super().save(*args, **kwargs)  # Сначала сохраняем без слага
        if not self.slug or self.slug.strip() == "":
            transliterated_desc = translit(self.description[:30], 'ru', reversed=True)  
            self.slug = f"{slugify(transliterated_desc)}-{self.pk}"  # Теперь pk уже есть
        super().save(*args, **kwargs)  # Сохраняем снова с правильным slug


    def __str__(self):
        return f"{self.name.name} - {self.description}"
    
    def get_prefix(self):
        return "2"  # ДрагДроп

class Container(models.Model):
    task = models.ForeignKey(DragDropTask, on_delete=models.CASCADE, blank=True, null=True, related_name="containers")
    title = models.CharField(max_length=255)
    image_url = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True, related_name="containers")
    condition = models.CharField(max_length=255, blank=True)
    visibility_text = models.BooleanField(default=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.condition})"


class Item(models.Model):
    task = models.ForeignKey(DragDropTask, on_delete=models.CASCADE, blank=True, null=True, related_name="items")
    text = models.CharField(max_length=255)
    image_url = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True, related_name="items")
    condition = models.CharField(max_length=255, blank=True)
    visibility_text = models.BooleanField(default=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.text} ({self.condition})"

