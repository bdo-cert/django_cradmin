from __future__ import unicode_literals
import json
from xml.sax.saxutils import quoteattr
from django import forms
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.translation import gettext


class BulkFileUploadWidget(forms.Widget):
    template_name = 'django_cradmin/apps/cradmin_temporaryfileuploadstore/bulkfileupload-widget.django.html'

    def __init__(self,
                 accept=None,
                 apiparameters=None,
                 dropbox_text=None,
                 invalid_filetype_message=None,
                 advanced_fileselectbutton_text=None,
                 simple_fileselectbutton_text=None,
                 autosubmit=False):
        """
        Parameters:
            accept (str): Comma separated string of filetypes that we should accept.
                Added to the file upload field as the accept attribute.
                Note that this is not validated serverside - use the accept attribute
                of ``apiparameters`` to do that.
            apiparameters (dict): Dict of API parameters. Here you can
                put values for the ``minutes_to_live``, ``accept``, ``max_filename_length``
                and ``unique_filenames`` attributes of
                :class:`django_cradmin.apps.cradmin_temporaryfileuploadstore.models.TemporaryFileCollection`.

                Example::

                    apiparameters = {
                        'minutes_to_live': 10,
                        'accept': 'application/pdf,text/plain,image/*',
                        'unique_filenames': True
                    }
            autosubmit: If this is ``True``, the form is submitted
                when the upload is finished. This also makes it impossible
                to upload more than one batch of files, because the widget
                hides all the upload widgets as soon as any files is added.
                It works with multi-file upload, but the user will only
                be able to upload one batch of files, and they will not
                be able to remove or upload more files.
        """
        self.accept = accept
        self.apiparameters = apiparameters or {}
        self.dropbox_text = dropbox_text
        self.invalid_filetype_message = invalid_filetype_message
        self.advanced_fileselectbutton_text = advanced_fileselectbutton_text
        self.simple_fileselectbutton_text = simple_fileselectbutton_text
        self.autosubmit = autosubmit
        super(BulkFileUploadWidget, self).__init__(attrs=None)

    def get_uploadapiurl(self):
        """
        Get the file upload API URL.

        You can override this if you provide your own upload API.
        """
        return reverse('cradmin_temporary_file_upload_api')

    def get_errormessage503(self):
        """
        Get the error message to show on 503 server errors.
        """
        return gettext('Server timeout while uploading the file. This may be caused '
                       'by a poor upload link and/or a too large file.')

    def get_use_singlemode(self):
        """
        If this returns ``True``, only single file upload is allowed.
        Defaults to ``False``, but :class:`.SingleFileUploadWidget`
        overrides this.
        """
        return False

    def get_apiparameters(self):
        """
        Get parameters for the upload API.
        """
        apiparameters = self.apiparameters.copy()
        apiparameters['singlemode'] = self.get_use_singlemode()
        return apiparameters

    def get_angularjs_directive_options(self):
        """
        Get options for the ``django-cradmin-bulkfileupload``
        angularjs directive.

        Must return a JSON encodable dict.
        """
        return {
            'uploadapiurl': self.get_uploadapiurl(),
            'apiparameters': self.get_apiparameters(),
            'errormessage503': self.get_errormessage503(),
            'autosubmit': str(self.autosubmit).lower()
        }

    def get_template_context_data(self, **context):
        """
        Can be overridden to adjust the template context data.
        """
        context['accept'] = self.accept
        context['dropbox_text'] = self.dropbox_text
        context['invalid_filetype_message'] = self.invalid_filetype_message
        context['advanced_fileselectbutton_text'] = self.advanced_fileselectbutton_text
        context['simple_fileselectbutton_text'] = self.simple_fileselectbutton_text
        context['angularjs_directive_options'] = quoteattr(json.dumps(
            self.get_angularjs_directive_options()))
        context['singlemode'] = self.get_use_singlemode()
        return context

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        return render_to_string(self.template_name, self.get_template_context_data(
            hiddenfieldname=name,
            fieldvalue=value))


class SingleFileUploadWidget(BulkFileUploadWidget):
    def __init__(self, *args, **kwargs):
        super(SingleFileUploadWidget, self).__init__(*args, **kwargs)

    def get_use_singlemode(self):
        return True

    def get_template_context_data(self, **context):
        context = super(SingleFileUploadWidget, self).get_template_context_data(**context)
        return context
