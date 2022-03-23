from django import template
from celebrities.models import *

register = template.Library()


@register.simple_tag(name='get_cats')
def get_categories(filter=None):
    if filter is None:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('celebrities/list_categories.html')
def show_categories(sort, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.all().order_by(sort)

    return {'cats': cats, 'cat_selected': cat_selected}
