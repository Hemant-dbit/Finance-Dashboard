from django.db import models
from apps.core.models import BaseModel, ActiveManager


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        db_table = "categories"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Transaction(BaseModel):
    class Type(models.TextChoices):
        INCOME  = "income",  "Income"
        EXPENSE = "expense", "Expense"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,  # Cannot delete user with transactions
        related_name="transactions",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=Type.choices)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="transactions",
    )
    date = models.DateField()
    notes = models.TextField(blank=True)

    objects = ActiveManager()   
    all_objects = models.Manager()  

    class Meta:
        db_table = "transactions"
        ordering = ["-date"]
        indexes = [
            # Indexes make filtering fast at scale.
            # Without these, every filter is a full table scan.
            models.Index(fields=["user", "date"]),
            models.Index(fields=["transaction_type"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_deleted"]),
        ]

    def __str__(self):
        return f"{self.transaction_type} | {self.amount} | {self.date}"
