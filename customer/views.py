import json

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from customer.models import Customer, MobileWallet, LoanOffer
from customer.serializers import CustomerSerializer, MobileWalletSerializer, LoanOfferSerializer, PayLoanSerializer
from lending.models import LoanProduct


class CustomerView(APIView):
    queryset = Customer.objects.filter(user__is_active=True).all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        customer = get_object_or_404(self.queryset, id=id, user=request.user)
        serializer = self.serializer_class(customer)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        customer = get_object_or_404(self.queryset, id=id, user=request.user)
        serializer = self.serializer_class(instance=customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class MobileWalletView(APIView):
    queryset = MobileWallet.objects.all()
    serializer_class = MobileWalletSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        wallet = get_object_or_404(self.queryset, id=id, customer=request.user.customer)
        serializer = self.serializer_class(wallet)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(customer=request.user.customer)
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        wallet = get_object_or_404(self.queryset, id=id, customer=request.user.customer)
        serializer = self.serializer_class(wallet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoanOfferView(APIView):
    queryset = LoanOffer.objects.all()
    serializer_class = LoanOfferSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        offers = self.queryset.filter(customer_id=request.user.customer.id)
        serializer = self.serializer_class(offers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(customer=request.user.customer)
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class PayLoanView(APIView):
    serializer_class = PayLoanSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
