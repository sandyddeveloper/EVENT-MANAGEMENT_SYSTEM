from rest_framework.permissions import BasePermission

class IsAttendee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_attendee

class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_organizer

class IsNotLocked(BasePermission):
    def has_permission(self, request, view):
        email = request.data.get('email')
        from django.core.cache import cache
        return not cache.get(f"{email}_locked", False)
