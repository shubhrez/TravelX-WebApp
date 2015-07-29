from django.conf.urls import patterns, url, include
import views.android_views as views

urlpatterns = patterns('',

	url(r'^categories/$', views.get_categories, name='get_categories'),

	)