from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User


class LoanProductApiTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser("admin@admin.com", "Xcaioshg99!")
        self.customer = User.objects.create_user("customer@gmail.com", "Xcaioshg99!")
        self.product_payload = {
            "product_name": "Product A",
            "loan_limit": "1000.00",
            "interest_rate": "10.00",
            "duration": 15,
            "notification_channel": "ALL"
        }

    def test_create_loan_product_by_admin(self):
        # login admin
        response = self.client.post(reverse("token_obtain_pair"),
                                    data={"email": self.admin.email, "password": "Xcaioshg99!"})
        data = response.json()
        access_token = data["access"]

        # create loan product
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.post(reverse("loan_product"),
                                    data=self.product_payload)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["product_name"], "Product A")

    def test_create_loan_product_by_customer_fails(self):
        # login customer
        response = self.client.post(reverse("token_obtain_pair"),
                                    data={"email": self.customer.email, "password": "Xcaioshg99!"})
        data = response.json()
        access_token = data["access"]

        # create loan products
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.post(reverse("loan_product"),
                                    data=self.product_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
