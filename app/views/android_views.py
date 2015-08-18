from app.models import *
from django.http import HttpResponse
import simplejson
from django.views.decorators.csrf import csrf_exempt

def get_categories(request):
    print "called"
    data = []
    categories = Category.objects.filter(is_active=True)
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
        data.append({'id':p.id,'name':p.name,'image':p.image,'location':p.location.city + "," + p.location.state,'short_description':p.short_description})

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
    else:
        visitor = Visitor(email=email,app_id=app_id,app_version=app_version)
        visitor.save()

    return HttpResponse(data,content_type='application/json')
