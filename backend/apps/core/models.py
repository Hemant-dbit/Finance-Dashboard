import uuid
from django.db import models

class BaseModel(models.Model):
    """
    Abstract base for every model in the project.

    UUID primary key: harder to enumerate than integers (security),
    works across distributed systems without coordination.

    Soft delete: finance records are never truly deleted.
    Deleted records are excluded from queries but kept for audit.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True  # Django will NOT create a table for this

    def soft_delete(self):
        """Mark as deleted. Never call .delete() on finance records."""
        self.is_deleted = True
        self.save(update_fields=["is_deleted", "updated_at"])


class ActiveManager(models.Manager):
    """Default manager that excludes soft-deleted records."""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
