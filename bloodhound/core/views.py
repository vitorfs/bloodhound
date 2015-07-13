from django.views.generic import TemplateView, ListView

from bloodhound.core.models import Product


class Home(ListView):
    model = Product
    template_name = 'core/home.html'
    queryset = Product.objects.filter(status=Product.OK)
    paginate_by = 100
