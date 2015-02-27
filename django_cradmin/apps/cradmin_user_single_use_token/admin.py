from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django_cradmin.apps.cradmin_user_single_use_token.models import UserSingleUseToken


class UserSingleUseTokenAdmin(admin.ModelAdmin):
    list_display = (
        'token',
        'user',
        'app',
        'created_datetime',
        'expiration_datetime',
        'expiration_naturaltime',
    )
    search_fields = (
        'app',
        'user__email',
        'token',
    )
    list_filter = (
        'app',
        'created_datetime',
        'expiration_datetime',
    )
    readonly_fields = (
        'token',
        'user',
        'app',
        'created_datetime',
    )
    ordering = ['-created_datetime']

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(UserSingleUseTokenAdmin, self).get_queryset(request)
        else:
            return UserSingleUseToken.objects.none()

    def expiration_naturaltime(self, obj):
        return naturaltime(obj.expiration_datetime)
    expiration_naturaltime.short_description = 'Expires'
    expiration_naturaltime.admin_order_field = 'expiration_datetime'

admin.site.register(UserSingleUseToken, UserSingleUseTokenAdmin)
