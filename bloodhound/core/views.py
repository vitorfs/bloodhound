from django.views.generic import TemplateView, ListView

from bloodhound.core.models import Product


class Home(ListView):
    model = Product
    template_name = 'core/home.html'
    queryset = Product.objects.filter(status=Product.OK).order_by('-visited_at')
    paginate_by = 100
