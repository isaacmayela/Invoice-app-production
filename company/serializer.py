from .models import Company, Customer, Invoice, Article
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
        fields = '__all__'

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
        model = Customer
        fields = '__all__'

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


class InvoiceSerializer(serializers.ModelSerializer):
    # customer = serializers.CharField(max_length=132)
    # email = serializers.EmailField()
    # phone = serializers.CharField(max_length=132)
    # adress = serializers.CharField(max_length=255)
    # country = serializers.CharField(max_length=100)
    # city = serializers.CharField(max_length=100)
    # state = serializers.CharField(max_length=100, default="Kinshasa")
    # type = serializers.CharField(max_length=30)
    # services = serializers.CharField(max_length=300)

    class Meta:
        model = Invoice
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['customer'] = CustomerSerializer(instance.customer).data
        return rep

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


class AllInvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['customer'] = CustomerSerializer(instance.customer).data
        return rep
    



class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

    


class AddInvoiceSerializer(serializers.Serializer):
    articles = ArticleSerializer(many=True)  # Serializer pour les articles
    concern = serializers.CharField(max_length=250)
    client = serializers.CharField(max_length=250)
    company = serializers.CharField(max_length=250)
    total = serializers.FloatField()


    class Meta:
        model = Invoice
        fields = '__all__'

    def create(self, validated_data):
        articles_data = validated_data.pop('articles')
        id_number = validated_data("client")
        concern = validated_data("concern")
        total = validated_data("total")
        company = validated_data("company")
        user = self.context['request'].user

        try:
            company = Company.objects.get(id_number=company)
        except Company.DoesNotExist:
            raise serializers.ValidationError("Company not found.")
        
        try:
            customer = Customer.objects.get(id_number=id_number)
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Customer not found.")
        
        invoice = Invoice.objects.create(
            customer=customer,
            concern = concern,
            save_by = user,
            total = total,
            company = company
        )

        for article_data in articles_data:
            Article.objects.create(invoice=invoice, **article_data)

        return invoice