from rest_framework.permissions import BasePermission


# class IsAdmin(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == 'admin'

# class IsCustomer(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role in ('customer', 'vendor')


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "admin"
        )


class IsVendor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "vendor"
        )


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "customer"
        )


class IsOwnerVendor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.vendor == request.user