from rest_framework.permissions import BasePermission


class IsTheSameUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj=None):
        return request.user.is_authenticated() and request.user.pk == obj.pk


class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class DenyAll(BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated()


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated() and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated() and request.user.is_superuser


class UserPermissions(BasePermission):
    enough_perms = AllowAny()
    global_perms = None
    retrieve_perms = IsTheSameUser()
    update_perms = IsTheSameUser()
    partial_update_perms = IsTheSameUser()
    destroy_perms = IsTheSameUser()
    list_perms = AllowAny()
    login_perms = AllowAny()
    logout_perms = IsAuthenticated()
    password_change_perms = AllowAny()
    register_perms = AllowAny()
    registered_list_perms = AllowAny()
    categories_perms = AllowAny()
    product_perms = AllowAny()
