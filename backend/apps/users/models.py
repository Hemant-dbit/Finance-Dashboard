from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import BaseModel


class Role(models.TextChoices):
    VIEWER  = "viewer",  "Viewer"    # Read-only access to dashboard
    ANALYST = "analyst", "Analyst"   # Read + analytics endpoints
    ADMIN   = "admin",   "Admin"     # Full CRUD + user management


class User(AbstractUser, BaseModel):
    """
    Custom user model using email for login.
    Extended with role-based access and common fields from BaseModel.
    """
    email = models.EmailField(unique=True)
    role  = models.CharField(max_length=20, choices=Role.choices, default=Role.VIEWER)

    USERNAME_FIELD  = "email"       # Login with email, not username
    REQUIRED_FIELDS = ["username"]  

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.email} ({self.role})"
