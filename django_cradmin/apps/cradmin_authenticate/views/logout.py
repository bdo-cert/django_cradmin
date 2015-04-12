from __future__ import unicode_literals
from django.contrib.auth.views import logout


def cradmin_logoutview(request, template_name='cradmin_authenticate/logout.django.html'):
    next_page = None
    if 'next' in request.GET:
        next_page = request.GET['next']
    return logout(
        request,
        template_name=template_name,
        next_page=next_page)
