from django.conf.urls import patterns, include, url

urlpatterns = patterns('bloodhound.api.views',
    url(r'^product/$', 'product', name='product'),
)
