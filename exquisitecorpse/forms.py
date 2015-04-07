__author__ = 'jschnall'

from django.core.urlresolvers import reverse
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit, Layout, Fieldset
from crispy_forms.bootstrap import FormActions

from api.models import Composition, Part


class CompositionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CompositionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-compositionForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                'Composition Settings',
                'title',
                'join_policy',
                'turns',
                'max_users',
                'min_part_chars',
                'max_part_chars'
            ),
            FormActions (
                Submit('create', 'Create'),
                Button('cancel', 'Cancel',
                       css_class='btn-default',
                       onclick='window.location.href="{}"'.format(reverse('corpse:dashboard')))
            )
        )

    class Meta:
        model = Composition
        fields = ['max_users', 'title', 'turns', 'min_part_chars', 'max_part_chars', 'join_policy']


class PartForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CompositionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-compositionForm'
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('create', 'Create'))
        self.helper.add_input(Button('cancel', 'Cancel',
                                     css_class='btn-default',
                                     onclick='window.location.href="{}"'.format(reverse('corpse:dashboard'))))
        self.helper.layout = Layout(
            Fieldset(
                'Add text, and a segue for the next player',
                'text',
                'segue',
            ),
        )

    class Meta:
        model = Part
        fields = ['text', 'segue']
