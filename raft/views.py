from django.shortcuts import render
from django.forms import formset_factory
from django.db.models import Count
from django.http import JsonResponse
from django.views.generic.edit import FormView
from .models import Category, Service, Contact
from .forms import EstimateForm, ContactForm
from .index import slider, switcher


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


def estimate(request):
    categories = [
        category for category in Category.objects.annotate(
            num_services=Count('service')
        ).order_by('-num_services')
    ]
    EstimateFormset = formset_factory(
        form=EstimateForm,
        extra=len(categories),
        max_num=len(categories),
        validate_max=True
    )
    if request.method == 'POST':
        formset = EstimateFormset(
            request.POST,
            initial=[{'model_id': category.id} for category in categories]
        )
        if formset.is_valid():
            selections = [
                form.cleaned_data['services']
                for form in formset if form.cleaned_data['services']
            ]
            ids = [int(id) for selection in selections for id in selection]
            services = [Service.objects.get(id=int(id)) for id in ids]
            total = EstimateForm.sum_price(*services)
            response = {
                'success': True,
                'total': str(total),
                'services': [service.name for service in services]
            }
        else:
            response = {
                'success': False,
                'errors': {
                    form.model.id: form['services'].errors
                    for form in formset if form.errors
                }
            }
        return JsonResponse(response)
    elif request.method == 'GET':
        formset = EstimateFormset(
            initial=[{'model_id': category.id} for category in categories]
        )
    context = {'formset': formset}
    return render(request, 'raft/estimate.html', context=context)


class ContactView(FormView):
    template_name = 'raft/contact.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
