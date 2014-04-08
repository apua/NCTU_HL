from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.views.generic import ListView, DetailView
from information.models import Information as Info
from shopping_cart.models import Product

<<<<<<< local
from django.contrib.auth import views
=======
from django.contrib.auth.views import login, password_reset
>>>>>>> other


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', '_.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
<<<<<<< local
=======
    url(r'^/accounts/password/reset/$', password_reset,
        name='admin_password_reset'),
>>>>>>> other

<<<<<<< local
    url(r'^passreset/$',
        views.password_reset,
        name='admin_password_reset'),
    url(r'^passresetdone/$',
        views.password_reset_done,
        name='password_reset_done'),
    url(r'^passresetconfirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^passresetcomplete/$',
        views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^login/$',
        views.login, kwargs={'template_name':'auth/login.html'},
        name='login'),

=======
>>>>>>> other
    url(r'^$',
        DetailView.as_view( model=Info ),
        kwargs={'pk':1},
        name='index',
        ),
    url(r'^products/$',
        ListView.as_view( model=Product ),
        name='products',
        ),
    url(r'^order/$',
        'shopping_cart.views.order',
        name='order',
        ),
)
