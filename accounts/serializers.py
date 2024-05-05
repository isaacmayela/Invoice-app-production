from rest_framework import exceptions, serializers
from django.contrib.auth import authenticate, get_user_model
# from django.conf import settings
# from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import EmailConfirmationToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _

# # User = settings.AUTH_USER_MODEL

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email

        return token

# class LoginSerializer(serializers.Serializer):

#     email = serializers.EmailField()
#     password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

#     def validate(self, data):
#         email = data.get("email")
#         password = data.get("password")

#         if email and password:
#             user = User.objects.filter(email=email).first()
#             if user:
#                 if not user.check_password(password):
#                     raise serializers.ValidationError({'message': 'Invalid credentials'})
#                 if not user.is_active:
#                     raise serializers.ValidationError({'message': 'User is inactive'})
#             else:
#                 raise serializers.ValidationError({'message': 'User not found'})
#         else:
#             raise serializers.ValidationError({'message': 'Email and password are required'})

#         return data

#         # if email and password:
#         #     try:
#         #         user = User.objects.get(email=email)
#         #     except User.DoesNotExist:
#         #         user = None
            
#         #     if user:
#         #         user = authenticate(username=user.username, password=password)

#         #         if not user.is_active:
#         #             msg = "User account is disabled."
#         #             raise serializers.ValidationError(msg)
                
#         #         data["user"] = user
#         #         return data

#         #     else:
#         #         msg = "Unable to log in with provided credentials."
#         #         raise serializers.ValidationError(msg)
#         # else:
#         #     msg = "Must include 'email' and 'password'."
#         #     raise serializers.ValidationError(msg)
        
# class LoggedUserSerializer(serializers.Serializer):
#     """"
#     Serializer for User logged in
#     """
#     token = serializers.CharField(source='token.key')
#     first_name = serializers.CharField()
#     middle_name = serializers.CharField()
#     last_name = serializers.CharField()
#     user_type = serializers.CharField(source='employee_type')
#     number = serializers.CharField()
        
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
        
class RegisterSerializer(serializers.Serializer):
    # username = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=80, style={'input_type': 'password'})

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).first():
            raise serializers.ValidationError("An account using this email already exists.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):

        id_number = validated_data["id_number"]

        user = CustomUser.objects.create_user(
            **validated_data
        )

        user.attachement = id_number
        user.is_active = False
        user.save()

        return user
    
class EmailConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['is_active']

class RendedEmailConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # if not User.objects.filter(email=value).exists():
        #     raise serializers.ValidationError("Invalid email.")
        return value
    
class ChangePasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    _errors = {}
    user = None
    set_password_form = None

    def validate_token(self, value):
        
        try:
            check_token = EmailConfirmationToken.objects.get(id=value)
        except (EmailConfirmationToken.DoesNotExist):
            raise ValidationError({"Invalid token"})

        return value
    
    def validate(self, attrs):
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError("The two password didn’t match.")
        return attrs
    
    # def save(self, **kwargs):
    #     self.set_password_form = self.set_password_form_class(user=self.user, data=self.validated_data)
    #     if self.set_password_form.is_valid():
    #         self.set_password_form.save()
    #         return self.user
    #     else:
    #         self._errors = self.set_password_form.errors
    #         raise serializers.ValidationError("Erreur lors du changement de mot de passe.")


class AddCollaboratorsSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).first():
            raise serializers.ValidationError("An account using this email already exists.")
        return value
    

class CreatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name']