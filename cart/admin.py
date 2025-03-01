from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser')
    ordering = ('email',)  # ✅ Use 'email' instead of 'username'

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),  # ✅ Removed 'date_joined'
    )

    readonly_fields = ('date_joined', 'last_login')  # ✅ Mark `date_joined` as readonly


# Register the CustomUser model with CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
