from django.core import exceptions
from rest_framework import generics

from lending.models import LoanProduct
from lending.serializers import LoanProductSerializer


class LoanProductView(generics.ListCreateAPIView):
    queryset = LoanProduct.objects.all()
    serializer_class = LoanProductSerializer

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_admin is False:
            raise exceptions.PermissionDenied()
        return self.create(request, *args, **kwargs)
