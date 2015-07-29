from app.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages



def admin_login(request):
	next_page = request.GET.get('next', '')
	# logger.debug('user_login request')
	context = {
		'next': next_page
	}
	if request.user:
		if request.user.is_active and request.user.is_staff:
			next_page = request.GET.get('next')
			if next_page:
				return HttpResponseRedirect(next_page)
			return HttpResponseRedirect('/admin/')
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		print username + " " + password
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active and user.is_staff:
				login(request, user)
				# logger.debug('user_login ' + username)
				next_page = request.GET.get('next')
				if next_page:
					return HttpResponseRedirect(next_page)
				return HttpResponseRedirect('/admin/')
			else:
				return HttpResponse("Your Movincart account is disabled.")
		else:
			# logger.debug("Invalid login details: {0}, {1}".format(username, password))
			# logger.debug('user_login ' + username + 'unable to login')
			messages.warning(request, 'Invalid Login Details', context)
			return render(request, 'login.html', context)
	else:
		return render(request, 'login.html', context)