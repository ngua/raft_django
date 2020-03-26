import json
from decimal import Decimal, ROUND_HALF_EVEN
from django.core.cache import cache
from django.shortcuts import render
from django.forms import formset_factory
from django.db.models import Count
from django.http import JsonResponse
from django.views import View
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from honeypot.decorators import check_honeypot
from djmoney.contrib.exchange.models import convert_money
from .models import Category, Service
from .forms import EstimateForm, ContactForm
from .index import slider, switcher


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def index(request):
    context = {'switcher': switcher, 'slider': slider}
    return render(request, 'raft/index.html', context=context)


def services(request):
    categories = list(Category.objects.all())
    categories = sorted(
        categories,
        key=lambda x: len(list(x.service_set.all())),
        reverse=True
    )
    context = {'categories': categories}
    return render(request, 'raft/services.html', context=context)


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


class EstimateView(View):
    template_name = 'raft/estimate.html'
    categories = [
        category for category in Category.objects.annotate(
            num_services=Count('service')
        ).order_by('-num_services')
    ]
    cap = len(categories)
    form_class = formset_factory(
        form=EstimateForm,
        extra=cap,
        max_num=cap,
        validate_max=True
    )
    initial = [{'model_id': category.id} for category in categories]

    def get(self, request, *args, **kwargs):
        formset = self.form_class(initial=self.initial)
        context = {'formset': formset}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = self.form_class(request.POST, initial=self.initial)
        context = {'formset': formset}
        if formset.is_valid():
            selections = [
                form.cleaned_data['services']
                for form in formset if form.cleaned_data['services']
            ]
            ids = [int(id) for selection in selections for id in selection]
            services = [Service.objects.get(id=int(id)) for id in ids]
            total = EstimateForm.sum_price(*services)
            return JsonResponse({
                'success': True,
                'total': str(total),
                'services': [service.name for service in services]
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': {
                    form.model.id: form['services'].errors
                    for form in formset if form.errors
                }
            })
        return render(request, self.template_name, context)


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
