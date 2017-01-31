from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zyrl_square_pos.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^zyrl-admin/$', 'square_sys.views.adminIndex', name="zyrl-admin"),
    url(r'^customer/(?P<uid>[-\w]+)/$', 'square_sys.views.customer_details', name="customer-details"),
    url(r'^$', 'square_sys.views.index', name="home"),
    url(r'^callback/$', 'square_sys.views.callback', name="callback"),
    url(r'^admin/', include(admin.site.urls)),
)
