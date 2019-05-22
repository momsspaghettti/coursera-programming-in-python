from django.http import HttpResponse


def simple_route(request):
    if request.method == 'GET':
        return HttpResponse("", status=200)
    else:
        return HttpResponse(status=405)


def slug_route(request):
    return HttpResponse(str(request.path).split('/')[-2])


def sum_route(request):
    slug = str(request.path).split('/')
    a = int(slug[-2])
    b = int(slug[-3])

    return HttpResponse(a+b)


def sum_get_method(request):
    if request.method == 'GET':
        try:
            a = int(request.GET.get('a'))
            b = int(request.GET.get('b'))
            return HttpResponse(a + b)
        except:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=400)


def sum_post_method(request):
    if request.method == 'POST':
        try:
            a = int(request.GET.get('a'))
            b = int(request.GET.get('b'))
            return HttpResponse(a + b)
        except:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=400)