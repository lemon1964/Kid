from pixi_app2.models import PixiTask, PixiObject, PixiTaskType
from quiz_app.models import Music

def create_find_red_squares():
    # ✅ Ищем существующую категорию "Геометрия"
    try:
        task_type = PixiTaskType.objects.get(type="geometry")
    except PixiTaskType.DoesNotExist:
        print("❌ Ошибка: Категория 'Геометрия' не найдена!")
        return

    # ✅ Проверяем, есть ли уже такая задача
    if PixiTask.tasks.filter(slug="find-the-red-squares").exists():
        print("⚠️ Задача 'Find The Red Squares' уже существует. Пропускаем создание.")
        return

    # ✅ Создаем задачу
    task = PixiTask.tasks.create(
        type=task_type,
        title="Find The Red Squares",
        description="Find and click on all the red squares",
        task_mode="find",
        slug="find-the-red-squares"
    )

    # ✅ Привязываем музыку (если есть)
    try:
        task.music = Music.objects.get(title="find-the-red-squares")
        task.save()
    except Music.DoesNotExist:
        print("⚠️ Музыка 'find-the-red-squares' не найдена. Пропускаем.")

    # ✅ Объекты для задачи (немного разнообразим)
    objects_data = [
        {"color": "red", "shape": "square", "is_correct": True},
        {"color": "red", "shape": "circle", "is_correct": False},
        {"color": "blue", "shape": "square", "is_correct": False},
        {"color": "yellow", "shape": "triangle", "is_correct": False},
        {"color": "red", "shape": "triangle", "is_correct": False},
        {"color": "green", "shape": "square", "is_correct": False},
        {"color": "red", "shape": "square", "is_correct": True},
        {"color": "purple", "shape": "circle", "is_correct": False},
    ]

    # ✅ Создаем PixiObject
    objects_to_create = [PixiObject(task=task, **obj) for obj in objects_data]
    PixiObject.objects.bulk_create(objects_to_create)

    print("✅ Pixi task 'Find The Red Squares' and objects successfully created!")

# Запускаем скрипт
create_find_red_squares()
