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
    services = serializers.CharField()
    class Meta:
        model = Company
        fields = ('id', 'name', 'email', 'phone', 'adress', 'country', 'city', 'services', )

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