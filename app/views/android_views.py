from app.models import *
from django.http import HttpResponse
import simplejson


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