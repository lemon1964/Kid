from pixi_app2.models import PixiTask, PixiObject

def add_objects_to_select_all_but_squares():
    # ✅ Находим задачу
    try:
        task = PixiTask.tasks.get(slug="select-all-but-squares")
    except PixiTask.DoesNotExist:
        print("❌ Ошибка: Задача 'Select All But Squares' не найдена!")
        return

    # ✅ Проверяем, есть ли уже объекты
    if task.objects.exists():
        print("⚠️ Объекты уже добавлены в 'Select All But Squares'. Пропускаем.")
        return

    # ✅ Создаем новый набор объектов
    objects_data = [
        {"color": "blue", "shape": "circle", "is_correct": True},
        {"color": "red", "shape": "square", "is_correct": False},
        {"color": "green", "shape": "triangle", "is_correct": True},
        {"color": "yellow", "shape": "circle", "is_correct": True},
        {"color": "purple", "shape": "triangle", "is_correct": True},
        {"color": "orange", "shape": "square", "is_correct": False},
        {"color": "pink", "shape": "circle", "is_correct": True},
        {"color": "skyblue", "shape": "square", "is_correct": False},
    ]

    # ✅ Добавляем объекты
    objects_to_create = [PixiObject(task=task, **obj) for obj in objects_data]
    PixiObject.objects.bulk_create(objects_to_create)

    print("✅ Pixi objects successfully added to 'Select All But Squares'!")

# Запускаем скрипт
add_objects_to_select_all_but_squares()
