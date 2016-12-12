from django import forms
from django.urls import reverse

from django_cradmin import uicontainer
from django_cradmin.demo.cradmin_javascript_demos.models import FictionalFigureCollection
from django_cradmin.viewhelpers import formview
from django_cradmin.viewhelpers import generic


class Overview(generic.StandaloneBaseTemplateView):
    template_name = 'cradmin_javascript_demos/overview.django.html'


class DateTimePickerDemo(generic.StandaloneBaseTemplateView):
    template_name = 'cradmin_javascript_demos/datetimepicker-demo.django.html'

    def get_javascriptregistry_component_ids(self):
        return ['django_cradmin_javascript']


class TabsDemo(generic.StandaloneBaseTemplateView):
    template_name = 'cradmin_javascript_demos/tabs-demo.django.html'

    def get_javascriptregistry_component_ids(self):
        return ['django_cradmin_javascript']


class DataListWidgetsDemo(generic.StandaloneBaseTemplateView):
    template_name = 'cradmin_javascript_demos/data-list-widgets-demo.django.html'

    def get_javascriptregistry_component_ids(self):
        return ['django_cradmin_javascript']


class DemoForm(forms.ModelForm):
    class Meta:
        model = FictionalFigureCollection
        fields = [
            'name',
            'primary_fictional_figure'
        ]


class DataListWidgetsUicontainerDemo(formview.StandaloneFormView):
    form_class = DemoForm

    def get_pagetitle(self):
        return 'Data list widgets uicontainer demo'

    def get_fictional_figures_api_url(self):
        return reverse('cradmin_javascript_demos_api:fictional-figures-list')

    def get_form_field_renderables(self):
        return [
            uicontainer.fieldwrapper.FieldWrapper(
                fieldname='name'
            ),
            uicontainer.fieldwrapper.FieldWrapper(
                fieldname='primary_fictional_figure',
                field_renderable=uicontainer.foreignkeyfield.Dropdown(
                    api_url=self.get_fictional_figures_api_url()
                )
            ),
        ]

    def get_form_renderable(self):
        return uicontainer.form.Form(
            form=self.get_form(),
            children=[
                uicontainer.layout.AdminuiPageSection(
                    children=[
                        uicontainer.layout.Container(
                            children=self.get_form_field_renderables()
                        )
                    ]
                ),
                uicontainer.layout.AdminuiPageSection(
                    children=[
                        uicontainer.layout.Container(
                            children=[
                                uicontainer.button.SubmitPrimary(text='Create')
                            ]
                        )
                    ]
                )
            ]
        ).bootstrap()

    def get_javascriptregistry_component_ids(self):
        return ['django_cradmin_javascript']

    def form_valid(self, form):
        form.save()
        return super(DataListWidgetsUicontainerDemo, self).form_valid(form)

    def get_success_url(self):
        return self.request.path
