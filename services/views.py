from django.shortcuts import render
from django.http import JsonResponse
from django.forms import formset_factory
from django.db.models import Count, Q
from django.views import View
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Category, Service
from .forms import EstimateForm


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class EstimateView(View):
    template_name = 'services/estimate.html'
    categories = [
        category for category in Category.objects.annotate(
            num_services=Count(
                'service', filter=Q(service__price__gt=0)
            )).exclude(num_services__lt=1).order_by('-num_services')
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


@cache_page(CACHE_TTL)
def services(request):
    categories = list(Category.objects.all())
    categories = sorted(
        categories,
        key=lambda x: len(list(x.service_set.all())),
        reverse=True
    )
    context = {'categories': categories}
    return render(request, 'services/services.html', context=context)
