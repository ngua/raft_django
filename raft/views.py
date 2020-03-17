import json
from django.shortcuts import render
from django.contrib.staticfiles import finders
from django.forms import formset_factory
from django.db.models import Count
from django.http import JsonResponse
from .models import Category, Service
from .forms import EstimateForm


def index(request):
    switcher_path = finders.find('raft/data/index_switcher.json')
    slider_path = finders.find('raft/data/index_slider.json')
    with open(switcher_path, 'r') as f:
        switcher = json.load(f)
    with open(slider_path, 'r') as f2:
        slider = json.load(f2)
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
            service_ids = [form.cleaned_data['services'] for form in formset]
            services = [
                Service.objects.get(id=service_id)
                for service_id in service_ids
            ]
            total = Service.sum_price(*services)
            response = {'success': True, 'total': str(total)}
        else:
            response = {
                'success': False,
                'errors': {form.model.id: form['services'].errors for form in formset if form.errors}
            }
            print(response)
        return JsonResponse(response)
    elif request.method == 'GET':
        formset = EstimateFormset(
            initial=[{'model_id': category.id} for category in categories]
        )
    context = {'formset': formset}
    return render(request, 'raft/estimate.html', context=context)
