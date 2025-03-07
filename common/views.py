from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from quiz_app.models import Quiz
from dragdrop_app.models import DragDropTask
from pixi_app2.models import PixiTask

from quiz_app.serializers import QuizSerializer
from dragdrop_app.serializers import DragDropTaskSerializer
from pixi_app2.serializers import PixiTaskSerializer

@api_view(["GET"])
@permission_classes([AllowAny])
def get_task_by_id(request, unique_id):
    """ Универсальный API для получения задачи по unique_id. """
    if unique_id.startswith("1"):
        task = get_object_or_404(Quiz, unique_id=unique_id)
        return Response({"type": "quiz", "data": QuizSerializer(task).data})

    if unique_id.startswith("2"):
        task = get_object_or_404(DragDropTask, unique_id=unique_id)
        return Response({"type": "dragdrop", "data": DragDropTaskSerializer(task).data})

    if unique_id.startswith("3"):
        task = get_object_or_404(PixiTask, unique_id=unique_id)
        return Response({"type": "pixi", "data": PixiTaskSerializer(task).data})

    return Response({"error": "Сущность не найдена"}, status=404)

@api_view(["GET"])
@permission_classes([AllowAny])
def get_task_list(request):
    """API для получения списка всех задач."""
    quizzes = list(Quiz.objects.values("unique_id", "title"))
    dragdrops = list(DragDropTask.objects.values("unique_id", "description"))
    pixi_tasks = list(PixiTask.tasks.values("unique_id", "title"))
    # print("quizzes", quizzes)
    result = {
        "quizzes": quizzes if quizzes else "Нет данных",
        "dragdrops": dragdrops if dragdrops else "Нет данных",
        "pixi_tasks": pixi_tasks if pixi_tasks else "Нет данных",
    }

    return Response(result)