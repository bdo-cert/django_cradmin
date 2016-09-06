from django import test

from django_cradmin import javascriptregistry
from django_cradmin.javascriptregistry.component import AbstractJsComponent


class MinimalAbstractJsComponent(javascriptregistry.component.AbstractJsComponent):
    @classmethod
    def get_component_id(cls):
        return 'minimal'


class TestAbstractJsComponent(test.TestCase):
    def test_get_component_id(self):
        with self.assertRaises(NotImplementedError):
            javascriptregistry.component.AbstractJsComponent.get_component_id()

    def test__init__component_id_uppercase_not_allowed(self):
        class MockJsComponent(AbstractJsComponent):
            @classmethod
            def get_component_id(cls):
                return 'Hello'

        with self.assertRaises(javascriptregistry.component.ComponentIdFormatError):
            MockJsComponent(request=None)

    def test__init__component_id_minus_not_allowed(self):
        class MockJsComponent(AbstractJsComponent):
            @classmethod
            def get_component_id(cls):
                return 'he-lo'

        with self.assertRaises(javascriptregistry.component.ComponentIdFormatError):
            MockJsComponent(request=None)

    def test__init__component_id_underscore_last_not_allowed(self):
        class MockJsComponent(AbstractJsComponent):
            @classmethod
            def get_component_id(cls):
                return 'hello_'

        with self.assertRaises(javascriptregistry.component.ComponentIdFormatError):
            MockJsComponent(request=None)

    def test__init__component_id_underscore_first_not_allowed(self):
        class MockJsComponent(AbstractJsComponent):
            @classmethod
            def get_component_id(cls):
                return '_hello'

        with self.assertRaises(javascriptregistry.component.ComponentIdFormatError):
            MockJsComponent(request=None)

    def test__init__component_id_number_first_not_allowed(self):
        class MockJsComponent(AbstractJsComponent):
            @classmethod
            def get_component_id(cls):
                return '1hello'

        with self.assertRaises(javascriptregistry.component.ComponentIdFormatError):
            MockJsComponent(request=None)

    def test__init__component_id_underscore_middle_allowed(self):
        class MockJsComponent(AbstractJsComponent):
            @classmethod
            def get_component_id(cls):
                return 'he_lo'

        MockJsComponent(request=None)  # No ComponentIdFormatError

    def test__init__component_id_number_middle_allowed(self):
        class MockJsComponent(AbstractJsComponent):
            @classmethod
            def get_component_id(cls):
                return 'he3lo'

        MockJsComponent(request=None)  # No ComponentIdFormatError

    def test__init__component_id_number_last_allowed(self):
        class MockJsComponent(AbstractJsComponent):
            @classmethod
            def get_component_id(cls):
                return 'hello1'

        MockJsComponent(request=None)  # No ComponentIdFormatError

    def test_get_dependencies(self):
        self.assertEqual([], MinimalAbstractJsComponent(request=None).get_dependencies())

    def test_get_head_sourceurls(self):
        self.assertEqual([], MinimalAbstractJsComponent(request=None).get_head_sourceurls())

    def test_get_sourceurls(self):
        self.assertEqual([], MinimalAbstractJsComponent(request=None).get_sourceurls())

    def test_get_javascript_code_before_sourceurls(self):
        self.assertIsNone(MinimalAbstractJsComponent(request=None).get_javascript_code_before_sourceurls())

    def test_get_javascript_code_after_sourceurls(self):
        self.assertIsNone(MinimalAbstractJsComponent(request=None).get_javascript_code_after_sourceurls())

    def test_get_static_url(self):
        self.assertEqual(
            '/static/test', MinimalAbstractJsComponent(request=None).get_static_url(path='test'))


class MinimalCradminAngular1(javascriptregistry.component.CradminAngular1):
    @classmethod
    def get_component_id(cls):
        return 'minimal'

    def get_target_domelement_selector(self):
        return '#id_test'


class TestCradminAngular1(test.TestCase):
    def test_get_component_id(self):
        with self.assertRaises(NotImplementedError):
            javascriptregistry.component.AbstractJsComponent.get_component_id()

    def test_get_target_domelement_selector(self):
        class MockCradminAngular1(javascriptregistry.component.CradminAngular1):
            @classmethod
            def get_component_id(cls):
                return 'minimal'

        with self.assertRaises(NotImplementedError):
            MockCradminAngular1(request=None).get_target_domelement_selector()

    def test_get_head_sourceurls(self):
        self.assertEqual(
            [
                '/static/django_cradmin/dist/vendor/cradmin-vendorjs.js',
                '/static/django_cradmin/dist/js/cradmin.min.js'
            ],
            MinimalCradminAngular1(request=None).get_head_sourceurls())

    def test_get_angularjs_modules(self):
        self.assertEqual(
            [],
            MinimalCradminAngular1(request=None).get_angularjs_modules())

    def test_get_javascript_code_after_sourceurls(self):
        class MockCradminAngular1(javascriptregistry.component.CradminAngular1):
            @classmethod
            def get_component_id(cls):
                return 'mock'

            def get_target_domelement_selector(self):
                return '#id_mock'

        js = MockCradminAngular1(request=None).get_javascript_code_after_sourceurls()

        self.assertTrue(
            'angular.module("MockApp", []);\n'
            'angular.bootstrap(document.querySelector("#id_mock"), ["MockApp"])',
            js)

    def test_get_javascript_code_after_sourceurls_with_modules(self):
        class MockCradminAngular1(javascriptregistry.component.CradminAngular1):
            @classmethod
            def get_component_id(cls):
                return 'mock'

            def get_target_domelement_selector(self):
                return '#id_mock'

            def get_angularjs_modules(self):
                return ['myapp.forms', 'myapp.modal']

        js = MockCradminAngular1(request=None).get_javascript_code_after_sourceurls()

        self.assertTrue(
            'angular.module("MockApp", ["myapp.forms", "myapp.modal"]);\n'
            'angular.bootstrap(document.querySelector("#id_mock"), ["MockApp"])',
            js)


class TestCradminMenu(test.TestCase):
    def test_get_component_id(self):
        self.assertEqual(
            'django_cradmin_mainmenu',
            javascriptregistry.component.CradminMenu.get_component_id())

    def test_get_target_domelement_selector(self):
        self.assertEqual(
            '#id_django_cradmin_mainmenu',
            javascriptregistry.component.CradminMenu(request=None).get_target_domelement_selector())

    def test_get_angularjs_modules(self):
        self.assertEqual(
            ['djangoCradmin.menu'],
            javascriptregistry.component.CradminMenu(request=None).get_angularjs_modules())