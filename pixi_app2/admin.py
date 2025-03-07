from django.contrib import admin
from .models import PixiTaskType, PixiTask, PixiObject, PixiSVG, PixiImage
from django.utils.html import format_html

@admin.register(PixiTaskType)
class PixiTaskTypeAdmin(admin.ModelAdmin):
    list_display = ("type", "slug")  # Отображение типов задач
    prepopulated_fields = {"slug": ("type",)}  # Автозаполнение slug

class PixiImageInline(admin.TabularInline):  # или admin.StackedInline
    model = PixiImage
    extra = 1  # Количество пустых строк для добавления новых объектов
    
@admin.register(PixiTask)
class PixiTaskAdmin(admin.ModelAdmin):
    list_display = ("title", 'unique_id', "type", "task_mode", "slug", "music", "background_preview")
    list_filter = ("type", "task_mode")  # Фильтрация по типу и режиму задачи
    search_fields = ("title", "description", "slug")  # Поиск по заголовку и описанию
    prepopulated_fields = {"slug": ("title",)}  # Автозаполнение slug
    inlines = [PixiImageInline]  # ✅ Добавляем inline вместо filter_horizontal
    
    # fields = ('unique_id', 'page_background', 'title', 'description', 'type', 'task_mode', 'slug')
    readonly_fields = ('unique_id',)  # ✅ Запрещаем редактирование, но показываем

    def background_preview(self, obj):
        if obj.page_background:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:5px"/>',
                obj.page_background.file.url
            )
        return "Нет изображения"

    background_preview.short_description = "Фон страницы"

@admin.register(PixiObject)
class PixiObjectAdmin(admin.ModelAdmin):
    list_display = ("task", "color", "shape", "is_correct")  # Отображаемые колонки
    list_filter = ("is_correct", "task")  # Фильтрация по задаче и правильности
    search_fields = ("color", "shape")  # Поиск

@admin.register(PixiImage)
class PixiImageAdmin(admin.ModelAdmin):
    list_display = ("task", "image", "is_correct")  # Отображение PixiImage
    list_filter = ("is_correct", "task")  # Фильтрация
    search_fields = ("image__title",)  # Поиск по названию изображения

@admin.register(PixiSVG)
class PixiSVGAdmin(admin.ModelAdmin):
    list_display = ("task", "title", "file")  # Отображаемые колонки
    search_fields = ("title",)  # Поиск
