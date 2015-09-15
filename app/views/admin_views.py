import simplejson
from app.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import urllib
import datetime as dt
from django.contrib import messages
import os
from django.contrib.admin.models import LogEntry, ADDITION,CHANGE,DELETION,ContentType
from gcm import GCM
from app.utils import constant
import time
from app.utils import send_mail
from django.core.exceptions import PermissionDenied
import shutil

def admin(request):
	return HttpResponseRedirect('/admin/login/')

def admin_login(request):
	if request.user.is_authenticated() and request.user.is_staff:
		return HttpResponseRedirect('/admin/home')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user:
			if user.is_active and user.is_staff:
				login(request,user)
				return HttpResponseRedirect('/admin/home/')
			else:
				return HttpResponse("Your Account is disabled")
		else:
			messages.warning(request,'Invalid Login Details')
			return render(request,'login.html')

	return render(request,'login.html')

def admin_logout(request):
	logout(request)
	return HttpResponseRedirect('/admin/login/')

@login_required(login_url='/admin/login/')
def home(request):
	context ={}
	return render(request, 'dashboard.html', context)

@login_required(login_url='/admin/login/')
def show_categories(request):
	categories = Category.objects.all()
	context = {
		'categories' : categories,
	}
	return render(request,'all_category.html',context)

@login_required(login_url='/admin/login/')
def edit_category(request,id):
	category = Category.objects.get(pk=id)
	locations = Location.objects.all()
	selected_location = category.location.all()

	context={
		'category' : category,
		'locations' : locations,
		'selected_location' : selected_location,
	}
	if request.method == "POST":
		name = request.POST.get('name','')
		is_active = request.POST.get('is_active','')
		location_id = request.POST.get('location','')
		print location_id
		location = Location.objects.get(pk=location_id)
		print location
		category.name = name
		is_active_value = False
		if is_active == 'on':
			is_active_value = True
		category.is_active = is_active_value
		category.location.add(location)
		category.save()
		print "hello"
		send_mail.notify_admin()

		LogEntry.objects.log_action(
			user_id         = request.user.pk,
			content_type_id = ContentType.objects.get_for_model(category).pk,
			object_id       = category.pk,
			object_repr     = str(category),
			action_flag     = CHANGE,
			change_message="Changed Category" + str(category.pk)
		)
		messages.success(request, 'Category Saved')
	return render(request,'edit_category.html',context)

@login_required(login_url='/admin/login/')
def all_places(request):
	places = Place.objects.all()
	context={
		'places':places,
	}
	return render(request,'all_places.html',context)

@login_required(login_url='/admin/login/')
def edit_place(request,id):
	place = Place.objects.get(pk=id)
	categories = Category.objects.all()
	selected_cat = place.category
	description = Description.objects.filter(place=place)
	context={
		'place' : place,
		'categories' : categories,
		'selected_cat' : selected_cat,
		'description' : description,
	}

	if request.method == "POST":
		if request.user.has_perm('app.change_place'):
			name = request.POST.get('name','')
			is_active = request.POST.get('is_active','')
			short_description = request.POST.get('short_description','')
			duration = request.POST.get('duration','')
			budget = request.POST.get('budget','')

			category_id = request.POST.get('category','')
			category = Category.objects.get(pk=category_id)

			is_active_value = False
			if is_active == 'on':
				is_active_value = True
			place.is_active = is_active_value
			place.name = name
			place.short_description = short_description
			place.duration = duration
			place.budget = budget
			place.category=category
			place.save()
			LogEntry.objects.log_action(
				user_id         = request.user.pk,
				content_type_id = ContentType.objects.get_for_model(place).pk,
				object_id       = place.pk,
				object_repr     = str(place),
				action_flag     = CHANGE,
				change_message="Changed Category" + str(category.pk)
			)
			messages.success(request,"Place Have Been Saved Successfully",context)
		else:
			raise PermissionDenied

	return render(request,'edit_place.html',context)

