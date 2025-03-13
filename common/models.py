from django.db import models

class AbstractBaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    unique_id = models.CharField(max_length=10, unique=True, editable=False, blank=True)

    def save(self, *args, **kwargs):
        # Если объект новый, сохраняем его для получения pk
        if not self.pk:
            super().save(*args, **kwargs)
        # Если уникальный идентификатор ещё не установлен, вычисляем его
        if not self.unique_id:
            prefix = self.get_prefix()
            self.unique_id = f"{prefix}{self.pk:03d}"
            # Обновляем только поле unique_id, чтобы избежать рекурсии
            super().save(update_fields=["unique_id"])
        else:
            super().save(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     if not self.unique_id:
    #         prefix = self.get_prefix()
    #         self.unique_id = f"{prefix}{self.id:03d}"
    #     super().save(*args, **kwargs)

    def get_prefix(self):
        raise NotImplementedError("Метод должен быть реализован в наследниках")

    class Meta:
        abstract = True
