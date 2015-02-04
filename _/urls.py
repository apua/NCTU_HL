from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from django.contrib.auth import views

from django.views.generic import ListView, DetailView
from information.models import Information as Info
from shopping_cart.models import Product


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', '_.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^nuclear_bomb/$',
        'email_auth.views.clean_database',
        name='clean_database'),

    url(r'^signup/$',
        'email_auth.views.signup',
        name='signup'),

    url(r'^signupdone/$',
        'email_auth.views.signup_done',
        name='signup_done'),

    url(r'^signupconfirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        'email_auth.views.signup_confirm',
        name='signup_confirm'),

    url(r'^passreset/$',
        views.password_reset, kwargs={'template_name':'auth/passreset.html'},
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

    url(r'^logout/$',
        'email_auth.views.logout_view',
        name='logout'),

    url(r'^$',
        DetailView.as_view( model=Info ),
        kwargs={'pk':1},
        name='index'),

    url(r'^products/$',
        ListView.as_view( model=Product ),
        name='products'),

    url(r'^order/$',
        'shopping_cart.views.order',
        name='order'),

    url(r'^statistics/$',
        'nctuhl_statistics.views.statistics_index',
        name='statistics_index'),

    url(r'^statistics/products$',
        'nctuhl_statistics.views.statistics_products',
        name='statistics_products'),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT})
    )
