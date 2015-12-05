from __future__ import unicode_literals

from django.test import TestCase
import htmls
import mock
from model_mommy import mommy
from future import standard_library

from django_cradmin.tests.viewhelpers.cradmin_viewhelpers_testapp.models import FilterTestModel
from django_cradmin.viewhelpers.listfilter.base.abstractfilter import AbstractFilter
from django_cradmin.viewhelpers.listfilter.base.abstractfilterlist import AbstractFilterList
from django_cradmin.viewhelpers.listfilter.base.abstractgroupchild import AbstractGroupChild
from django_cradmin.viewhelpers.listfilter.base.exceptions import InvalidFiltersStringError

standard_library.install_aliases()


class MinimalFilterGroupChild(AbstractGroupChild):
    template_name = 'cradmin_viewhelpers_testapp/listfilter/minimal-filtergroupchild.django.html'


class MinimalIntFilter(AbstractFilter):
    template_name = 'cradmin_viewhelpers_testapp/listfilter/minimal-filtergroupchild.django.html'

    def get_slug(self):
        return 'i'

    def clean_value(self, value):
        return int(value)


class MinimalStringFilter(AbstractFilter):
    template_name = 'cradmin_viewhelpers_testapp/listfilter/minimal-filtergroupchild.django.html'

    def get_slug(self):
        return 's'


class TestAbstractFilterList(TestCase):
    def test_append(self):
        filterlist = AbstractFilterList(urlbuilder=mock.MagicMock())
        testchild = MinimalFilterGroupChild()
        filterlist.append(testchild)
        self.assertEqual([testchild], filterlist.children)
        self.assertEqual(filterlist, testchild.filterlist)

    def test_render(self):
        filterlist = AbstractFilterList(urlbuilder=mock.MagicMock())
        filterlist.append(MinimalFilterGroupChild())
        filterlist.append(MinimalFilterGroupChild())
        selector = htmls.S(filterlist.render())
        self.assertEqual(2, selector.count('li'))

    def test_set_filters_string_invalid_slug(self):
        filterlist = AbstractFilterList(urlbuilder=mock.MagicMock())
        stringfilter = MinimalStringFilter()
        filterlist.append(stringfilter)
        with self.assertRaisesMessage(InvalidFiltersStringError,
                                      '"x" is not a valid filter slug.'):
            filterlist.set_filters_string('x-10')

    def test_set_filters_string(self):
        filterlist = AbstractFilterList(urlbuilder=mock.MagicMock())
        intfilter = MinimalIntFilter()
        stringfilter = MinimalStringFilter()
        filterlist.append(intfilter)
        filterlist.append(stringfilter)
        filterlist.set_filters_string('i-10/s-test')
        self.assertEqual(['10'], intfilter.values)
        self.assertEqual(['test'], stringfilter.values)

    def test_filter(self):
        class FilterOne(AbstractFilter):
            def filter(self, queryobject):
                return queryobject.filter(mycharfield='test')

        class FilterTwo(AbstractFilter):
            def filter(self, queryobject):
                return queryobject.filter(mybooleanfield=True)

        match = mommy.make('cradmin_viewhelpers_testapp.FilterTestModel',
                           mycharfield='test', mybooleanfield=True)
        mommy.make('cradmin_viewhelpers_testapp.FilterTestModel',
                   mycharfield='no match', mybooleanfield=True)
        mommy.make('cradmin_viewhelpers_testapp.FilterTestModel',
                   mycharfield='test', mybooleanfield=False)

        filterlist = AbstractFilterList(urlbuilder=mock.MagicMock())
        filterlist.append(FilterOne(slug='filterone'))
        filterlist.append(FilterTwo(slug='filtertwo'))
        queryset = filterlist.filter(FilterTestModel.objects.all())
        self.assertEqual({match},
                         set(queryset))