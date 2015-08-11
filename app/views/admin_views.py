from app.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import urllib
import datetime as dt
from django.contrib import messages

# def admin_login(request):
# 	next_page = request.GET.get('next', '')
# 	print next_page
# 	# logger.debug('user_login request')
# 	context = {
# 		'next': next_page
# 	}
# 	if request.user:
# 		if request.user.is_active and request.user.is_staff:
# 			next_page = request.GET.get('next')
# 			if next_page:
# 				return HttpResponseRedirect(next_page)
# 			return HttpResponseRedirect('/backend/test/')
# 	if request.method == 'POST':
# 		username = request.POST['username']
# 		password = request.POST['password']
# 		print username + " " + password
# 		user = authenticate(username=username, password=password)
# 		if user:
# 			if user.is_active and user.is_staff:
# 				login(request, user)
# 				# logger.debug('user_login ' + username)
# 				next_page = request.GET.get('next')
# 				print next_page
# 				if next_page:
# 					return HttpResponseRedirect(next_page)
# 				return HttpResponseRedirect('/backend/test/')
# 			else:
# 				return HttpResponse("Your account is disabled.")
# 		else:
# 			# logger.debug("Invalid login details: {0}, {1}".format(username, password))
# 			# logger.debug('user_login ' + username + 'unable to login')
# 			messages.warning(request, 'Invalid Login Details', context)
# 			return render(request, 'login.html', context)
# 	else:
# 		return render(request, 'login.html', context)

def admin(request):
	return HttpResponseRedirect('/admin/login/')

def admin_login(request):
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

def show_categories(request):
	categories = Category.objects.all()
	context = {
		'categories' : categories,
	}
	return render(request,'all_category.html',context)


def edit_category(request,id):
	category = Category.objects.get(pk=id)
	context={
		'category' : category,
	}
	if request.method == "POST":
		name = request.POST.get('name','')
		is_active = request.POST.get('is_active','')
		category.name = name
		is_active_value = False
		if is_active == 'on':
			is_active_value = True
		category.is_active = is_active_value
		category.save()
		messages.success(request, ' Category Saved')
	return render(request,'edit_category.html',context)

def all_places(request):
	places = Place.objects.all()
	context={
		'places':places,
	}
	return render(request,'all_places.html',context)

def edit_place(request,id):
	place = Place.objects.get(pk=id)
	context={
		'place' : place,
	}
	if request.method == "POST":
		name = request.POST.get('name','')
		is_active = request.POST.get('is_active','')
		short_description = request.POST.get('short_description','')
		duration = request.POST.get('duration','')
		budget = request.POST.get('budget','')

		is_active_value = False
		if is_active == 'on':
			is_active_value = True
		place.is_active = is_active_value
		place.name = name
		place.short_description = short_description
		place.duration = duration
		place.budget = budget
		place.save()

	return render(request,'edit_place.html',context)

def add_category(request):

	context={

	}
	return render(request,'add_category.html',context)

def change_category_image(request):
	id = request.GET.get('category_id','')
	image_url = request.GET.get('category_image','')
	category = Category.objects.get(pk=id)
	print category.name

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
			# category.image = str(image)
			category.image = str(image+'?t='+dt.datetime.now().strftime("%Y%m%d%H%M%S%f"))
			category.save()
			print category.image
		else:
			print "inside not png"
			newpath=path
			print image
			urllib.urlretrieve(image, newpath+category.name+'.jpg')
			image = newpath.replace(to_replace,'/')+category.name+'.jpg'
			# category.image = str(image)
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
		'image' : place.image,
	}
	return  render(request,'place_image_div.html',context)

def add_image_to_place_gallery(request):

	id = request.GET.get('place_id','')
	image_url = request.GET.get('place_image','')
	short_description = request.GET.get('short_description','')
	place = Place.objects.get(pk=id)
	gallery_count = place.gallery.all()
	gallery_count = gallery_count.count() + 1

	path='app/static/galleryImage/'
	to_replace = 'app/'
	if 'http' in image_url:
		image = image_url
		if '.png' in image:
			newpath=path + str(place.id) + '/'
			urllib.urlretrieve(image, newpath + place.name + str(gallery_count) + '.png')
			image = newpath.replace(to_replace,'/')+place.name + + str(gallery_count) + '.png'
			gallery = Gallery(image_link = image,short_description=short_description)
			gallery.save()
			place.gallery.add(gallery)
		else:
			newpath=path + str(place.id) + '/'
			urllib.urlretrieve(image, newpath + place.name + str(gallery_count) + '.jpg')
			image = newpath.replace(to_replace,'/')+place.name+ str(gallery_count) + '.jpg'
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