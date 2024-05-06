from django.shortcuts import render
from rest_framework import  generics, mixins
from .models import Company, Customer
from .serializer import CompanySerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.permissions import EditorPermissionsMixins

# Create your views here.

class CompanyView(EditorPermissionsMixins, generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin, 
    mixins.ListModelMixin,mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = "pk"

    def perform_create(self, serializer):
        # serializer.save(save_by=self.request.user)
        company = serializer.save(save_by=self.request.user)
        company.users.add(self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Company.objects.filter(users=user)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        if pk is not None:  
            return self.retrieve(request, *args, **kwargs)    
         
        return self.list(request, *args, **kwargs)
    
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
    
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = "pk"

    def perform_create(self, serializer):
        serializer.save(save_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
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
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