@login_required(login_url='/admin/login/')
def add_category(request):
	if request.method == 'POST':
		print "called"
		name = request.POST.get('name','')
		image_url = request.POST.get('image','')
		is_active = request.POST.get('is_active','')
		is_active_value = False
		if is_active == 'true':
			is_active_value = True
		print name

		path='app/static/categoryImage/'
		to_replace = 'app/'
		if 'http' in image_url:
			image = image_url
			if '.png' in image:
				newpath=path
				urllib.urlretrieve(image, newpath+ name +'.png')
				image = newpath.replace(to_replace,'/')+name+'.png'
			else:
				newpath=path
				urllib.urlretrieve(image, newpath+name+'.jpg')
				image = newpath.replace(to_replace,'/')+name+'.jpg'

			category = Category(name=name,is_active=is_active_value,image=image)
			category.save()
			return HttpResponseRedirect('/admin/all_category/')
	return render(request,'add_category.html')


@login_required(login_url='/admin/login/')
def add_place(request):
	locations = Location.objects.all()
	categories = Category.objects.all()
	context = {
		'locations' : locations,
		'categories': categories,
	}

	if request.method == 'POST':
		print "called"
		name = request.POST.get('name','')
		print name
		image_url = request.POST.get('image','')
		description = request.POST.get('description','')
		is_active = request.POST.get('is_active','')
		time = request.POST.get('time','')
		budget = request.POST.get('budget','')
		location_id = request.POST.get('location','')
		category_id = request.POST.get('category','')
		print category_id

		location = Location.objects.get(pk=location_id)
		category = Category.objects.get(pk=category_id)

		is_active_value = False
		if is_active == 'true':
			is_active_value = True
		print is_active_value
		path='app/static/placeImage/'
		to_replace = 'app/'
		if 'http' in image_url:
			print "http"
			image = image_url
			if '.png' in image:
				newpath=path
				urllib.urlretrieve(image, newpath+ name +'.png')
				image = newpath.replace(to_replace,'/')+name+'.png'
			else:
				newpath=path
				urllib.urlretrieve(image, newpath+name+'.jpg')
				image = newpath.replace(to_replace,'/')+name+'.jpg'

			place = Place(name=name,is_active=is_active_value,image=image,duration=time,budget=budget,short_description=
						  description,location=location,category=category)
			print "saving place"
			print place.name
			place.save()
			if os.path.exists(os.path.join('app/static/galleryImage/', str(place.id))):
				shutil.rmtree(os.path.join('app/static/galleryImage/', str(place.id)))
			else:
				os.mkdir(os.path.join('app/static/galleryImage/', str(place.id)))
			return HttpResponseRedirect('/admin/all_places/')

	return render(request,'add_place.html',context)

@login_required(login_url='/admin/login/')
def change_category_image(request):
	id = request.GET.get('category_id','')
	image_url = request.GET.get('category_image','')
	category = Category.objects.get(pk=id)


	path='app/static/categoryImage/'
	to_replace = 'app/'
	if 'http' in image_url:
		print "inside http"
		image = image_url
		if '.png' in image:
			print "inside png"
			newpath=path
			print image
			urllib.urlretrieve(image, newpath+category.name+'.png')
			image = newpath.replace(to_replace,'/')+category.name+'.png'
			category.image = str(image+'?t='+dt.datetime.now().strftime("%Y%m%d%H%M%S%f"))
			category.save()
			print category.image
		else:
			print "inside not png"
			newpath=path
			print image
			urllib.urlretrieve(image, newpath+category.name+'.jpg')
			image = newpath.replace(to_replace,'/')+category.name+'.jpg'
			category.image = str(image+'?t='+dt.datetime.now().strftime("%Y%m%d%H%M%S%f"))
			category.save()
			print category.image
	else:
		category.image=image_url
		category.save()

	category = Category.objects.get(pk=id)
	context={
		'image' : category.image,
	}
	return  render(request,'category_image_div.html',context)

