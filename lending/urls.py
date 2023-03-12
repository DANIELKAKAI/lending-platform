from django.urls import path

from lending.views import LoanProductView

urlpatterns = [
    path("product", LoanProductView.as_view(), name="loan_product"),
]
