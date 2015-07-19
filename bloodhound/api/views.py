from django.shortcuts import render

from bloodhound.core.models import Product, PriceHistory
from bloodhound.sniffer.crawler import Bloodhound


def product(request):
    product_code = request.GET.get('code')
    try:
        product = Product.objects.get(code=product_code)
    except Product.DoesNotExist:
        product = Product(code=product_code)
        crawler = Bloodhound()
        product = crawler.howl(product)
    if product.status == Product.OK:
        lowest_price = PriceHistory.objects.filter(product=product).order_by('price')[0]
        highest_price = PriceHistory.objects.filter(product=product).order_by('-price')[0]
        return render(request, 'api/product.html', { 
                'product': product,
                'lowest_price': lowest_price,
                'highest_price': highest_price
            })
    else:
        return render(request, 'api/product_not_found.html')
        