from dragdrop_app.models import DragDropTask, DragDropName

def update_task_names():
    for task in DragDropTask.objects.all():
        task.name = DragDropName.objects.filter(name=task.task_name).first()
        task.save(update_fields=["name"])
        print(f"Обновлена задача: {task.description} → {task.name.name}")

update_task_names()
