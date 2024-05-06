from django.contrib import admin
from .models import Company, Customer, Invoice, Article

# Register your models here.
admin.site.register(Company)
admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(Article)