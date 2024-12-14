from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Product, Cart

# Register Product and Category models with default ModelAdmin
admin.site.register(Product)
admin.site.register(Category)


# Custom UserAdmin for the User model
class CustomUserAdmin(UserAdmin):
    model = User

    # Fields to display in the admin list view
    list_display = ('email', 'first_name', 'last_name', 'mobile', 'is_active', 'is_staff', 'is_superuser')

    # Filters for the admin list view
    list_filter = ('is_active', 'is_staff', 'is_superuser')

    # Search functionality for the list view
    search_fields = ('email', 'first_name', 'last_name', 'mobile')

    # Default ordering in the list view
    ordering = ('email',)

    # Horizontal filter for related fields (not needed here but kept for flexibility)
    filter_horizontal = ()

    # Fieldsets for the detail view of a user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'mobile', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Fieldsets for the add user form in the admin interface
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'mobile', 'is_active', 'is_staff',
                       'is_superuser')}),
    )


# Register the custom user model with the admin interface
admin.site.register(User, CustomUserAdmin)


# Custom Admin for the Cart model
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view (removed added_at)
    list_display = ('id', 'user', 'product', 'quantity')

    # Fields for search functionality
    search_fields = ('user__email', 'product__name')

    # Filters for the admin list view (removed added_at)
    list_filter = ()

    # Optionally, specify ordering in the list view
    ordering = ('-id',)  # Show the most recent cart additions first by ID
