from django import forms
from crispy_forms import layout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from django_cradmin.apps.cradmin_invite.invite_url import InviteUrl
from django_cradmin.crispylayouts import PrimarySubmit
from django_cradmin.viewhelpers.formbase import FormView


class CreatePublicInviteUrl(forms.Form):
    message = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label=_('Message'),
        help_text=_('An optional message that people will see when they visit the sharable link.')
    )
    expiration_datetime = forms.DateTimeField(
        required=False,
        label=_('Expiration time'),
        help_text=_('An optional expiration time for the sharable link.')
    )


class SiteAdminInviteUrl(InviteUrl):
    def get_appname(self):
        return 'webdemo_inviteadmins_public'

    def get_confirm_invite_url(self, generictoken):
        return reverse('webdemo-inviteadmins-accept', kwargs={
            'token': generictoken.token
        })


class CreatePublicInvite(FormView):
    form_class = CreatePublicInviteUrl
    template_name = 'webdemo/inviteadmins_public/create_public_invite.django.html'

    def get_field_layout(self):
        return [
            layout.Div(
                layout.Field('message'),
                layout.Field('expiration_datetime'),
                css_class='cradmin-globalfields'
            )
        ]

    def get_buttons(self):
        return [
            PrimarySubmit('submit', _('Get sharable link')),
        ]

    def form_valid(self, form):
        expiration_datetime = form.cleaned_data['expiration_datetime']
        message = form.cleaned_data['message']
        site = self.request.cradmin_role
        inviteurl = SiteAdminInviteUrl(
            request=self.request, private=False, content_object=site,
            expiration_datetime=expiration_datetime,
            metadata={'message': message})
        inviteurl.get_share_url()
        return HttpResponseRedirect(self.get_success_url())
