from django.urls import path

from customer.views import CustomerView, MobileWalletView, LoanOfferView, PayLoanView

urlpatterns = [
    path('', CustomerView.as_view(), name="customer"),
    path('<uuid:id>', CustomerView.as_view(), name="get-update-customer"),
    path('mobile-wallet', MobileWalletView.as_view(), name="mobile_wallet"),
    path('mobile-wallet/<uuid:id>', MobileWalletView.as_view(), name="get-update-mobile_wallet"),
    path('loan-offer', LoanOfferView.as_view(), name="loan_offer"),
    path('pay-loan', PayLoanView.as_view(), name="pay_loan")
]
