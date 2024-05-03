from django.urls import path

from company.views import CompanyView

urlpatterns = [
    path('informations/', CompanyView.as_view(), name='company'),

]