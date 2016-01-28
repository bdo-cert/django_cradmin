"""
Custom django-crispy-forms layouts.
"""
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from crispy_forms import layout
from crispy_forms.helper import FormHelper
from crispy_forms.utils import flatatt
from django.template.loader import render_to_string
from django_cradmin.templatetags.cradmin_icon_tags import cradmin_icon


class CradminSubmitButton(layout.Submit):
    template = 'django_cradmin/crispylayouts/submitbutton.django.html'
    extra_button_attributes = {}

    def get_extra_button_attributes(self):
        return self.extra_button_attributes

    def __init__(self, name, value, icon_cssclass=None, **kwargs):
        self.extra_button_attributes = flatatt(self.get_extra_button_attributes())
        self.icon_cssclass = icon_cssclass
        super(CradminSubmitButton, self).__init__(name, value, **kwargs)


class PrimarySubmit(CradminSubmitButton):
    field_classes = "btn btn-primary"


class PrimarySubmitBlock(CradminSubmitButton):
    field_classes = "btn btn-primary btn-block"


class PrimarySubmitLg(CradminSubmitButton):
    field_classes = "btn btn-primary btn-lg"


class DangerSubmit(CradminSubmitButton):
    field_classes = "btn btn-danger"


class DangerSubmitBlock(CradminSubmitButton):
    field_classes = "btn btn-danger btn-block"


class DefaultSubmit(CradminSubmitButton):
    field_classes = "btn btn-default"


class DefaultSubmitBlock(CradminSubmitButton):
    field_classes = "btn btn-default btn-block"


class CollapsedSectionLayout(layout.Div):
    wrapper_template_name = 'django_cradmin/crispylayouts/collapsed-section-layout.django.html'

    def __init__(self, *args, **kwargs):
        self.show_label = kwargs.pop('show_label', _('Show'))
        self.hide_label = kwargs.pop('hide_label', _('Hide'))
        self.show_icon = kwargs.pop('show_icon', cradmin_icon('caret-down'))
        self.hide_icon = kwargs.pop('hide_icon', cradmin_icon('caret-up'))
        super(CollapsedSectionLayout, self).__init__(*args, **kwargs)

    def get_wrapper_context_data(self):
        return {
            'show_label': self.show_label,
            'hide_label': self.hide_label,
            'show_icon': self.show_icon,
            'hide_icon': self.hide_icon,
        }

    def render(self, *args, **kwargs):
        content = super(CollapsedSectionLayout, self).render(*args, **kwargs)
        context = {
            'content': content
        }
        context.update(self.get_wrapper_context_data())
        return render_to_string(self.wrapper_template_name, context)


class CradminFormHelper(FormHelper):
    template = 'django_cradmin/crispylayouts/cradmin_form_helper.django.html'
