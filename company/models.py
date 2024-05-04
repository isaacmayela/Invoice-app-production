from django.db import models
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
import random
import string

def generate_id_number():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))

class Company(models.Model):
    
    name = models.CharField(max_length=132)
    email = models.EmailField()
    phone = models.CharField(max_length=132)
    adress = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default="Kinshasa")
    services = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    id_number = models.CharField(max_length=15, unique=True, default=generate_id_number())
    save_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
    def __str__(self):
        return self.name

class Customer(models.Model):

    name = models.CharField(max_length=132)
    email = models.EmailField()
    phone = models.CharField(max_length=132)
    adress = models.CharField(max_length=64)
    adress = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    type =models.CharField(max_length=30)
    services = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    id_number = models.CharField(max_length=15, unique=True, default=generate_id_number())
    save_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
    def __str__(self):
        return self.name


class Invoice(models.Model):

    INVOICE_TYPE = (
        ('P', ('PROFORMA INVOICE')),
        ('I', ('INVOICE'))
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    concern = models.CharField(max_length=200, default="nothing")
    save_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    invoice_date_time = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()
    last_updated_date = models.DateTimeField(null=True, blank=True)
    paid  = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    id_number = models.CharField(max_length=15, unique=True, default=generate_id_number())
    comments = models.TextField(null=True, max_length=1000, blank=True)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
           return f"{self.customer.name}_{self.invoice_date_time}"

    @property
    def get_total(self):
        articles = self.article_set.all()   
        total = sum(article.get_total for article in articles)
        return total   

class Article(models.Model):

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    details = models.CharField(max_length=60, default="nothing")
    unity = models.CharField(max_length=10)
    name = models.CharField(max_length=32)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    id_number = models.CharField(max_length=15, unique=True, default=generate_id_number())
    total = models.FloatField()

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    @property
    def get_total(self):
        total = self.quantity * self.unit_price 
        return total
    