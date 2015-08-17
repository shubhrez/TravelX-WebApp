from django.conf.urls import patterns, url, include
import views.android_views as views

urlpatterns = patterns('',

	url(r'^get_categories/$', views.get_categories, name='get_categories'),
	url(r'^get_places/$', views.get_places, name='get_places'),
	url(r'^get_place_details/$', views.get_place_details, name='get_place_details'),
	url(r'^register_app_id/$', views.register_app_id, name='register_app_id'),
	)