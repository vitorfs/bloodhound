# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from bloodhound.core.models import Product


def home(request):
    queryset = Product.objects.filter(status=Product.OK)

    querystring = request.GET.get('q')
    if querystring:
        queryset = queryset.filter(name__icontains=querystring)

    default_order = '-visited_at'
    order = request.GET.get('o', default_order)
    if order not in ['name', '-name', 'current_price', '-current_price', '-price_changes', 'price_percentage_variance', '-price_percentage_variance']:
        order = default_order
    queryset = queryset.order_by(order)

    paginator = Paginator(queryset, 100)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'core/home.html', { 
            'products': products, 
            'order': order, 
            'querystring': querystring 
        })
