# Django
from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='sector')
def sector(user, group_name):
    # group = Group.objects.get(name=group_name)
    # return True if group in user.groups.all() else False
    # para comentar en este es control shift 7


        try: 
            group = Group.objects.get(name=group_name)
            return True if group in user.groups.all() else False
        except Group.DoesNotExist:
            return False    
