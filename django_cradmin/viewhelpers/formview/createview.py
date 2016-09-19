import urllib.parse

from django.utils.translation import ugettext_lazy
from django.views.generic import CreateView as DjangoCreateView

from . import create_update_view_mixin


class CreateView(create_update_view_mixin.CreateUpdateViewMixin,
                 DjangoCreateView):
    template_name = 'django_cradmin/viewhelpers/create.django.html'

    #: The viewname within this app for the edit view.
    #: See :meth:`.get_editurl`.
    editview_appurl_name = 'edit'

    def get_pagetitle(self):
        """
        Get the page title (the title tag).

        Defaults to ``Create <verbose_name model>``.
        """
        return ugettext_lazy('Create %(what)s') % {'what': self.model_verbose_name}

    def get_success_message(self, obj):
        """
        Defaults to ``"Created "<str(obj)>".``
        """
        return ugettext_lazy('Created "%(object)s"') % {'object': obj}

    def get_editurl(self, obj):
        """
        Get the edit URL for ``obj``.

        Defaults to::

            self.request.cradmin_app.reverse_appurl(self.editview_appurl_name, args=[obj.pk])

        You normally want to use :meth:`.get_full_editurl` instead of this method.
        """
        return self.request.cradmin_app.reverse_appurl(self.editview_appurl_name, args=[obj.pk])

    def get_full_editurl(self, obj):
        """
        Get the full edit URL for the provided object.

        Unlike :meth:`.get_editurl`, this ensures that any ``success_url`` in ``request.GET``
        is included in the URL.

        Args:
            obj: A saved model object.
        """
        url = self.get_editurl(obj)
        if 'success_url' in self.request.GET:
            url = '{}?{}'.format(
                url, urllib.parse.urlencode({
                    'success_url': self.request.GET['success_url']}))
        return url