from pixi_app2.models import PixiTaskType, PixiTask

def create_select_all_but_squares_task():
    # ✅ Определяем тип задачи (Геометрия)
    task_type = PixiTaskType.objects.get(type="geometry")

    # ✅ Проверяем, есть ли уже такая задача
    if PixiTask.tasks.filter(slug="select-all-but-squares").exists():
        print("⚠️ Задача 'Select All But Squares' уже существует. Пропускаем.")
        return

    # ✅ Создаем задачу
    task = PixiTask.tasks.create(
        type=task_type,
        title="Select All But Squares",
        description="Find and click on all shapes except squares",
        task_mode="select",
        slug="select-all-but-squares"
    )

    print(f"✅ Задача '{task.title}' успешно создана!")

# Запускаем скрипт
create_select_all_but_squares_task()
