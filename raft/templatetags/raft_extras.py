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


@register.filter
def vnd_to_usd(money):
    key = str(money)
    if cache.get(key, default=None) is None:
        conversion = convert_money(money, 'USD')
        conversion.amount = Decimal(
            conversion.amount
        ).quantize(Decimal('1.'), rounding=ROUND_HALF_EVEN)
        cache.set(key, conversion, 24 * 3600)
    return cache.get(key)
