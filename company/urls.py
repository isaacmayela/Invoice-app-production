from django.urls import path

from company.views import CompanyView, CustomerView, InvoiceView, GetAllInvoices

urlpatterns = [
    path('informations/', CompanyView.as_view(), name='company'),
    path('informations/<str:id_number>', CompanyView.as_view(), name='company'),
    path('customers/', CustomerView.as_view(), name='company'),
    path('<str:cmp_id_number>/invoices/', InvoiceView.as_view(), name='company'),
    path('invoices/<str:cmp_id_number>/invoices/<str:inv_id_number>/', InvoiceView.as_view(), name='company'),
    path('invoice/delete/<int:id_number>/', InvoiceView.as_view(), name='invoice-delete'),
    path('all_invoices/', GetAllInvoices.as_view(), name='company'),
]