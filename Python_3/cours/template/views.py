from django.shortcuts import render


# Create your views here.

def echo(request):
    if 'X_PRINT_STATEMENT' in request.META.keys():
        statement_cond = request.META['X_PRINT_STATEMENT']
    else:
        statement_cond = 'empty'

    param = ''
    var = ''
    val = ''

    if request.META['QUERY_STRING']:
        param = str(request.method).lower() + ' '
        var = str(request.META['QUERY_STRING']).split('=')[0] + ': '
        val = str(request.META['QUERY_STRING']).split('=')[1] + ' '

    return render(request, 'echo.html', context={'param': param, 'var': var, 'val': val,
                                                 'statement_cond': statement_cond})


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })