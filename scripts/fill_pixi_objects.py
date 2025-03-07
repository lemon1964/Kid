from pixi_app2.models import PixiTask, PixiObject

def add_objects_to_task():
    # ✅ Получаем задачу "Find All The Squares"
    try:
        task = PixiTask.tasks.get(slug="find-all-the-squares")
    except PixiTask.DoesNotExist:
        print("❌ Ошибка: Задача 'Find All The Squares' не найдена!")
        return

    # ✅ Проверяем, нет ли уже объектов в задаче
    if PixiObject.objects.filter(task=task).exists():
        print("⚠️ Объекты уже существуют для этой задачи. Пропускаем создание.")
        return

    # ✅ Данные объектов
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

    # ✅ Создаем PixiObject (используем bulk_create для оптимизации)
    objects_to_create = [PixiObject(task=task, **obj) for obj in objects_data]
    PixiObject.objects.bulk_create(objects_to_create)  

    print("✅ Pixi objects successfully added to 'Find All The Squares'!")

# Запускаем скрипт
add_objects_to_task()
