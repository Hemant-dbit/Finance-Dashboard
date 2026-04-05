from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from apps.transactions.models import Transaction
from decimal import Decimal
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class AnalyticsService:

    @staticmethod
    def get_dashboard_summary(user=None):
        """
        Returns total income, total expenses, net balance.
        """
        qs = Transaction.objects.filter(is_deleted=False)
        if user:
            qs = qs.filter(user=user)

        result = qs.aggregate(
            total_income=Sum(
                "amount", filter=Q(transaction_type="income")
            ),
            total_expenses=Sum(
                "amount", filter=Q(transaction_type="expense")
            ),
        )

        income   = result["total_income"]   or Decimal("0")
        expenses = result["total_expenses"] or Decimal("0")

        return {
            "total_income":   income,
            "total_expenses": expenses,
            "net_balance":    income - expenses,
        }

    @staticmethod
    def get_monthly_trends(user=None, months=6):
        """
        Returns income and expense totals per month for the last N months.
        """
        cutoff = timezone.now().date() - relativedelta(months=months)

        qs = Transaction.objects.filter(is_deleted=False, date__gte=cutoff)
        if user:
            qs = qs.filter(user=user)

        return (
            qs
            .annotate(month=TruncMonth("date"))
            .values("month", "transaction_type")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )

    @staticmethod
    def get_category_breakdown(user=None):
        """Returns spending totals grouped by category."""
        qs = Transaction.objects.filter(is_deleted=False)
        if user:
            qs = qs.filter(user=user)

        return (
            qs
            .values("category__name")
            .annotate(total=Sum("amount"), count=Count("id"))
            .order_by("-total")
        )
