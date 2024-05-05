from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.authtoken.models import Token
# from .utils import generate_username, send_email_confirmation, validate_email_token
# from .models import EmailConfirmationProfile, EmailConfirmationToken
from django.conf import settings
from django.template.loader import render_to_string
# from django.contrib.auth.models import User
# import jwt, datetime
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (CreatedUserSerializer, CustomTokenObtainPairSerializer, RegisterSerializer, EmailConfirmationSerializer, 
RendedEmailConfirmationSerializer, ChangePasswordSerializer, LogoutSerializer, AddCollaboratorsSerializer)
from .models import EmailConfirmationToken, CustomUser
from .utils import validate_email_token, generate_password
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config
from django.contrib.auth.models import Group, Permission


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data.get('refresh')
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'success': 'User logged out successfully'}, status=status.HTTP_200_OK)

# class LoginView(GenericAPIView):

#     permission_classes = (AllowAny,)
#     serializer_class = LoginSerializer
#     throttle_scope = 'accounts'

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data["user"]
#         try:
#             is_user_email_confirm = EmailConfirmationProfile.objects.get(user=user)
#             if not is_user_email_confirm.is_email_confirmed:
#                 raise ValueError
#         except (EmailConfirmationProfile.DoesNotExist, ValueError):
#             return Response({"message": "You must validate your email address before continuing."}, status=status.HTTP_400_BAD_REQUEST)
        
#         payload = {
#             "id":user.id,
#             "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=6),
#             "iat": datetime.datetime.utcnow()
#         }

#         token = jwt.encode(payload, 'secret', algorithm='HS256')
            
#         # token, created = Token.objects.get_or_create(user=user)
#         response = Response()

#         response.data = {
#             "token": token
#         }

#         response.set_cookie(key='jwt_token', value=token, httponly=True)

#         response.status_code = status.HTTP_200_OK

#         return response
#         return Response(
#             {
#                 "user": {
#                     "id": user.id,
#                     "username": user.username,
#                     "email": user.email,
#                     "first_name": user.first_name,
#                     "last_name":user.last_name
#                 },
#                 "token": token
#             }, 
#             status=status.HTTP_200_OK)
    
class RegisterView(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    throttle_scope = 'accounts'
    CORS_ORIGINS = config("CORS_ORIGINS")

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        group = Group.objects.get(name='administrator')
        user.groups.add(group)

        email_token, created = EmailConfirmationToken.objects.get_or_create(user=user, defaults={
            "token_type" : "activation"
        })

        # print(email_token)

        confirmation_url = f"""Félicitation, vous venez de creer votre compte ! 
                               Veuiller confirmer vos informations en cliquant sur ce lien {self.CORS_ORIGINS}/email-verification/{email_token.id}/"""

        subject = "Email de confirmation"

        template = "index.html"

        context = {'confirmation_url': confirmation_url}

        message =  render_to_string(template, context)

        user.email_user(subject, confirmation_url, settings.EMAIL_HOST_USER, **kwargs)

        return Response({"message": "The account has been successfully registered", "email":user.email}, status=status.HTTP_201_CREATED)


class EmailConfirmationView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailConfirmationSerializer

    def post(self, request, *args, **kwargs):

        token = self.kwargs.get('token')

        if not validate_email_token(token):
            return Response({"message": "Invalid Token."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            email_token = EmailConfirmationToken.objects.get(id=token)
        except EmailConfirmationToken.DoesNotExist:
            return Response({"message": "Invalid Token."}, status=status.HTTP_404_NOT_FOUND)

        is_user_email_confirm = CustomUser.objects.get(email=email_token.user.email)

        print(email_token.token_type)

        if email_token.token_type == "activation":

            is_user_email_confirm.is_active = True
            is_user_email_confirm.save()

            email_token.delete()

            return Response({'message': 'Account validated successfully.'}, status=status.HTTP_200_OK)

        email_token.delete()

        return Response({'message': 'Successful verification.'}, status=status.HTTP_200_OK)
    

class RendedEmailConfirmationView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RendedEmailConfirmationSerializer
    CORS_ORIGINS = config("CORS_ORIGINS")

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
            try:

                user_email_token = EmailConfirmationToken.objects.get(user=user)
                user_email_token.delete()
            except EmailConfirmationToken.DoesNotExist:
                pass

            email_token, created = EmailConfirmationToken.objects.get_or_create(user=user, defaults={
                "token_type" : "verification"
            })

            confirmation_url = f"Confirmez votre identité en cliquant sur ce lien {self.CORS_ORIGINS}/changePassword/{email_token.id}/"
            subject = "Email de confirmation"
            message =  render_to_string("index.html", {'confirmation_url': confirmation_url})

            user.email_user(subject, confirmation_url, settings.EMAIL_HOST_USER, **kwargs)
            print("token",email_token.id)

        except CustomUser.DoesNotExist:
            pass

        return Response({"message": "A new validation token has been created"}, status=status.HTTP_201_CREATED)
    
class ChangePasswordAPIView(GenericAPIView):

    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        new_password1 = serializer.validated_data['new_password1']

        if not validate_email_token(token):
            return Response({"message": "Invalid Token."}, status=status.HTTP_400_BAD_REQUEST)

        email_token = EmailConfirmationToken.objects.get(id=token)

        user = CustomUser.objects.get(email=email_token.user.email)

        if email_token.token_type == "verification":

            user.set_password(new_password1)
            user.save()
            
            email_token.delete()
            return Response({'message': 'Password has been chagnge succifuly.'}, status=status.HTTP_200_OK)

        email_token.delete()

        return Response({'message': 'Password has been chagnge succifuly.'}, status=status.HTTP_200_OK)


class AddCollaborators(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = AddCollaboratorsSerializer
    CORS_ORIGINS = config("CORS_ORIGINS")

    def post(self, request, *args, **kwargs):

        admin = request.user

        if not admin.groups.filter(name='administrator').exists() or not admin.is_superuser:
            return Response({"message": "You do not have the necessary authorizations."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']

        user = CustomUser.objects.create_user(email=email, password=generate_password(), first_name= first_name, last_name= last_name, attachement=admin.id_number)
        user.is_active = True
        user.save()

        group = Group.objects.get(name='collaborator')
        user.groups.add(group)

        confirmation_url = f"""
                                {admin.first_name} {admin.last_name} vous a ajouté comme collaborateur avec votre adrèsse mail {user.email} 
        Votre mot de passe temporaire est: {user.password} veuiller le modifier en suivant ce lien {self.CORS_ORIGINS}/login
                            """

        subject = "Email d'invitation"

        user.email_user(subject, confirmation_url, settings.EMAIL_HOST_USER, **kwargs)

        return Response({"message": "The account has been successfully registered", "email":user.email}, status=status.HTTP_201_CREATED)
    
class GetCreatedUsers(ListAPIView):
    serializer_class = CreatedUserSerializer
    permission_classes = [IsAuthenticated]

    def get_users_created_by(self, user):
        utilisateurs_crees = user.created_users.all()
        return utilisateurs_crees

    def list(self, request, *args, **kwargs):
        user = request.user

        if user.groups.filter(name='administrator').exists() or user.is_superuser:
            utilisateurs_crees = self.get_users_created_by(user)
            serializer = self.serializer_class(utilisateurs_crees, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "You do not have the necessary authorizations."}, status=status.HTTP_403_FORBIDDEN)

        


        
    