@login_required(login_url='/admin/login/')
def change_place_image(request):
	id = request.GET.get('place_id','')
	image_url = request.GET.get('place_image','')
	place = Place.objects.get(pk=id)

	path='app/static/placeImage/'
	to_replace = 'app/'
	if 'http' in image_url:
		image = image_url
		if '.png' in image:
			newpath=path
			urllib.urlretrieve(image, newpath+place.name+'.png')
			image = newpath.replace(to_replace,'/')+place.name+'.png'
			# place.image = str(image)
			place.image = str(image+'?t='+dt.datetime.now().strftime("%Y%m%d%H%M%S%f"))
			place.save()
		else:
			newpath=path
			urllib.urlretrieve(image, newpath+place.name+'.jpg')
			image = newpath.replace(to_replace,'/')+place.name+'.jpg'
			# place.image = str(image)
			place.image = str(image+'?t='+dt.datetime.now().strftime("%Y%m%d%H%M%S%f"))
			place.save()
	else:
		place.image=image_url
		place.save()

	context={
		'place' : place,
	}
	return  render(request,'place_image_div.html',context)

@login_required(login_url='/admin/login/')
def add_image_to_place_gallery(request):

	id = request.GET.get('place_id','')
	image_url = request.GET.get('place_image','')
	short_description = request.GET.get('short_description','')
	place = Place.objects.get(pk=id)
	# gallery_count = place.gallery.all()
	# gallery_count = gallery_count.count() + 1

	path='app/static/galleryImage/'
	to_replace = 'app/'
	if 'http' in image_url:
		image = image_url
		if '.png' in image:
			newpath=path + str(place.id) + '/'
			value = str(dt.datetime.now().strftime("%Y%m%d%H%M%S%f"))
			urllib.urlretrieve(image, newpath + place.name + value + '.png')
			image = newpath.replace(to_replace,'/')+place.name + value + '.png'
			gallery = Gallery(image_link = image,short_description=short_description)
			gallery.save()
			place.gallery.add(gallery)
		else:
			newpath=path + str(place.id) + '/'
			value = str(dt.datetime.now().strftime("%Y%m%d%H%M%S%f"))
			urllib.urlretrieve(image, newpath + place.name + value + '.jpg')
			image = newpath.replace(to_replace,'/')+place.name + value + '.jpg'
			gallery = Gallery(image_link = image,short_description=short_description)
			gallery.save()
			place.gallery.add(gallery)
	else:
		place.image=image_url
		place.save()
	place = Place.objects.get(pk=id)
	context = {
		'place' : place,
	}
	return render(request,'place_gallery_div.html',context)

@login_required(login_url='/admin/login/')
def delete_image_from_gallery(request):
	place_id = request.GET.get('place_id','')
	gallery_id = request.GET.get('gallery_id','')
	gallery = Gallery.objects.get(pk=gallery_id)
	gallery.delete()
	place = Place.objects.get(pk=place_id)
	context = {
		'place' : place,
	}

	return render(request,'place_gallery_div.html',context)

@login_required(login_url='/admin/login/')
def edit_image_from_gallery(request):
	gallery_id = request.GET.get('gallery_id','')
	place_id = request.GET.get('place_id','')
	image_url = request.GET.get('image_link','')
	short_description = request.GET.get('description','')

	place = Place.objects.get(pk=place_id)
	# gallery_count = place.gallery.all()
	# gallery_count = gallery_count.count() + 1
	gallery = Gallery.objects.get(pk=gallery_id)
	gallery.short_description = short_description
	print gallery.short_description


	path='app/static/galleryImage/'
	to_replace = 'app/'
	if 'http' in image_url:
		image = image_url
		if '.png' in image:
			newpath=path + str(place.id) + '/'
			value = str(dt.datetime.now().strftime("%Y%m%d%H%M%S%f"))
			urllib.urlretrieve(image, newpath + place.name + value + '.png')
			image = newpath.replace(to_replace,'/')+place.name + value + '.png'
			gallery.image_link = image
			gallery.save()
		else:
			newpath=path + str(place.id) + '/'
			value = str(dt.datetime.now().strftime("%Y%m%d%H%M%S%f"))
			urllib.urlretrieve(image, newpath + place.name + value + '.jpg')
			image = newpath.replace(to_replace,'/')+place.name+ value + '.jpg'
			print image
			gallery.image_link = image
	gallery.save()

	place = Place.objects.get(pk=place_id)
	context={
		'place' : place,
	}
	return render(request,'place_gallery_div.html',context)

