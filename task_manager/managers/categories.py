from django.db import models

class SoftDeleteManager(models.Model):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

