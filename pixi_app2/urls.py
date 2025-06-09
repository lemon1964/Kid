from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PixiTaskTypeViewSet,
    PixiTaskViewSet,
    PixiObjectViewSet,
    PixiSVGViewSet,
    PixiImageViewSet,
)

# Создаем роутер
router = DefaultRouter()
router.register(r"task-types", PixiTaskTypeViewSet, basename="pixi-task-type")  # ✅ Типы задач
router.register(r"tasks", PixiTaskViewSet, basename="pixi-task")  # ✅ Задачи Pixi
router.register(r"objects", PixiObjectViewSet, basename="pixi-object")  # ✅ Фигуры (геометрия)
router.register(r"svgs", PixiSVGViewSet, basename="pixi-svg")  # ✅ SVG-файлы (раскраски)
router.register(r"images", PixiImageViewSet, basename="pixi-image")  # ✅ JPG/PNG изображения

# Подключаем маршруты
urlpatterns = [
    path("", include(router.urls)),
]
