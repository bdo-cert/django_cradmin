# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from collections import OrderedDict

import markdown
import pykss
from django.conf import settings
from django.templatetags.static import static
from ievv_opensource.utils.singleton import Singleton
from ievv_opensource.utils import ievvbuildstatic

from django_cradmin.apps.cradmin_kss_styleguide import markdownformatter


class AbstractStyleGuide(object):
    #: The extensions to look for when finding style files.
    stylefile_extensions = ['.less', '.css', '.sass', '.scss']

    def __init__(self, unique_id, label,
                 template_name="cradmin_kss_styleguide/styleguideview/guide.django.html",
                 section_template_name='cradmin_kss_styleguide/templatetags/render_kss_section.django.html',
                 sections_template_name='cradmin_kss_styleguide/templatetags/render_kss_sections.django.html',
                 toc_template_name='cradmin_kss_styleguide/templatetags/render_kss_toc.django.html',
                 frontpage_template=None):
        """
        Args:
            unique_id: A unique ID for the styleguide.
            label: The label of the styleguide.
        """
        self.unique_id = unique_id
        self.label = label
        self.template_name = template_name
        self.section_template_name = section_template_name
        self.sections_template_name = sections_template_name
        self.toc_template_name = toc_template_name
        self.frontpage_template = frontpage_template

    def get_sourcefolders(self):
        raise NotImplementedError()

    def get_cssurl_for_styleguide(self):
        raise NotImplementedError()

    def make_kss_styleguide(self):
        return pykss.Parser(*self.get_sourcefolders(), extensions=self.stylefile_extensions)

    def get_template_name(self):
        return self.template_name

    def get_section_template_name(self):
        return self.section_template_name

    def get_sections_template_name(self):
        return self.sections_template_name

    def get_toc_template_name(self):
        return self.toc_template_name

    def format_description_text(self, text):
        return markdownformatter.MarkdownFormatter.to_html(markdowntext=text)

    def __str__(self):
        return self.label


class StyleGuide(AbstractStyleGuide):
    def __init__(self, sourcefolders, cssurl_for_styleguide, **kwargs):
        """
        Args:
            sourcefolders (list): List of source folders.
            **kwargs: See :class:`.AbstractStyleGuide`.
        """
        super(StyleGuide, self).__init__(**kwargs)
        self.sourcefolders = sourcefolders
        self.cssurl_for_styleguide = cssurl_for_styleguide

    def get_sourcefolders(self):
        return self.sourcefolders

    def get_cssurl_for_styleguide(self):
        return self.cssurl_for_styleguide


class IevvBuildstaticStyleGuide(AbstractStyleGuide):
    def __init__(self, appname, sourcefile, sourcefolder='styles', **kwargs):
        super(IevvBuildstaticStyleGuide, self).__init__(**kwargs)
        self.appname = appname
        self.sourcefolder = sourcefolder
        self.sourcefile = sourcefile

    def find_plugin(self):
        app = settings.IEVVTASKS_BUILDSTATIC_APPS.get_app(self.appname)
        for plugin in app.plugins:
            if isinstance(plugin, ievvbuildstatic.sassbuild.Plugin):
                if plugin.sourcefolder == self.sourcefolder and plugin.sourcefile == self.sourcefile:
                    return plugin
        raise ValueError(
            'Plugin in {appname} matching sourcefolder={sourcefolder} and '
            'sourcefile={sourcefile} not found'.format(
                appname=self.appname,
                sourcefolder=self.sourcefolder,
                sourcefile=self.sourcefile))

    def get_sourcefolders(self):
        plugin = self.find_plugin()
        sourcefolders = [plugin.get_sourcefolder_path()]
        sourcefolders.extend(plugin.get_other_sourcefolders_paths())
        return sourcefolders

    def get_cssurl_for_styleguide(self):
        plugin = self.find_plugin()
        staticurl = plugin.get_destinationfile_path().split('{sep}static{sep}'.format(sep=os.sep))[1]
        return static(staticurl)


class Registry(Singleton):
    """
    Registry of :class:`.StyleGuide` objects.

    Examples:

        First, define a subclass of :class:`.AbstractCustomSql`.

        Register a StyleGuide in the registry via an AppConfig for your
        Django app::

            from django.apps import AppConfig
            from django_cradmin.apps.cradmin_kss_styleguide import styleguide_registry

            class MyAppConfig(AppConfig):
                name = 'myapp'

                def ready(self):
                    styleguide = styleguide_registry.StyleGuide(
                        unique_id='my_styles',
                        label='My styles',
                        source_folder='/path/to/my/styles/')
                    styleguide_registry.Registry.get_instance().add(styleguide)
    """

    def __init__(self):
        super(Registry, self).__init__()
        self._styleguides = OrderedDict()

    def add(self, styleguide):
        """
        Add the given ``customsql_class`` to the registry.

        Parameters:
            styleguide (.AbstractStyleGuide): The styleguide.
        """
        if styleguide.unique_id in self._styleguides:
            raise KeyError('Duplicate unique_id in styleguide: {}'.format(styleguide.unique_id))
        self._styleguides[styleguide.unique_id] = styleguide

    def __getitem__(self, unique_id):
        """
        Get the :class:`.AbstractStyleGuide` registered with ``unique_id``.
        """
        return self._styleguides[unique_id]

    def iterstyleguides(self):
        return self._styleguides.values()


class MockableRegistry(Registry):
    """
    A non-singleton version of :class:`.Registry`. For tests.

    Typical usage in a test::

        from django_cradmin.apps.cradmin_kss_styleguide import styleguide_registry

        class MockStyleGuide(styleguide_registry.StyleGuide):
            # ...

        mockregistry = styleguide_registry.MockableRegistry()
        mockregistry.add(MockStyleGuide(...))

        with mock.patch('django_cradmin.apps.cradmin_kss_styleguide.styleguide_registry.Registry.get_instance',
                        lambda: mockregistry):
            pass  # ... your code here ...
    """

    def __init__(self):
        self._instance = None  # Ensure the singleton-check is not triggered
        super(MockableRegistry, self).__init__()