from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", CustomUser.Role.SUPER_ADMIN)
        return super().create_superuser(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = "SUPER_ADMIN", "Super admin"
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="users",
    )
    role = models.CharField(
        max_length=32,
        choices=Role.choices,
        default=Role.USER,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    class Meta:
        db_table = "user"
        ordering = ["username"]

    def clean(self) -> None:
        super().clean()
        if self.role in (self.Role.ADMIN, self.Role.USER) and self.company_id is None:
            raise ValidationError(
                {"company": "Admin and user accounts must belong to a company."}
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
