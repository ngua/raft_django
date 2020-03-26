from decimal import Decimal, ROUND_HALF_EVEN
from django import template
from djmoney.contrib.exchange.models import convert_money
from django.core.cache import cache


register = template.Library()


@register.filter
def slice_url(url):
    prefix = url[1:3]
    if prefix not in ['en', 'vi']:
        return url
    return url[3:]
