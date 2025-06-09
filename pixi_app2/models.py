from django.db import models
from django.utils.text import slugify
from transliterate import translit
from quiz_app.models import Image, Music
from common.models import AbstractBaseModel


class PixiTaskType(models.Model):
    TYPE_CHOICES = [
        ("geometry", "Геометрия"),
        ("image", "JPG/PNG"),
        ("coloring", "Раскраски"),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            self.slug = slugify(translit(self.get_type_display(), 'ru', reversed=True))  # Транслитерация и слаг
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.get_type_display()


class PixiTask(AbstractBaseModel):
    ANIMATION_CHOICES = [
    ("glow", "Glow"),      # Свечение и вращение
    ("shake", "Shake"),    # Тряска
    ("scale", "Scale"),    # Изменение размера
    ]
    type = models.ForeignKey(PixiTaskType, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    task_mode = models.CharField(max_length=10, choices=[("find", "Find"), ("select", "Select")])
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    music = models.ForeignKey(Music, on_delete=models.SET_NULL, blank=True, null=True)
    animation = models.CharField(max_length=10, choices=ANIMATION_CHOICES, default="glow")
    page_background = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="page_background_images", blank=True, null=True)
    pixi_background = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="pixi_background_images", blank=True, null=True)
    
    tasks = models.Manager()  # ✅ Добавляем менеджер задач

    def save(self, *args, **kwargs):
        if not self.pk:  # Если объект ещё не в базе
            super().save(*args, **kwargs)  # Сначала сохраняем без слага
        if not self.slug or self.slug.strip() == "":
            transliterated_desc = translit(self.description[:30], 'ru', reversed=True)  
            self.slug = f"{slugify(transliterated_desc)}-{self.pk}"  # Теперь pk уже есть
        super().save(*args, **kwargs)  # Сохраняем снова с правильным slug
        
    def __str__(self):
        return f"{self.title} ({self.get_task_mode_display()})"
    
    def get_prefix(self):
        return "3"  # Пикси


class PixiObject(models.Model):
    task = models.ForeignKey(PixiTask, related_name="objects", on_delete=models.CASCADE)
    color = models.CharField(max_length=20)
    shape = models.CharField(max_length=20)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.color} {self.shape} ({'Correct' if self.is_correct else 'Incorrect'})"


class PixiImage(models.Model):
    task = models.ForeignKey(PixiTask, related_name="pixi_images", on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="pixi_task_images", blank=True, null=True)  # ✅ Добавили null=True
    is_correct = models.BooleanField(default=False)  # Верный ли выбор

    def __str__(self):
        return f"{self.image.title} ({'Correct' if self.is_correct else 'Incorrect'})"


class PixiSVG(models.Model):
    task = models.ForeignKey(PixiTask, related_name="svg_images", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="images/svg/")

    def __str__(self):
        return self.title
