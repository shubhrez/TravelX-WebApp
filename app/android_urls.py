from django.conf.urls import patterns, url, include
import views.android_views as views

urlpatterns = patterns('',

	url(r'^get_categories/$', views.get_categories, name='get_categories'),
	url(r'^get_places/$', views.get_places, name='get_places'),

	)