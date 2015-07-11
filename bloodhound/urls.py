from django.conf.urls import include, url

from bloodhound.core.views import Home


urlpatterns = [
    url(r'^$', Home.as_view(), name='home')
]
