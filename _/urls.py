from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', '_.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'information.views.home'),
    url(r'^products/', 'shopping_cart.views.list_product'),
    url(r'^order/', 'shopping_cart.views.order'),
    url(r'^signup/','shopping_cart.views.signup'),
)
