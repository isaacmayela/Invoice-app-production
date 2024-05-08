from django.urls import path

from company.views import CompanyView, CustomerView, InvoiceView, GetAllInvoices, AddInvoiceView

urlpatterns = [
    path('informations/', CompanyView.as_view(), name='company'),
    path('informations/<str:id_number>', CompanyView.as_view(), name='company'),
    path('customers/', CustomerView.as_view(), name='company'),
    path('<str:cmp_id_number>/customers/', CustomerView.as_view(), name='customers'),
    path('customers/<str:cmp_id_number>/customers/<str:ctm_id_number>/', CustomerView.as_view(), name='customers'),
    path('<str:cmp_id_number>/invoices/', InvoiceView.as_view(), name='company'),
    path('invoices/<str:cmp_id_number>/invoices/<str:inv_id_number>/', InvoiceView.as_view(), name='company'),
    path('invoice/delete/<str:id_number>/', InvoiceView.as_view(), name='invoice-delete'),
    path('all_invoices/', GetAllInvoices.as_view(), name='company'),
    path('add_invoices/', AddInvoiceView.as_view(), name='add_invoice'),
]