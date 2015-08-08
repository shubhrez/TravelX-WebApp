from django.conf.urls import patterns, url, include
import views.admin_views as views

urlpatterns = patterns('',

	url(r'^login/$', views.admin_login, name='login'),
	url(r'^logout/$', views.admin_logout, name='logout'),
	url(r'^test/$', views.test, name='test'),
	)