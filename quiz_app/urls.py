from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuizListView

from django.http import HttpResponse

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')

urlpatterns = [
    path('', include(router.urls)),  # Пути для ViewSet
    path('list/', QuizListView.as_view(), name='quiz-list'),  # Новый эндпойнт
]
