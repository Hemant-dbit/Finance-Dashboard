import django_filters
from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    # Date range filtering
    date_from = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    date_to   = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    # Min/max amount
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")

    class Meta:
        model  = Transaction
        fields = ["transaction_type", "category", "date_from", "date_to",
                  "min_amount", "max_amount"]


