from django.template import RequestContext
from django.test import TestCase, RequestFactory
from django_cradmin.viewhelpers import listbuilder


class MinimalRenderable(listbuilder.base.AbstractRenderable):
    template_name = 'cradmin_viewhelpers_testapp/listbuilder/minimal-renderable.django.html'


class TestAbstractRenderable(TestCase):
    def test_get_template_name_no_template_name(self):
        with self.assertRaises(NotImplementedError):
            listbuilder.base.AbstractRenderable().get_template_name()

    def test_get_template_name_has_template_name(self):
        MinimalRenderable().get_template_name()  # NotImplementedError not raised

    def test_get_context_data(self):
        renderable = listbuilder.base.AbstractRenderable()
        self.assertEqual({'me': renderable}, renderable.get_context_data())

    def test_get_template_context_object_without_request(self):
        renderable = listbuilder.base.AbstractRenderable()
        self.assertEqual({'me': renderable}, renderable.get_template_context_object())

    def test_get_template_context_object_with_request(self):
        renderable = listbuilder.base.AbstractRenderable()
        request = RequestFactory().get('')
        context_object = renderable.get_template_context_object(request)
        self.assertTrue(isinstance(context_object, RequestContext))
        self.assertEqual(renderable, context_object['me'])

    def test_render(self):
        self.assertEqual('Test', MinimalRenderable().render().strip())


class TestAbstractItemRenderer(TestCase):
    def test_without_valuealias(self):
        itemrenderer = listbuilder.base.AbstractItemRenderer(value='test')
        self.assertEqual('test', itemrenderer.value)

    def test_with_valuealias(self):
        class MyItemRenderer(listbuilder.base.AbstractItemRenderer):
            valuealias = 'myvalue'

        itemrenderer = MyItemRenderer(value='test')
        self.assertEqual('test', itemrenderer.value)
        self.assertEqual('test', itemrenderer.myvalue)
