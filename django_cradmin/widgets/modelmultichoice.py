from __future__ import unicode_literals

import json

from django.utils.datastructures import MultiValueDict, MergeDict
from future import standard_library

standard_library.install_aliases()
import urllib.request
import urllib.parse
import urllib.error
from django.utils.translation import ugettext_lazy as _
from django.forms import widgets
from django.template.loader import render_to_string
from builtins import str
from past.builtins import basestring


class ModelMultiChoiceWidget(widgets.TextInput):
    """
    Model multi choice widget that uses an iframe popup to enable users
    to select values for many-to-many and one-to-many fields.
    """
    #: The template used to render the widget.
    template_name = 'django_cradmin/widgets/modelmultichoice.django.html'

    #: Do not override this (if you set this to hidden, the widget is not rendered correctly).
    input_type = 'text'

    #: Set this to ``True`` to debug the value of the input field.
    #: Setting this to ``True``, makes the ``type`` of the actually
    #: submitted input field to ``text`` instead of ``hidden``.
    #: Probably only useful for debugging.
    input_field_visible = True

    #: The default select-button text. You can override this in a subclass,
    #: or use the ``selectbutton_text``-argument for the constructor to
    #: change the button text.
    default_selectbutton_text = _('Select ...')

    def __init__(self, queryset, selectview_url, preview='',
                 selectbutton_text=None):
        self.queryset = queryset
        self.preview = preview
        self.selectview_url = selectview_url
        self.selectbutton_text = selectbutton_text or self.default_selectbutton_text
        super(ModelMultiChoiceWidget, self).__init__()

    def __make_selectview_url(self, fieldid, current_value):
        return '{}?{}'.format(
            self.selectview_url, urllib.parse.urlencode({
                'foreignkey_select_current_value': current_value,
                'foreignkey_select_fieldid': fieldid,
            }))

    def get_rendered_input_type(self):
        if self.input_field_visible:
            return 'text'
        else:
            return 'hidden'

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        if isinstance(value, basestring):
            # This handles the data we get from this widget,
            # the other stuff below is just if we get data
            # from tests and other sources where it is not JSON encoded.
            return json.loads(value)
        elif isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        else:
            return data.get(name, None)

    def render(self, name, value, attrs=None):
        if value is None or value == '':
            value = ''
        else:
            value = json.dumps(value)
        fieldid = attrs['id']
        return render_to_string(self.template_name, {
            'preview': self.preview,
            'fieldname': name,
            'fieldid': fieldid,
            'fieldvalue': value,
            'selectview_url': self.__make_selectview_url(fieldid, value),
            'selectbutton_text': self.selectbutton_text,
            'input_type': self.input_type,
            'rendered_input_type': self.get_rendered_input_type()
        })
