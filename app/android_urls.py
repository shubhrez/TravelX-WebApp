from django.conf.urls import patterns, url, include
import views.android_views as views

urlpatterns = patterns('',

	url(r'^get_categories/$', views.get_categories, name='get_categories'),
	url(r'^get_places/$', views.get_places, name='get_places'),
	url(r'^get_place_details/$', views.get_place_details, name='get_place_details'),
	url(r'^register_app_id/$', views.register_app_id, name='register_app_id'),
	url(r'^get_search_results/$', views.get_search_results, name='get_search_results'),
	url(r'^rate_place/$', views.rate_place, name='rate_place'),
	url(r'^comfirm_booking/$', views.comfirm_booking, name='comfirm_booking'),
	)