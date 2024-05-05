from django.db import models
# from django.contrib.auth.models import User
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from .manager import UserManager
from django.utils import timezone
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _
import random
import string

# Create your models here.

def generate_id_number():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))

class CustomUser(AbstractUser, PermissionsMixin):

    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=200, default="username")
    id_number = models.CharField(max_length=15, unique=True, default=generate_id_number())
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    attachement = models.CharField(max_length=15, default="e310-8f32-425b")
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def email_user(self, subject, message, from_email, **kwargs):
        """Send an email to this user."""
        email = EmailMessage(
            subject = subject,
            body=message,
            from_email=from_email,
            to=[self.email],
            reply_to=[from_email],
            headers={'Content-Type': 'text/plain'},
        )
        email.send()

    @property
    def _default_manager(self):
        return self.objects

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name
    
    # def __str__(self):
    #     return self.email

# class Patron(Group):
#     class Meta:
#         verbose_name = _('Patron')
#         verbose_name_plural = _('Patrons')

# class Employee(Group):
#     class Meta:
#         verbose_name = _('Employee')
#         verbose_name_plural = _('Employees')


# class EmailConfirmationProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     is_email_confirmed = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.username

class EmailConfirmationToken(models.Model):
    TOKEN_TYPES = (
        ('activation', 'activation'),
        ('verification', 'verification'),
    )

    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token_type = models.CharField(max_length=20,choices=TOKEN_TYPES)
    
    def __str__(self):
        return self.user.email
    