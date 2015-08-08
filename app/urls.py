from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import admin_views as views

admin.site.login = views.admin_login

urlpatterns = patterns('',

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^android/', include('app.android_urls')),
    url(r'^admin/', include('app.admin_urls')),
)