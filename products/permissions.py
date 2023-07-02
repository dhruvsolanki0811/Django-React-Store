from rest_framework import permissions

class isAdminOnlyOrGetOnly(permissions.BasePermission):
    message =  'Only admin allowed to change,delete or create.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # return bool(request.user and request.user.is_staff)
            return True
class IsReviewUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.review_user == request.user or request.user.is_staff