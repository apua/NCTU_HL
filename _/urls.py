from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from information.models import Information as Info
from shopping_cart.models import Product

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

    #url(r'^$', 'information.views.home'),
    #url(r'^products/', 'shopping_cart.views.list_product'),
    url(r'^order/$', 'shopping_cart.views.order'),
    url(r'^login/$','shopping_cart.views.login_signup'),
)
