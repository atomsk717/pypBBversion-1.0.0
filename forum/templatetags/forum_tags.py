from django import template

register = template.Library()


@register.filter
def is_moderator(user):
    if not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    return user.groups.filter(name='Moderator').exists()


@register.filter
def is_forum_admin(user):
    if not user.is_authenticated:
        return False
    return user.is_staff or user.is_superuser


@register.filter
def role_class(user):
    if not user.is_authenticated:
        return ""
    if user.is_staff or user.is_superuser:
        return "role-admin"
    if user.groups.filter(name='Moderator').exists():
        return "role-moderator"
    return ""