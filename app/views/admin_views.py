from app.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import urllib

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
	return render(request,'edit_place.html',context)

def add_category(request):

	context={

	}
	return render(request,'add_category.html',context)

def change_category_image(request):
	id = request.GET.get('category_id','')
	image_url = request.GET.get('category_image','')

	category = Category.objects.get(pk=id)
	if category:
		path='app/static/categoryImage/'
		to_replace = 'app/'
		if 'http' in image_url:
			image = image_url
			if '.png' in image:
				newpath=path
				urllib.urlretrieve(image, newpath+category.name+'.png')
				image = newpath.replace(to_replace,'/')+category.name+'.png'
				category.image = str(image).replace('app/','/')
				category.save()
			else:
				newpath=path
				urllib.urlretrieve(image, newpath+category.name+'.jpg')
				image = newpath.replace(to_replace,'/')+category.name+'.jpg'
				category.image = str(image).replace('/home/shubham/webapps/movincart/','').replace('app/','/')
				category.save()
		else:
			category.image=image_url
			category.save()

	context={
		'image' : category.image,
	}
	return  render(request,'category_image_div.html',context)