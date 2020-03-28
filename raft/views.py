import json
from decimal import Decimal, ROUND_HALF_EVEN
from django.core.cache import cache
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from honeypot.decorators import check_honeypot
from djmoney.contrib.exchange.models import convert_money
from services.models import Service
from .forms import ContactForm
from .index import slider, switcher
from .about import about_us


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def index(request):
    context = {'switcher': switcher, 'slider': slider}
    return render(request, 'raft/index.html', context=context)


# @cache_page(CACHE_TTL)
def about(request):
    context = {'content': about_us}
    return render(request, 'raft/about.html', context=context)


@csrf_exempt
@require_POST
def convert_currency(request):
    services = Service.objects.all()
    currency = json.loads(request.body).get('currency')
    if currency == 'vnd':
        response = {service.id: str(service.price) for service in services}
    else:
        response = {}
        for service in services:
            price = service.price
            key = str(price)
            if cache.get(key, default=None) is None:
                conversion = convert_money(price, 'USD')
                conversion.amount = Decimal((
                    Decimal(conversion.amount).quantize(
                        Decimal('1.'), rounding=ROUND_HALF_EVEN
                    ) // 5
                ) * 5)
                cache.set(key, conversion, 24 * 3600)
            response.update({service.id: str(cache.get(key))})
    return JsonResponse(response)


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class ContactView(FormView):
    template_name = 'raft/contact.html'
    form_class = ContactForm
    success_url = '/'

    @method_decorator(check_honeypot)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        form.send_email()
        return super().form_valid(form)
