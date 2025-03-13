from django.contrib import admin
from .models import DragDropTask, DragDropName, DragDropType, Container, Item
from django.utils.html import format_html

class DragDropTaskAdmin(admin.ModelAdmin):
    list_filter = ('replacement', 'author', 'created_at')
    list_display = ('name', 'unique_id', 'replacement', 'author', 'created_at', 'slug', 'background_preview')
    filter_horizontal = ("next_task",)  # ✅ Позволяет выбирать задачи в админке
    search_fields = ('slug',)
    # exclude = ('slug',)
    # exclude = ('background_image', 'slug')
    
    # fields = ('unique_id', 'description','background_image', 'music')
    readonly_fields = ('unique_id',)  # ✅ Запрещаем редактирование, но показываем


    def background_preview(self, obj):
        if obj.background_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:5px"/>',
                obj.background_image.file.url  # Используем background_image
            )
        return "Нет изображения"

    background_preview.short_description = "Фон"
    
class DragDropNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'slug')
    search_fields = ('name', 'slug')

class DragDropTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'slug')
    search_fields = ('type', 'slug')

class ContainerAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'condition', 'image_url', 'visibility_text', 'alt_text')
    list_filter = ('task', 'condition', 'visibility_text')
    search_fields = ('title', 'condition', 'alt_text')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('text', 'task', 'condition', 'image_url', 'visibility_text', 'alt_text')
    list_filter = ('task', 'condition', 'visibility_text')
    search_fields = ('text', 'condition', 'alt_text')

admin.site.register(DragDropTask, DragDropTaskAdmin)
admin.site.register(DragDropType, DragDropTypeAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Container, ContainerAdmin)
admin.site.register(DragDropName, DragDropNameAdmin)

