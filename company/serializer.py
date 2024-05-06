from .models import Company
from rest_framework import serializers
from .validators import FieldsValidators


class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[FieldsValidators.validate_company_name ])
    email = serializers.EmailField()
    phone = serializers.CharField()
    adress = serializers.CharField()
    country = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    services = serializers.CharField()
    class Meta:
        model = Company
        fields = ('name', 'email', 'phone', 'adress', 'country', 'city', 'state', 'services')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.adress = validated_data.get('adress', instance.adress)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.services = validated_data.get('services', instance.services)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()


class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=132)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=132)
    adress = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100, default="Kinshasa")
    type = serializers.CharField(max_length=30)
    services = serializers.CharField(max_length=300)

    class Meta:
        model = Company
        fields = ('name', 'email', 'phone', 'adress', 'state', 'country', 'city', 'type', 'services')

    def get_fields(self):
        fields = super().get_fields()
        model_fields = self.Meta.model._meta.fields
        for field in model_fields:
            if field.name not in fields:
                fields[field.name] = serializers.CharField()
        return fields

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.adress = validated_data.get('adress', instance.adress)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.services = validated_data.get('services', instance.services)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()