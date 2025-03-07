from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from .models import DragDropTask, DragDropType
from .serializers import DragDropTaskSerializer, DragDropTypeSerializer

    
class DragDropTaskViewSet(ReadOnlyModelViewSet):
    queryset = DragDropTask.objects.prefetch_related('containers', 'items', 'background_image', 'music', 'next_task').all()
    serializer_class = DragDropTaskSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """
        Позволяет фильтровать задачи по группе (slug) и конкретной задаче (task_slug).
        Примеры:
          - /api/dragdrop/tasks/?slug=resettle → список всех задач группы
          - /api/dragdrop/tasks/?slug=resettle&task_slug=rasseli-druzej-test → конкретная задача
        """
        queryset = super().get_queryset()
        name_slug = self.request.query_params.get("slug")  # Имя группы задач (resettle, place и т.д.)
        task_slug = self.request.query_params.get("task_slug")  # Конкретная задача (rasseli-druzej-test)

        if name_slug:
            queryset = queryset.filter(name__slug=name_slug)
        if task_slug:
            queryset = queryset.filter(slug=task_slug)

        return queryset
    
    
class DragDropTypeViewSet(ReadOnlyModelViewSet):
    queryset = DragDropType.objects.all()
    serializer_class = DragDropTypeSerializer
    permission_classes = [AllowAny]
