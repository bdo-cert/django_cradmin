from crispy_forms import layout
from crispy_forms.helper import FormHelper
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.views.generic import FormView

from django_cradmin.apps.cradmin_user_single_use_token.models import UserSingleUseToken
from django_cradmin.crispylayouts import PrimarySubmit


class RepeatPasswordForm(forms.Form):
    password1 = forms.CharField(
        label=_('Type your new password'),
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_('Type your new password one more time'),
        widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(RepeatPasswordForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_('The passwords do not match'))


class ResetPasswordView(FormView):
    template_name = 'cradmin_passwordreset/reset.django.html'
    form_class = RepeatPasswordForm

    def get_formhelper(self):
        helper = FormHelper()
        helper.form_action = '#'
        helper.form_id = 'django_cradmin_resetpassword_reset_form'
        helper.layout = layout.Layout(
            'password1',
            'password2',
            PrimarySubmit('submit', _('Submit'))
        )
        return helper

    def get_context_data(self, **kwargs):
        context = super(ResetPasswordView, self).get_context_data(**kwargs)
        context['formhelper'] = self.get_formhelper()
        try:
            context['single_use_token'] = UserSingleUseToken.objects.get(
                token=self.kwargs['token'], app='cradmin_passwordreset')
        except UserSingleUseToken.DoesNotExist:
            pass
        return context

    def get_success_url(self):
        return getattr(settings, 'DJANGO_CRADMIN_RESETPASSWORD_FINISHED_REDIRECT_URL', settings.LOGIN_URL)

    def form_valid(self, form):
        try:
            user = UserSingleUseToken.objects.pop(
                token=self.kwargs['token'], app='cradmin_passwordreset')
        except UserSingleUseToken.DoesNotExist:
            return self.render_to_response(self.get_context_data())
        else:
            raw_password = form.cleaned_data['password1']
            user.set_password(raw_password)
            user.save()
            return super(ResetPasswordView, self).form_valid(form)
