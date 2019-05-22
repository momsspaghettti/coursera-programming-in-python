from django.conf.urls import url
from views import *


urlpatterns = [
    url(r'^/routing/simple_route/$', simple_route),
    url(r'^/routing/slug_route/^[a-z0-9-_]{1,16}$/$', slug_route),
    url(r'^/routing/sum_route/-{0,1}\d/-{0,1}\d/$', sum_route),
    url(r'^/routing/sum_get_method/\?a=-{0,1}\d&b=-{0,1}\d$', sum_get_method),
    url(r'^/routing/sum_post_method/$', sum_post_method)
]