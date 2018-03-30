from django import template
from django.contrib.auth.models import Group 
register = template.Library()

@register.filter(name='range')
def _range(_min, args=None):
    _max, _step = None, None
    if args:
        if not isinstance(args, int):
            _max, _step = map(int, args.split(','))
        else:
            _max = args
    args = filter(None, (_min, _max, _step))
    return range(*args)

@register.filter(name='times') 
def times(number):
    return range(int(number))


@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all()     

    