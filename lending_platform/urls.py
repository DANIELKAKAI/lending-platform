from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('lending/', include('lending.urls')),
    path('customer/', include('customer.urls'))
]
