from django.http import HttpResponse


def simple_route(request):
    method = str(request.request).split(' ')[1][1:4]

    if method == 'GET':
        return HttpResponse("", status=200)
    else:
        return HttpResponse("", status=405)


def slug_route(slug):
    return HttpResponse(str(slug.url).split('/')[-2])


def sum_route(request):
    slug = str(request.url).split('/')
    a = int(slug[-2])
    b = int(slug[-3])

    return HttpResponse(a+b)


def sum_get_method(request):
    slug = str(request.url).split('/')
    ab = slug[-1].split('&')
    a = int(ab[0][-1])
    b = int(ab[1][-1])

    return HttpResponse(a+b)


def sum_post_method(request):
    a = int(request.GET.get('a'))
    b = int(request.GET.get('b'))

    return HttpResponse(a+b)