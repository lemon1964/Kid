from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from .models import PixiTaskType, PixiTask, PixiObject, PixiSVG, PixiImage
from .serializers import (
    PixiTaskTypeSerializer,
    PixiTaskSerializer,
    PixiObjectSerializer,
    PixiSVGSerializer,
    PixiImageSerializer,
)


class PixiTaskTypeViewSet(ReadOnlyModelViewSet):
    """API для получения типов задач (Геометрия, JPG/PNG, Раскраски)."""
    queryset = PixiTaskType.objects.all()
    serializer_class = PixiTaskTypeSerializer
    permission_classes = [AllowAny]


class PixiTaskViewSet(ReadOnlyModelViewSet):
    """API для получения задач Pixi."""
    serializer_class = PixiTaskSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = PixiTask.tasks.prefetch_related(
            "type",  # ✅ Подгружаем тип задачи
            Prefetch("objects", queryset=PixiObject.objects.all()),
            Prefetch("svg_images", queryset=PixiSVG.objects.all()),
            Prefetch("pixi_images", queryset=PixiImage.objects.select_related("image")),
        )

        slug = self.request.query_params.get("slug")
        if slug:
            queryset = queryset.filter(slug=slug)  # ✅ Фильтруем задачи по `slug`

        return queryset


class PixiObjectViewSet(ReadOnlyModelViewSet):
    """API для объектов (фигур) в задачах."""
    queryset = PixiObject.objects.all()
    serializer_class = PixiObjectSerializer
    permission_classes = [AllowAny]


class PixiSVGViewSet(ReadOnlyModelViewSet):
    """API для получения SVG-изображений для раскрасок."""
    queryset = PixiSVG.objects.all()
    serializer_class = PixiSVGSerializer
    permission_classes = [AllowAny]


class PixiImageViewSet(ReadOnlyModelViewSet):
    """API для получения JPG/PNG изображений, связанных с задачами."""
    queryset = PixiImage.objects.select_related("image").all()
    serializer_class = PixiImageSerializer
    permission_classes = [AllowAny]
