from django.urls import path
# from accounts.views import (
#     LoginView, RegisterView, EmailConfirmationView, RendedEmailConfirmationView, CustomTokenObtainPairView
# )

from accounts.views import LoginView, RegisterView, EmailConfirmationView,RendedEmailConfirmationView, ChangePasswordAPIView, LogoutView

urlpatterns = [
    # path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password/reset/confirm', PasswordResetConfirmView.as_view(), name='password_confirm'),
    path('login/', LoginView.as_view(), name='login'),
#     path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email_confirm/<str:token>/', EmailConfirmationView.as_view(), name='email_confirm'),
    path('resend_email/', RendedEmailConfirmationView.as_view(), name='email_resent'),
    path('logout/', LogoutView.as_view(), name='logout'),
#     # path('user/', UserDetailsView.as_view(), name='user_details'),
    path('password/change/', ChangePasswordAPIView.as_view(), name='password_change'),
]