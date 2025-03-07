from pixi_app2.models import PixiTask, PixiObject, PixiTaskType
from django.utils.text import slugify

def create_pixi_tasks():
    # Получаем или создаем тип задачи "geometry"
    geometry_type, _ = PixiTaskType.objects.get_or_create(type="geometry")

    # ✅ Создаем задачу "Find All The Squares" через tasks (менеджер)
    task1 = PixiTask.tasks.create(
        type=geometry_type,
        title="Find All The Squares",
        description="Find and click on all the squares",
        task_mode="find",
        slug=slugify("Find All The Squares")
    )

    # Фигуры для задачи
    objects_data = [
        {"color": "red", "shape": "square", "is_correct": True},
        {"color": "blue", "shape": "circle", "is_correct": False},
        {"color": "green", "shape": "triangle", "is_correct": False},
        {"color": "yellow", "shape": "square", "is_correct": True},
        {"color": "skyblue", "shape": "circle", "is_correct": False},
        {"color": "purple", "shape": "triangle", "is_correct": False},
        {"color": "orange", "shape": "square", "is_correct": True},
        {"color": "pink", "shape": "circle", "is_correct": False},
    ]

    # ✅ Создаем PixiObjects (без `create`, используем `bulk_create`)
    objects_to_create = [PixiObject(task=task1, **obj) for obj in objects_data]
    PixiObject.objects.bulk_create(objects_to_create)  

    print("✅ Pixi task and objects added successfully!")

# Запускаем скрипт
create_pixi_tasks()
