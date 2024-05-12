from django.shortcuts import render
from rest_framework import  generics, mixins
from .models import Company, Customer, Invoice, Article
from .serializer import CompanySerializer, CustomerSerializer, InvoiceSerializer, AllInvoiceSerializer, AddInvoiceSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.permissions import EditorPermissionsMixins
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

class CompanyView(EditorPermissionsMixins, generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, 
    mixins.ListModelMixin,mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = "id_number"

    def perform_create(self, serializer):
        # serializer.save(save_by=self.request.user)
        company = serializer.save(save_by=self.request.user)
        company.users.add(self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Company.objects.filter(users=user)

    
    def get(self, request, *args, **kwargs):
        id_number = kwargs.get("id_number")

        if id_number is not None:
            company = Company.objects.filter(id_number=id_number).first()
            if company:
                serializer = self.get_serializer(company)
                return Response(serializer.data)
            else:
                return Response({"message": "Company not found"}, status=404)

        return self.list(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        companies = self.get_queryset()
        data = []
        
        for company in companies:
            paid_invoices = Invoice.objects.filter(company=company,paid=True).count()
            unpaid_invoices = Invoice.objects.filter(company=company,paid=False).count()
            
            serializer = self.get_serializer(company)
            company_data = serializer.data
            company_data["paid_invoices"] = paid_invoices
            company_data["unpaid_invoices"] = unpaid_invoices
            
            data.append(company_data)
        
        return Response(data)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    

class CustomerView(EditorPermissionsMixins, generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, 
    mixins.ListModelMixin,mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = "pk"

    def perform_create(self, serializer):
        serializer.save(save_by=self.request.user)

    # def get_queryset(self):
    #     user = self.request.user
    #     return Customer.objects.filter(save_by=user)
    
    def get_queryset(self):
        user = self.request.user
        cmp_id_number = self.kwargs.get('cmp_id_number')
        ctm_id_number = self.kwargs.get('ctm_id_number')

        if ctm_id_number:
            return Customer.objects.filter(id_number=ctm_id_number).first()
        elif cmp_id_number and not ctm_id_number:
            try:
                company = Company.objects.get(id_number=cmp_id_number)
                return Customer.objects.filter(company=company)
            except Company.DoesNotExist:
                return Customer.objects.none()
        return Customer.objects.filter(save_by=user)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        if pk is not None:  
            return self.retrieve(request, *args, **kwargs)    
         
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        id_number = kwargs.get('id_number')
        try:
            company = Company.objects.get(id_number=id_number)
            company.delete()
            return Response({'message': 'Company deleted successfuly'}, status=status.HTTP_204_NO_CONTENT)
        except Invoice.DoesNotExist:
            return Response({'message': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)



class InvoiceView(EditorPermissionsMixins, generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, 
    mixins.ListModelMixin,mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = "pk"

    def perform_create(self, serializer):
        serializer.save(save_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        cmp_id_number = self.kwargs.get('cmp_id_number')
        inv_id_number = self.kwargs.get('inv_id_number')

        if inv_id_number:
            return Invoice.objects.filter(id_number=inv_id_number)
        else:
            try:
                company = Company.objects.get(id_number=cmp_id_number)
                return Invoice.objects.filter(company=company)
            except Company.DoesNotExist:
                return Invoice.objects.none()
        
    

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        if pk is not None:  
            return self.retrieve(request, *args, **kwargs)    
         
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        id_number = kwargs.get('id_number')
        try:
            invoice = Invoice.objects.get(id_number=id_number)
            invoice.delete()
            return Response({'message': 'Invoice deleted successfuly'}, status=status.HTTP_204_NO_CONTENT)
        except Invoice.DoesNotExist:
            return Response({'message': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    


class GetAllInvoices(EditorPermissionsMixins, generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    
    queryset = Invoice.objects.all()
    serializer_class = AllInvoiceSerializer
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        return Invoice.objects.filter(save_by=user)
        
    
    def get(self, request, *args, **kwargs):       
        return self.list(request, *args, **kwargs)
    

class AddInvoiceView(EditorPermissionsMixins, generics.GenericAPIView,  mixins.CreateModelMixin):
    # queryset = Invoice.objects.all()
    serializer_class = AddInvoiceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(save_by=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def post(self, request, format=None):
    #     serializer = self.serializer_class(data=request.data, context={'save_by': request.user})

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
