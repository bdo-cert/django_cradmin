from __future__ import unicode_literals
import json
from xml.sax.saxutils import quoteattr

from django.utils.translation import ugettext

from django_cradmin.renderable import AbstractRenderableWithCss
from django_cradmin.templatetags.cradmin_icon_tags import cradmin_icon
from django_cradmin.viewhelpers.listfilter.base.abstractfilter import AbstractFilter
from django_cradmin.viewhelpers.listfilter.base.filtershandler import FiltersHandler


class AbstractFilterList(AbstractRenderableWithCss):
    """
    Defines a set of :class:`.AbstractFilter` objects.

    .. note:: This is not really an abstract class - it works on it own,
       but it should never be used directly. We provide subclasses that
       provide basis for rendereing, and if you want something totally different,
       you should not use this directly, but create a subclass and override
       :meth:`~django_cradmin.renderable.AbstractRenderableWithCss.get_base_css_classes_list`
       or :meth:`~django_cradmin.renderable.AbstractRenderableWithCss.get_extra_css_classes_list`
       (see their docs for their intended use cases).
    """
    template_name = 'django_cradmin/viewhelpers/listfilter/base/filterlist.django.html'

    def __init__(self, urlbuilder, target_css_selector='.django-cradmin-listfilter-target'):
        """
        Parameters:
            urlbuilder: See :class:`.FiltersHandler`.
            target_css_selector: The css selector of the element to replace when
                filters change value.
        """
        super(AbstractFilterList, self).__init__()
        self.children = []
        self.set_filters_string_called = False
        self.filtershandler = self.get_filters_handler_class()(urlbuilder=urlbuilder)
        self.target_css_selector = target_css_selector

    def get_target_css_selector(self):
        return self.target_css_selector

    def get_loadspinner_css_class(self):
        """
        Get the css class to use for the load spinner.

        You can return ``None`` to not show a load spinner at all.
        """
        return cradmin_icon('loadspinner')

    def get_loaderror_message(self):
        """
        Get the error message to show when the angularJS directive
        fails to load the filtered page.

        Must return a string (can not use ugettext_lazy, use ugettext instead).
        """
        return ugettext('An error occurred. Please try to reload the page.')

    def get_loadingmessage_delay_milliseconds(self):
        """
        Get the number of milliseconds to wait until we show the loading message.

        Defaults to ``1000``. This means that we wait for a second
        before showing the loading message, so for fast requests, it is
        not shown at all.
        """
        return 1000

    def get_angularjs_options_dict(self):
        return {
            'loadspinner_css_class': self.get_loadspinner_css_class(),
            'target_css_selector': self.get_target_css_selector(),
            'loaderror_message': self.get_loaderror_message(),
            'loadingmessage_delay_milliseconds': self.get_loadingmessage_delay_milliseconds(),
        }

    def get_angularjs_options_json(self):
        return quoteattr(json.dumps(self.get_angularjs_options_dict()))

    def get_filters_handler_class(self):
        return FiltersHandler

    def get_dom_id_prefix(self):
        """
        The prefix for all DOM IDs created by the filter. This is used by filters
        to generate unique DOM IDs.

        You should not need to override this unless you have multiple filterlists
        in a single page.

        Defaults to ``django-cradmin-listfilter-``.
        """
        return 'django_cradmin_listfilter'

    def append(self, child):
        """
        Add subclass of :class:`django_cradmin.renderable.AbstractGroupChild`
        to the filterlist.

        You will normally add subclasses of :class:`.AbstractFilter`
        but if you want to spice up the filter "box" with additional HTML,
        you can create a subclass of :class:`.AbstractGroupChild` and
        add an object of that class.
        """
        child.set_filterlist(self)
        self.children.append(child)
        if isinstance(child, AbstractFilter):
            self.filtershandler.add_filter(child)

    def get_base_css_classes_list(self):
        return ['django-cradmin-listfilter-filterlist']

    def iter_renderables(self):
        """
        Iterate over all the renderables (children) of the filterlist.
        """
        return iter(self.children)

    def set_filters_string(self, filters_string):
        """
        Set the current value of the filters.

        If you use nested groups, you will only call this once on the
        toplevel filterlist.

        Parameters:
            filter_string: The part of the URL that defines the filters.
                It is parsed by :meth:`.parse_filters_string`.

        Raises:
            InvalidFiltersStringError: When the ``filter_string`` can not be parsed.
                You will normally want to catch this, and show an error message,
                or perhaps ignore it and redirect to the view without filters.
        """
        self.filtershandler.parse(filters_string=filters_string)

    def filter(self, queryobject):
        """
        Apply the filters to the given ``queryobject``.

        See :meth:`.FiltersHandler.filter` for more details.
        """
        return self.filtershandler.filter(queryobject=queryobject)
