from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    code = models.SlugField(max_length=64, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "company"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
