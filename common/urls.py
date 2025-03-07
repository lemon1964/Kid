from django.urls import path
from .views import get_task_by_id, get_task_list

urlpatterns = [
    path("list/", get_task_list, name="get_task_list"),
    path("<str:unique_id>/", get_task_by_id, name="get_task_by_id"),
]
