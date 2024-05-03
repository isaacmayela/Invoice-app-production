from rest_framework import serializers
from .models import Company

class FieldsValidators():

    @staticmethod
    def validate_company_name(value):
        querry_set = Company.objects.filter(name__iexact = value)

        if querry_set.exists():
            raise serializers.ValidationError(f"A company with the name {value} already exists.")
        return value
    