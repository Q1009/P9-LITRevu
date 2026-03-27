from django.template import Library

register = Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.simple_tag(takes_context=True)
def get_user_display(context, user):
    if context['user'] == user:
        return 'Vous avez'
    return f'{user.username} a'


@register.filter
def rating_stars(value):
    return '★' * value + '☆' * (5 - value)
