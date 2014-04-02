from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.views.generic import ListView, DetailView
from information.models import Information as Info
from shopping_cart.models import Product

from django.contrib.auth.views import login


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', '_.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',
        DetailView.as_view( model=Info ),
        kwargs={'pk':1},
        name='index',
        ),
    url(r'^products/$',
        ListView.as_view( model=Product ),
        name='products',
        ),
    url(r'^login/$',
        login,
        kwargs={'template_name':'auth/login.html'},
        name='login',
        ),
    url(r'^order/$',
        'shopping_cart.views.order',
        name='order',
        ),
)
