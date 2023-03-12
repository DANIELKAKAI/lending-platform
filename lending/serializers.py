from rest_framework import serializers

from lending.models import LoanProduct


class LoanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProduct
        fields = "__all__"

    id = serializers.UUIDField(read_only=True)
