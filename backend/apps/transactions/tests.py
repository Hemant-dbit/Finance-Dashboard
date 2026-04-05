from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User, Role
from apps.transactions.models import Category, Transaction
from django.urls import reverse
from decimal import Decimal
from django.utils import timezone


class TransactionAccessControlTest(APITestCase):
    """
    Tests the most important thing in the system: RBAC.
    We test that the right roles can do the right things.
    """

    def setUp(self):
        self.admin   = User.objects.create_user(
            email="admin@test.com", username="admin", password="pass", role=Role.ADMIN
        )
        self.analyst = User.objects.create_user(
            email="analyst@test.com", username="analyst", password="pass", role=Role.ANALYST
        )
        self.viewer  = User.objects.create_user(
            email="viewer@test.com", username="viewer", password="pass", role=Role.VIEWER
        )
        self.category = Category.objects.create(name="Test Category")
        self.tx_data = {
            "amount": "100.00",
            "transaction_type": "income",
            "category": str(self.category.id),
            "date": str(timezone.now().date()),
        }

    def test_admin_can_create_transaction(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post("/api/v1/transactions/", self.tx_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_analyst_cannot_create_transaction(self):
        self.client.force_authenticate(user=self.analyst)
        response = self.client.post("/api/v1/transactions/", self.tx_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_viewer_cannot_list_all_transactions(self):
        """Viewers should only see their own transactions."""
        # Create a transaction belonging to admin
        Transaction.objects.create(
            user=self.admin, amount=Decimal("100"), category=self.category,
            transaction_type="income", date=timezone.now().date()
        )
        self.client.force_authenticate(user=self.viewer)
        response = self.client.get("/api/v1/transactions/")
        # Viewer sees 0 — they have no transactions
        self.assertEqual(len(response.data["results"]), 0)

    def test_amount_must_be_positive(self):
        self.client.force_authenticate(user=self.admin)
        data = {**self.tx_data, "amount": "-50.00"}
        response = self.client.post("/api/v1/transactions/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
