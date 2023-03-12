from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User


class UserApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = User.objects.create_user(
            "customer@gmail.com", "Xcaioshg99!"
        )

    def test_register_user(self):
        url = reverse("sign_up")
        email = "customer2@gmail.com"
        response = self.client.post(
            url, data={"email": email, "password": "Cdadahsgg12!"}
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), email)
        self.assertTrue(data.get("id"))

    def test_login_user(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, data={"email": self.customer.email, "password": "Xcaioshg99!"}
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get("access"))
        self.assertTrue(data.get("refresh"))
