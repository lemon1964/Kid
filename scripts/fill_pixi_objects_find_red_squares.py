from pixi_app2.models import PixiTask, PixiObject

def add_objects_to_find_red_squares():
    # ✅ Находим задачу
    try:
        task = PixiTask.tasks.get(slug="find-the-red-squares")
    except PixiTask.DoesNotExist:
        print("❌ Ошибка: Задача 'Find The Red Squares' не найдена!")
        return

    # ✅ Проверяем, есть ли уже объекты
    if task.objects.exists():
        print("⚠️ Объекты уже добавлены в 'Find The Red Squares'. Пропускаем.")
        return

    # ✅ Создаем новый набор объектов
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

    # ✅ Добавляем объекты
    objects_to_create = [PixiObject(task=task, **obj) for obj in objects_data]
    PixiObject.objects.bulk_create(objects_to_create)

    print("✅ Pixi objects successfully added to 'Find The Red Squares'!")

# Запускаем скрипт
add_objects_to_find_red_squares()
