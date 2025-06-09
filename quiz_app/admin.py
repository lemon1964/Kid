from django.contrib import admin
from .models import Quiz, Question, Answer, Image, Sound, Music, QuizResult
from django.utils.html import format_html


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'unique_id', 'description', 'background_preview')  # Поля, которые будут отображаться в админке
    search_fields = ('title',)
    
    # fields = ('title', 'unique_id', 'description', 'page_background')
    readonly_fields = ('unique_id',)  # ✅ Запрещаем редактирование, но показываем

    
    def background_preview(self, obj):
        if obj.page_background:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:5px"/>',
                obj.page_background.file.url
            )
        return "Нет изображения"

    background_preview.short_description = "Фон страницы"

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'question_type')  # Поля для отображения в админке
    search_fields = ('text',)
    list_filter = ('quiz',)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_correct', 'image_url', 'sound')  # Поля для отображения в админке
    list_filter = ('is_correct',)
    search_fields = ('text',)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')  # Показывать title и файл изображения
    search_fields = ('title',)

class SoundAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')  # Показывать title и файл звука
    search_fields = ('title',)

class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')  # Показывать title и файл музыки
    search_fields = ('title',)
    
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'points_earned')
    search_fields = ('user', 'quiz')

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Sound, SoundAdmin)
admin.site.register(Music, MusicAdmin)
admin.site.register(QuizResult, QuizResultAdmin)
