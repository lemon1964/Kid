from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DragDropTaskViewSet, DragDropTypeViewSet

router = DefaultRouter()
router.register(r'tasks', DragDropTaskViewSet, basename='dragdrop-task')
router.register(r'types', DragDropTypeViewSet, basename='dragdrop-type')

urlpatterns = [
    path('', include(router.urls)),
]
