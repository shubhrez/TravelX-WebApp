from app.models import *
from django.http import HttpResponse
import simplejson


def get_categories(request):
    print "called"
    data = []
    categories = Category.objects.filter(is_active=True)
    for c in categories:
        data.append({'id':c.id,'name':c.name})

    data = simplejson.dumps({'object':data})
    return HttpResponse(data, content_type='application/json')