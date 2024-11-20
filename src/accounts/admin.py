from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Product
admin.site.register(Product)
admin.site.register(Category)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'mobile', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'mobile')
    ordering = ('email',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'mobile', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'mobile', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

# Register the custom user model with the admin interface
admin.site.register(User, CustomUserAdmin)
