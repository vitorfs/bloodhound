from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'bloodhound.core.views.products_list', name='home'),
    url(r'^products/$', 'bloodhound.core.views.products_list', name='products'),
    url(r'^products/(\d+)/$', 'bloodhound.core.views.product_details', name='product'),
    url(r'^products/(\d+)/refresh/$', 'bloodhound.core.views.product_refresh', name='refresh'),
    url(r'^hot/$', 'bloodhound.core.views.hot', name='hot'),
    url(r'^api/', include('bloodhound.api.urls', namespace='api')),
]
