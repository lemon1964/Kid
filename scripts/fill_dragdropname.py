from dragdrop_app.models import DragDropTask, DragDropName, DragDropType

def migrate_task_names():
    existing_names = set(DragDropName.objects.values_list("name", flat=True))

    for task in DragDropTask.objects.all():
        if task.task_name not in existing_names:
            dragdrop_name = DragDropName.objects.create(
                type=task.type,  # Используем текущий type
                name=task.task_name,  
                slug=task.task_name.lower().replace(" ", "-")  # Генерируем slug
            )
            print(f"Создано: {dragdrop_name.name}")

migrate_task_names()
