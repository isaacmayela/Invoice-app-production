from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailConfirmationToken
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = '__all__'
        # Exclude the username field
        exclude = ('username',)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = '__all__'
        # Exclude the username field
        exclude = ('username',)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser','date_joined', 'get_groups')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Infos', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Groups'
    

# admin.site.unregister(Group)
admin.site.register(EmailConfirmationToken)
admin.site.register(CustomUser)
