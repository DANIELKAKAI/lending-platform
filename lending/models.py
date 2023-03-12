from django.core.validators import MinValueValidator
from django.db import models
import uuid


class LoanProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=256)
    loan_limit = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    notification_channel = models.CharField(
        max_length=256,
        choices=(("SMS", "SMS"), ("EMAIL", "EMAIL"), ("ALL", "ALL")),
    )

    class Meta:
        db_table = "loan_product"
        ordering = ["product_name"]
