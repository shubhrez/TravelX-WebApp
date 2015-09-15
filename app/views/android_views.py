from app.models import *
from django.http import HttpResponse
import simplejson
from django.views.decorators.csrf import csrf_exempt
from app.utils import send_mail
import datetime as dt

def get_categories(request):
    data = []
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')

    pkt = 'POINT(' + lat + ' ' + lng + ')'
    try:
        location_obj = Location.objects.get(mpoly__contains=pkt)
    except:
        location_obj = None
        data = simplejson.dumps({'objects':data})
        return HttpResponse(data, content_type='application/json')

    categories = Category.objects.filter(is_active=True,location=location_obj)
    for c in categories:
        data.append({'id':c.id,'name':c.name,'image':c.image})

    data = simplejson.dumps({'objects':data})
    return HttpResponse(data, content_type='application/json')

def get_places(request):
    data=[]
    category_id = request.GET.get('category_id')
    category = Category.objects.get(pk=category_id)
    places = Place.objects.filter(is_active=True,category=category)
    for p in places:
        ratings = Rating.objects.filter(place=p)
        rating = 0
        total = 0
        if ratings:
            for r in ratings:
                total += 1
                rating += r.rating
        if rating > 0:
            rating = float(rating/total)
        data.append({'id':p.id,'name':p.name,'rating':rating,'image':p.image,'location':p.location.city + "," + p.location.state,'short_description':p.short_description})

    data = simplejson.dumps({'objects':data})
    return HttpResponse(data, content_type='application/json')


def get_place_details(request):

    data=[]
    place_id = request.GET.get('place_id','')
    place = Place.objects.get(pk=place_id)
    description1 = Description.objects.filter(place=place)
    description = []
    for d in description1:
        desc = {'title' : d.heading,'text':d.text}
        description.append(desc)
    gallery1 = place.gallery.all()
    gallery = []
    for g in gallery1:
        gal = {'image': g.image_link,'short_description' : g.short_description}
        gallery.append(gal)

    data.append({'description' : description , 'gallery' : gallery,'budget' : place.budget,'duration' : place.duration})

    data = simplejson.dumps({'objects' : data})
    return HttpResponse(data,content_type='application/json')

@csrf_exempt
def register_app_id(request):
    data = []
    if request.method == 'POST':
        app_id = request.POST.get('app_id','')
        app_version = request.POST.get('version_code','')
        email = request.POST.get('email','')

    visitor = Visitor.objects.filter(email=email)
    if visitor:
        visitor = visitor[0]
        visitor.app_id = app_id
        visitor.app_version = app_version
        visitor.save()
    else:
        visitor = Visitor(email=email,app_id=app_id,app_version=app_version)
        visitor.save()

    return HttpResponse(data,content_type='application/json')

def get_search_results(request):
    data=[]
    search_regex = request.GET.get('keyword','')
    keyword = search_regex.split(' ')
    regex = "^"
    for key in keyword:
        regex += "(?=.*" + key.strip() + ")"
    regex += ".*$"
    places = Place.objects.filter(name__iregex=regex).distinct()
    object={}
    for place in places:
        object['id']=place.id
        object['name']=place.name
        object['location']=place.location.area
        data.append(object)
    data = simplejson.dumps({'objects' : data})
    return HttpResponse(data,content_type='application/json')

def rate_place(request):
    data=""
    email = request.GET.get("email","")
    place_id = request.GET.get("place_id","")
    rating = request.GET.get("rating","")
    app_id = request.GET.get("app_id","")
    place = Place.objects.get(pk=place_id)
    user = User.objects.filter(username=email)
    if user:
        user = user[0]
    else:
        user = User.objects.create_user(username=email, email=email,password=email)
        user.save()
    user_profile = UserProfile.objects.filter(user=user)
    if not user_profile:
        user_profile = UserProfile(user=user,app_id=app_id)
        user_profile.save()

    existing_rating = Rating.objects.filter(place=place,user=user)
    if existing_rating:
        data="rated"
        data = simplejson.dumps({'objects' : data})
        return HttpResponse(data,content_type="application/json")
    if rating == "":
        data="rate"
        data = simplejson.dumps({'objects' : data})
        return HttpResponse(data,content_type="application/json")
    else:
        rating = int(float(rating))
        rating = Rating(place=place,user=user,rating=rating)
        rating.save()
        data="rate1"
        data = simplejson.dumps({'objects' : data})
        return HttpResponse(data,content_type="application/json")

@csrf_exempt
def confirm_booking(request):
    data = "done"
    if request.method == "POST":
        email = request.POST.get("email","")
        place_id = request.POST.get("place_id","")
        app_id = request.POST.get("app_id","")
        user = User.objects.filter(username=email)
        if user:
            user = user[0]
        else:
            user = User.objects.create_user(username=email, email=email,password=email)
            user.save()
        user_profile = UserProfile.objects.filter(user=user,app_id=app_id)

        if user_profile:
            user_profile = user_profile[0]
        else:
            user_profile = UserProfile(user=user,app_id=app_id)
            user_profile.save()
        place = Place.objects.get(pk=int(place_id))
        delivery_time = dt.datetime.now()

        booking = Booking(user=user_profile,place=place,date_of_booking=delivery_time)
        booking.save()
        # data = simplejson.dumps({'status' : data})
        send_mail.notify_cs()
        return HttpResponse(data,content_type="application/json")