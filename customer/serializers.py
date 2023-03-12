from django.db import transaction
from rest_framework import serializers

from customer.models import Customer, MobileWallet, LoanOffer
from lending.models import LoanProduct
import datetime


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

    id = serializers.UUIDField(read_only=True)


class MobileWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileWallet
        fields = "__all__"

    id = serializers.UUIDField(read_only=True)
    customer_id = serializers.UUIDField(read_only=True)
    amount = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2
    )


class LoanOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOffer
        fields = "__all__"

    id = serializers.UUIDField(read_only=True)
    loan_product_id = serializers.UUIDField(write_only=True)
    customer_id = serializers.UUIDField(read_only=True)
    date_offered = serializers.DateField(read_only=True)
    due_date = serializers.DateField(read_only=True)
    paid = serializers.BooleanField(read_only=True)

    @transaction.atomic
    def create(self, validated_data):
        errors = dict()
        amount = validated_data["amount"]
        loan_product_id = validated_data["loan_product_id"]
        loan_product: LoanProduct = LoanProduct.objects.get(id=loan_product_id)
        if amount > loan_product.loan_limit:
            errors["amount"] = ["Amount requested greater than loan limit"]
        existing_offer = LoanOffer.objects.filter(
            loan_product_id=loan_product_id, paid=False
        ).exists()
        if existing_offer:
            errors["loan_product"] = [
                "You have an existing loan offer of similar product"
            ]
        if errors:
            raise serializers.ValidationError(errors)
        loan_offer = self.Meta.model(**validated_data)
        loan_offer.loan_product = loan_product
        loan_offer.due_date = datetime.date.today() + datetime.timedelta(
            days=loan_product.duration
        )
        loan_offer.save()
        mobile_wallet = MobileWallet.objects.get(
            customer_id=loan_offer.customer_id
        )
        mobile_wallet.amount += amount
        mobile_wallet.save()
        return loan_offer


class PayLoanSerializer(serializers.Serializer):
    class Meta:
        fields = ("amount", "loan_offer_id")

    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    loan_offer_id = serializers.UUIDField()

    def validate(self, data):
        loan_offer = LoanOffer.objects.get(id=data["loan_offer_id"])
        if loan_offer.amount == data["amount"]:
            loan_offer.paid = True
            loan_offer.save()
        if loan_offer.amount > data["amount"]:
            raise serializers.ValidationError(
                {"amount": "Amount Insufficient"}
            )
        if loan_offer.amount < data["amount"]:
            raise serializers.ValidationError({"amount": "Amount is Excess"})
        return data
