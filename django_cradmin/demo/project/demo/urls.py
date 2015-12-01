from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from django_cradmin.demo.login_not_required_demo.cradmin import LoginNotRequiredCrAdminInstance
from django_cradmin.demo.no_role_demo.cradmin import NoRoleCrAdminInstance
from django_cradmin.demo.project.demo.views.demo_overview import DemoView
from django_cradmin.demo.usermanagerdemo.cradmin import UsermanagerCrAdminInstance
from django_cradmin.demo.webdemo.cradmin import WebdemoCrAdminInstance

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^authenticate/', include('django_cradmin.apps.cradmin_authenticate.urls')),
    url(r'^resetpassword/', include('django_cradmin.apps.cradmin_resetpassword.urls')),
    url(r'^activate_account/', include('django_cradmin.apps.cradmin_activate_account.urls')),
    url(r'^register/', include('django_cradmin.apps.cradmin_register_account.urls')),

    url(r'^djangoadmin/', include(admin.site.urls)),
    url(r'^webdemo/', include(WebdemoCrAdminInstance.urls())),
    url(r'^login_not_required_demo/', include(LoginNotRequiredCrAdminInstance.urls())),
    url(r'^no_role_demo/', include(NoRoleCrAdminInstance.urls())),
    url(r'^webdemo/', include('django_cradmin.demo.webdemo.urls')),
    url(r'^usermanagerdemo/', include(UsermanagerCrAdminInstance.urls())),
    url(r'^cradmin_temporaryfileuploadstore/', include('django_cradmin.apps.cradmin_temporaryfileuploadstore.urls')),
    url(r'^$', DemoView.as_view()),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),
    url(r'^polls/', include('django_cradmin.demo.polls_demo.urls'))
)
