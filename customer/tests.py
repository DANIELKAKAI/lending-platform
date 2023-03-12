from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import datetime

from customer.models import Customer, MobileWallet
from lending.models import LoanProduct
from users.models import User


class LendingApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            "admin@admin.com", "Xcaioshg99!"
        )
        self.customer = User.objects.create_user(
            "customer@gmail.com", "Xcaioshg99!"
        )
        self.customer2 = User.objects.create_user(
            "customer2@gmail.com", "Xcaioshg99!"
        )
        self.customer3 = User.objects.create_user(
            "customer3@gmail.com", "Xcaioshg99!"
        )
        self.customer_profile = Customer.objects.create(
            full_name="test customer", user=self.customer
        )
        self.mobile_wallet = MobileWallet.objects.create(
            phone_number="254768554234", customer=self.customer_profile
        )
        self.product_a_payload = {
            "product_name": "Product A",
            "loan_limit": "1000.00",
            "interest_rate": "10.00",
            "duration": 15,
            "notification_channel": "ALL",
        }
        self.product_b_payload = {
            "product_name": "Product B",
            "loan_limit": "2500.00",
            "interest_rate": "12.50",
            "duration": 30,
            "notification_channel": "ALL",
        }
        self.loan_product = LoanProduct.objects.create(
            **self.product_a_payload
        )

    def get_customer_access_token(self, email):
        # login customer
        response = self.client.post(
            reverse("token_obtain_pair"),
            data={"email": email, "password": "Xcaioshg99!"},
        )
        data = response.json()
        return data["access"]

    def test_create_and_update_customer_profile(self):
        access_token = self.get_customer_access_token(self.customer2.email)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # create customer profile
        full_name = "Test Customer"
        response = self.client.post(
            reverse("customer"), data={"full_name": full_name}
        )
        data = response.json()
        self.assertEqual(data.get("user"), str(self.customer2.id))
        self.assertEqual(data.get("full_name"), full_name)
        self.assertTrue(data.get("id"))

        # update
        full_name = "Test Customer new name"
        response = self.client.put(
            reverse("get-update-customer", kwargs={"id": data["id"]}),
            data={"full_name": full_name},
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("full_name"), full_name)

    def test_create_and_update_mobile_wallet(self):
        # Create profile
        Customer.objects.create(
            full_name="test customer 2", user=self.customer2
        )

        # Authentication
        access_token = self.get_customer_access_token(self.customer2.email)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # create wallet
        phone_number = "254729445215"
        response = self.client.post(
            reverse("mobile_wallet"), data={"phone_number": phone_number}
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get("id"))
        self.assertTrue(data.get("customer_id"))
        self.assertEqual(data.get("phone_number"), phone_number)
        self.assertTrue(data.get("amount"))

        # update
        phone_number = "254729445219"
        response = self.client.put(
            reverse("get-update-mobile_wallet", kwargs={"id": data["id"]}),
            data={"phone_number": phone_number},
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("phone_number"), phone_number)

    def test_create_loan_offer(self):
        # Authentication
        access_token = self.get_customer_access_token(self.customer.email)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # create with excess amount
        amount = 5000
        response = self.client.post(
            reverse("loan_offer"),
            data={"loan_product_id": self.loan_product.id, "amount": amount},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # create loan offer with valid amount
        amount = 500
        response = self.client.post(
            reverse("loan_offer"),
            data={"loan_product_id": self.loan_product.id, "amount": amount},
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get("id"))
        self.assertEqual(
            data.get("due_date"),
            (
                datetime.date.today()
                + datetime.timedelta(self.loan_product.duration)
            ).strftime("%Y-%m-%d"),
        )
        self.assertEqual(data.get("paid"), False)
        self.assertTrue(data.get("amount"), amount)

        # check amount credited to wallet
        wallet = MobileWallet.objects.get(customer=self.customer.customer)
        self.assertEqual(wallet.amount, amount)

        # create new offer while there's an existing loan offer
        amount = 500
        response = self.client.post(
            reverse("loan_offer"),
            data={"loan_product_id": self.loan_product.id, "amount": amount},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lending_flow(self):
        # login admin
        response = self.client.post(
            reverse("token_obtain_pair"),
            data={"email": self.admin.email, "password": "Xcaioshg99!"},
        )
        data = response.json()
        access_token = data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # create loan products
        product_a = self.client.post(
            reverse("loan_product"), data=self.product_a_payload
        ).json()
        product_b = self.client.post(
            reverse("loan_product"), data=self.product_b_payload
        ).json()

        # login customer
        response = self.client.post(
            reverse("token_obtain_pair"),
            data={"email": self.customer3.email, "password": "Xcaioshg99!"},
        )
        data = response.json()
        access_token = data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Create customer profile
        full_name = "Test Customer 3"
        self.client.post(reverse("customer"), data={"full_name": full_name})

        # create wallet
        wallet_data = self.client.post(
            reverse("mobile_wallet"), data={"phone_number": "254729445215"}
        ).json()

        # create loan offer
        response = self.client.post(
            reverse("loan_offer"),
            data={"loan_product_id": product_a["id"], "amount": 500},
        )
        data = response.json()
        loan_offer_amount = data["amount"]
        loan_offer_id = data["id"]

        # check wallet balance after loan offer
        response = self.client.get(
            reverse(
                "get-update-mobile_wallet", kwargs={"id": wallet_data["id"]}
            )
        )
        data = response.json()
        wallet_amount = data["amount"]
        self.assertEqual(loan_offer_amount, wallet_amount)

        # pay loan manually
        response = self.client.post(
            reverse("pay_loan"),
            data={"loan_offer_id": loan_offer_id, "amount": 500},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        loan_offers = self.client.get(reverse("loan_offer")).json()
        self.assertEqual(loan_offers[0]["paid"], True)
