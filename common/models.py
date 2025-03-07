from django.db import models

class AbstractBaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    unique_id = models.CharField(max_length=10, unique=True, editable=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            prefix = self.get_prefix()
            self.unique_id = f"{prefix}{self.id:03d}"
        super().save(*args, **kwargs)

    def get_prefix(self):
        raise NotImplementedError("Метод должен быть реализован в наследниках")

    class Meta:
        abstract = True
