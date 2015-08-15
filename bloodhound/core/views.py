# coding: utf-8

import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse as r
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from bloodhound.core.models import Product
from bloodhound.sniffer.crawler import Bloodhound


def products_list(request):
    queryset = Product.objects.filter(status=Product.OK)

    querystring = request.GET.get('q')
    if querystring:
        queryset = queryset.filter(Q(name__icontains=querystring) | Q(code__icontains=querystring) | Q(manufacturer__icontains=querystring) | Q(manufacturer_code__icontains=querystring))

    default_order = 'price_percentage_variance'
    order = request.GET.get('o', default_order)
    if order not in ['name', '-name', 
                     'code', '-code', 
                     'current_price', '-current_price', 
                     'price_changes', '-price_changes', 
                     'price_percentage_variance', '-price_percentage_variance', 
                     'visited_at', '-visited_at',]:
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

    sorting_labels = {
        'name': 'Name (a - z)',
        '-name': 'Name (z - a)',
        'price_percentage_variance': 'Greater prices decreases',
        '-price_percentage_variance': 'Greater prices increases',
        'current_price': 'Lowest prices',
        '-current_price': 'Highest prices',
        '-price_changes': 'Most variances',
        '-visited_at': 'Recently visited',
    }

    label_sort_by = sorting_labels[order]

    return render(request, 'core/products_list.html', { 
            'products': products, 
            'order': order, 
            'querystring': querystring,
            'label_sort_by': label_sort_by
        })

def product_details(request, code):
    try:
        product = Product.objects.get(code=code)
    except Product.DoesNotExist:
        crawler = Bloodhound()
        product = Product(code=code)
        product = crawler.howl(product)

    if product.status == Product.OK:
        price_history_chart = product.price_history.all().order_by('created_at')
        return render(request, 'core/product_details.html', { 
                'product': product,
                'price_history_chart': price_history_chart
            })
    else:
        messages.error(request, u'Product with code {0} was not found.'.format(code))
        return redirect(r('home'))

@require_POST
def product_refresh(request, code):
    try:
        product = Product.objects.get(code=code)
        crawler = Bloodhound()
        crawler.howl(product)
        return redirect(r('product', args=(code,)))
    except Product.DoesNotExist:
        messages.error(request, u'Product with code {0} was not found.'.format(code))
        return redirect(r('home'))

def hot(request):
    today = datetime.datetime.today()
    today = datetime.datetime(today.year, today.month, today.day)
    products = Product.objects.filter(status=Product.OK, price_percentage_variance__lt=0.0, updated_at__gt=today).order_by('price_percentage_variance')
    return render(request, 'core/hot.html', { 
            'products': products 
        })
