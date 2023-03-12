from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password")

    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data["password"]
        user = self.Meta.model(**validated_data)
        errors = dict()
        try:
            validators.validate_password(password=password, user=user)
        except ValidationError as e:
            errors["password"] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        user.set_password(password)
        user.save()
        return user
