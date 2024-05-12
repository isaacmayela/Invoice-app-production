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
        fields = ["name", "email", "phone", "adress", "country", "city", "state", "services", "id_number"]

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.adress = validated_data.get('adress', instance.adress)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('city', instance.state)
        instance.services = validated_data.get('services', instance.services)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()


class CustomerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=132)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=132)
    adress = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100, default="Kinshasa")
    services = serializers.CharField(max_length=300)
    id_number = serializers.CharField(max_length=300)


    def create(self, validated_data):
        name = validated_data['name']
        email = validated_data['email']
        phone = validated_data['phone']
        adress = validated_data['adress']
        country = validated_data["country"]
        city = validated_data["city"]
        state = validated_data["state"]
        services = validated_data["services"]
        id_number = validated_data["id_number"]

        try:
            company = Company.objects.get(id_number=id_number)
        except Company.DoesNotExist:
            raise serializers.ValidationError("Company not found.")
        
        customer = Customer.objects.create(
            name = name,
            email = email,
            phone = phone,
            adress = adress,
            country = country,
            city = city,
            state = state,
            services = services,
            company = company,
            save_by = self.context['save_by'],
        )

        return customer

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.adress = validated_data.get('adress', instance.adress)
    #     instance.country = validated_data.get('country', instance.country)
    #     instance.city = validated_data.get('city', instance.city)
    #     instance.services = validated_data.get('services', instance.services)
    #     instance.save()
    #     return instance

    # def delete(self, instance):
    #     instance.delete()


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
        fields = ['name', 'unity', 'quantity', 'unit_price', 'total', 'details']

    


class AddInvoiceSerializer(serializers.Serializer):
    articles = ArticleSerializer(many=True)  # Serializer pour les articles
    concern = serializers.CharField(max_length=250)
    client = serializers.CharField(max_length=250)
    company = serializers.CharField(max_length=250)
    total = serializers.FloatField()

    def create(self, validated_data):
        articles_data = validated_data.pop('articles')
        client_id = validated_data['client']
        concern = validated_data['concern']
        total = validated_data['total']
        company_id = validated_data['company']

        try:
            company = Company.objects.get(id_number=company_id)
        except Company.DoesNotExist:
            raise serializers.ValidationError("Company not found.")
        
        try:
            customer = Customer.objects.get(id_number=client_id)
        except Customer.DoesNotExist:
            raise serializers.ValidationError("Customer not found.")
        
        invoice = Invoice.objects.create(
            customer=customer,
            concern = concern,
            # save_by = user,
            # save_by = self.context['save_by'],
            total = total,
            company = company
        )

        for article_data in articles_data:
            Article.objects.create(invoice=invoice, **article_data)

        return invoice