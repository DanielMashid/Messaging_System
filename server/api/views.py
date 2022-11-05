import json
from django.http import JsonResponse

def api_home(request, *args, **kwargs):
    # request -> HttpRequest -> Django
    # print(dir(request))
    # request.body
    body = request.body # byte string of JSON data
    data = {}
    try:
        data = json.loads(body) # string of JSON data -> Python Dict
    except:
        pass    
    print(data)
    # data['headers'] = request.headers # request.META ->
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type
    return JsonResponse({"message": "Hi there, this is your Django API response!!"})
