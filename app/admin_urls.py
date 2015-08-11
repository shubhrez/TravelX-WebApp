from django.conf.urls import patterns, url, include
import views.admin_views as views

urlpatterns = patterns('',

	url(r'^$', views.admin, name='admin'),
	url(r'^login/$', views.admin_login, name='login'),
	url(r'^logout/$', views.admin_logout, name='logout'),
	url(r'^home/$', views.home, name='home'),
    url(r'^all_category/$', views.show_categories, name='category'),
	url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^edit_category/(?P<id>\d+)/$', views.edit_category, name='edit_category'),
    url(r'^all_places/$', views.all_places, name='all_places'),
	url(r'^edit_place/(?P<id>\d+)/$', views.edit_place, name='edit_place'),
	url(r'^change_category_image/$', views.change_category_image, name='change_category_image'),
	url(r'^change_place_image/$', views.change_place_image, name='change_place_image'),
	url(r'^add_image_to_place_gallery/$', views.add_image_to_place_gallery, name='add_image_to_place_gallery'),
	)