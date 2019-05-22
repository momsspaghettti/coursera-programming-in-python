from django import template


register = template.Library()


@register.filter(name='inc')
def inc(value, arg):
    return int(value) + int(arg)


@register.simple_tag
def division(a, b, **kwargs):
    if 'to_int' in kwargs:
        if kwargs['to_int']:
            return int(a) // int(b)

    return int(a) / int(b)
