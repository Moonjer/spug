import json

from django.http import HttpResponse


def get_hook(request):
    print(request.body)
    return HttpResponse(json.dumps(request.POST), content_type='application/json')
