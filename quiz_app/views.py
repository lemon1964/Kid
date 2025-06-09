from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Quiz
from .serializers import QuizSerializer

@permission_classes([AllowAny])
class QuizViewSet(ReadOnlyModelViewSet):
    serializer_class = QuizSerializer
    
    def get_queryset(self):
        queryset = Quiz.objects.prefetch_related('questions__answers', 'questions__images').all()
        slug = self.request.query_params.get("slug")
        if slug:
            queryset = queryset.filter(slug=slug)  # ✅ Фильтруем задачи по `slug`

        return queryset

@permission_classes([AllowAny])
class QuizListView(APIView):
    def get(self, request):
        quizzes = Quiz.objects.all()
        data = [
            {
                "id": quiz.id,
                "title": quiz.title,
                "slug": quiz.slug,
            }
            for quiz in quizzes
        ]
        return Response(data)
