from rest_framework import serializers
from decimal import Decimal
from .models import Transaction, Category
from django.utils import timezone



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ["id", "name", "description"]


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    created_by    = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model  = Transaction
        fields = [
            "id", "amount", "transaction_type",
            "category", "category_name",
            "date", "notes",
            "created_by", "created_at",
        ]
        read_only_fields = ["id", "created_at", "created_by", "category_name"]

    def validate_amount(self, value):
        if value <= Decimal("0"):
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Transaction date cannot be in the future.")
        return value
