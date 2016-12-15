from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'campusballot.views.home', name='home'),
    url(r'^', include('group.urls', namespace="group")),
    url(r'^admin/', include(admin.site.urls)),
)
