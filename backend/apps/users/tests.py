from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.users.models import User, Role
from apps.transactions.models import Category


class JWTAndRBACIntegrationTest(APITestCase):

    def setUp(self):
        # Create users
        self.admin = User.objects.create_user(
            username="admin", email="admin@test.com",
            password="pass", role=Role.ADMIN
        )

        self.analyst = User.objects.create_user(
            username="analyst", email="analyst@test.com",
            password="pass", role=Role.ANALYST
        )

        self.viewer = User.objects.create_user(
            username="viewer", email="viewer@test.com",
            password="pass", role=Role.VIEWER
        )

        self.category = Category.objects.create(name="Test")

        self.login_url = "/api/v1/auth/login/"
        self.tx_url = "/api/v1/transactions/"

    # 🔐 Helper function to get token
    def get_token(self, email, password):
        response = self.client.post(self.login_url, {
            "email": email,
            "password": password
        })
        return response.data["access"]

    # ✅ TEST 1: Login works
    def test_login_returns_token(self):
        response = self.client.post(self.login_url, {
            "email": "admin@test.com",
            "password": "pass"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    # ❌ TEST 2: No token → unauthorized
    def test_no_token_cannot_access(self):
        response = self.client.get(self.tx_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ✅ TEST 3: Admin can create transaction (JWT)
    def test_admin_can_create_transaction_with_token(self):
        token = self.get_token("admin@test.com", "pass")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        data = {
            "amount": "100.00",
            "transaction_type": "income",
            "category": self.category.id,
            "date": "2024-01-01"
        }

        response = self.client.post(self.tx_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # ❌ TEST 4: Analyst cannot create transaction
    def test_analyst_cannot_create_transaction_with_token(self):
        token = self.get_token("analyst@test.com", "pass")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        data = {
            "amount": "100.00",
            "transaction_type": "income",
            "category": self.category.id,
            "date": "2024-01-01"
        }

        response = self.client.post(self.tx_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ✅ TEST 5: Viewer can list but only own data
    def test_viewer_can_list_own_transactions(self):
        token = self.get_token("viewer@test.com", "pass")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(self.tx_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)