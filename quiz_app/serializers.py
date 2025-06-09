from rest_framework import serializers
from .models import Quiz, Question, Answer, Image, Music, Sound


class ImageSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'file', 'title', 'file_url']

    def get_file_url(self, obj):
        if obj.file:
            return obj.file.url
        return None

class MusicSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Music
        fields = ['id', 'title', 'file_url']

    def get_file_url(self, obj):
        if obj.file:
            return obj.file.url
        return None


class SoundSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Sound
        fields = ['id', 'title', 'file_url']

    def get_file_url(self, obj):
        if obj.file:
            return obj.file.url
        return None


class AnswerSerializer(serializers.ModelSerializer):
    sound = SoundSerializer(read_only=True)
    image_url = ImageSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'text', 'alt_text', 'is_correct', 'image_url', 'sound']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)  # Сериализуем связанные изображения

    class Meta:
        model = Question
        fields = ['id', 'text', 'visibility_text', 'question_type', 'answers', 'images']


class QuizTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для передачи только title."""
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'slug']
        
        
class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    music = MusicSerializer(read_only=True)
    next_quizzes = QuizTitleSerializer(many=True, read_only=True)  # Используем вложенный сериализатор
    page_background = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'music', 'average_time_per_question', 'questions', 'next_quizzes', 'page_background']

    def get_page_background(self, obj):
        """Возвращает file_url, если фон существует"""
        if obj.page_background:
            return obj.page_background.file.url
        return None