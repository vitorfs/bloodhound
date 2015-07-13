from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'bloodhound.core.views.home', name='home')
]
