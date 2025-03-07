from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from common.models import AbstractBaseModel

User = get_user_model()

class Quiz(AbstractBaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    music = models.ForeignKey('Music', on_delete=models.SET_NULL, blank=True, null=True, related_name="quizzes")
    next_quizzes = models.ManyToManyField('self', blank=True, related_name="previous_quizzes", symmetrical=False)
    average_time_per_question = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    page_background = models.ForeignKey('Image', on_delete=models.CASCADE, related_name="quiz_page_background_images", blank=True, null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def get_prefix(self):
        return "1"  # Викторины


class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('text', 'Text Answer'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    visibility_text = models.BooleanField(default=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    image_url = models.ForeignKey('Image', on_delete=models.SET_NULL, blank=True, null=True, related_name="answers")
    sound = models.ForeignKey('Sound', on_delete=models.SET_NULL, blank=True, null=True, related_name="answers")

    def __str__(self):
        return self.text


class Image(models.Model):
    file = models.ImageField(upload_to='dummy')  # Временно указываем заглушку
    title = models.CharField(max_length=255, blank=True, null=True)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name="images", blank=True, null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="images", blank=True, null=True)
    containerdragdrop = models.ForeignKey('dragdrop_app.Container', on_delete=models.CASCADE, related_name="images", blank=True, null=True)
    itemdragdrop = models.ForeignKey('dragdrop_app.Item', on_delete=models.CASCADE, related_name="images", blank=True, null=True)
    taskdragdrop = models.ForeignKey('dragdrop_app.DragDropTask', on_delete=models.CASCADE, related_name="images", blank=True, null=True)
    taskpixi = models.ForeignKey('pixi_app2.PixiTask', on_delete=models.CASCADE, related_name="images", blank=True, null=True)

    def __str__(self):
        return self.title or self.file.name

    def get_upload_to(self, filename):
        if self.question and self.question.quiz:
            quiz_slug = slugify(self.question.quiz.title)
            return f'images/{quiz_slug}/{filename}'
        elif self.containerdragdrop:
            return f'images/containers/{filename}'
        elif self.itemdragdrop:
            return f'images/items/{filename}'
        elif self.taskdragdrop:
            return f'images/tasks/{filename}'
        elif self.taskpixi:
            return f'images/pixi/{filename}'
        elif self.quiz:
            return f'images/quizzes/{filename}'
        return f'images/unknown/{filename}'

    def save(self, *args, **kwargs):
        upload_to = self.get_upload_to(self.file.name)
        self.file.field.upload_to = lambda _, __: upload_to
        super().save(*args, **kwargs)



class Sound(models.Model):
    file = models.FileField(upload_to='sounds/')
    title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title or self.file.name


class Music(models.Model):
    file = models.FileField(upload_to='musics/')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_results")
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name="results")
    correct_answers = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    points_earned = models.PositiveIntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} ({self.points_earned} points)"
    
    