import json
from django.shortcuts import render
from django.contrib.staticfiles import finders
from django.forms import formset_factory
from django.db.models import Count
from .models import Category
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
        max_num=len(categories)
    )
    formset = EstimateFormset(
        initial=[{'model_id': category.id} for category in categories]
    )
    context = {'formset': formset}
    return render(request, 'raft/estimate.html', context=context)