@login_required(login_url='/admin/login/')
def add_desc_to_place(request):

	place_id = request.GET.get('place_id','')
	heading = request.GET.get('title','')
	description = request.GET.get('description','')


	place = Place.objects.get(pk=place_id)
	if place:
		desc = Description(place=place,heading=heading,text=description)
		desc.save()

	description = Description.objects.filter(place=place)
	context = {
		'description' : description,
	}
	return render(request,'place_desc_div.html',context)

@login_required(login_url='/admin/login/')
def edit_description(request):
	place_id = request.GET.get('place_id','')
	desc_id = request.GET.get('desc_id','')
	title = request.GET.get('title','')
	text = request.GET.get('description','')

	description = Description.objects.get(pk=desc_id)
	description.heading = title
	description.text = text
	description.save()

	description = Description.objects.filter(place__id=place_id)
	context = {
		'description' : description,
	}
	return render(request,'place_desc_div.html',context)

@login_required(login_url='/admin/login/')
def delete_description(request):
	desc_id = request.GET.get('desc_id','')
	place_id = request.GET.get('place_id','')
	description = Description.objects.get(pk=desc_id)
	if description:
		description.delete()

	description = Description.objects.filter(place__id=place_id)
	context = {
		'description' : description,
	}
	return render(request,'place_desc_div.html',context)

@login_required(login_url='/admin/login/')
def all_locations(request):
	locations = Location.objects.all()
	context = {
		'locations' : locations,
	}
	return render(request,'all_locations.html',context)

@login_required(login_url='/admin/login/')
def add_location(request):

	return render(request,'add_location.html')

@login_required(login_url='/admin/login/')
def add_new_location(request):

	if request.method == "POST":
		city = request.POST.get('city','')
		state = request.POST.get('state','')
		area = request.POST.get('area','')
		l_cord = request.POST.get('l_coord','')
		location = Location(city=city,state=state,area=area,mpoly=l_cord)
		location.save()

	return render(request,'add_location.html')


def edit_location(request,id):

	if request.method == "POST":
		city = request.POST.get('city','')
		state = request.POST.get('state','')
		area = request.POST.get('area','')
		l_cord = request.POST.get('l_coord','')
		location = Location.objects.get(pk=id)
		location.city = city
		location.area = area
		location.state = state
		location.mpoly = l_cord
		location.save()

	location = Location.objects.get(pk=id)
	polygon_coordi = simplejson.loads(location.mpoly.json)['coordinates'][0]
	context = {
		'location' : location,
		'polygon_cord' : polygon_coordi,
	}

	return render(request,'edit_location.html',context)

def all_logs(request):
	logs = LogEntry.objects.all()

	context = {
		'logs' : logs,
	}
	return render(request,'all_logs.html',context)

def all_visitors(request):
	visitors = Visitor.objects.all()
	context = {
		'visitors' : visitors,
	}
	return render(request,'all_visitors.html',context)

def send_notification(request):

	return render(request,'send_notification.html')

def send_notification_with_result(request):
	title = request.GET.get('title','')
	message = request.GET.get('message','')
	print title
	print message

	data = {'title' : title,'message': message}
	reg_ids = map(lambda x: x.app_id, Visitor.objects.all())

	n = 1
	for i in range(0, len(reg_ids), n):
		print "1"
		API_KEY = constant.API_KEY
		gcm = GCM(API_KEY)
		response = gcm.json_request(registration_ids=reg_ids[i:i + n], data=data)

		time.sleep(1)

	return render(request,'blank_page.html')

def all_booking(request):
	context = {

	}
	return render(request,'all_booking.html',context)