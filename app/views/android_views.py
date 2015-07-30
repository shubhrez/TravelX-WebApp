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