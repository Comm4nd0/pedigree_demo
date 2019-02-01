from django import forms
from django.forms import ModelForm
from .models import Pedigree, PedigreeAttributes, PedigreeImage
import datetime

class PedigreeForm(forms.Form):

    breeder = forms.CharField(required=False)

    current_owner = forms.CharField(required=False)

    reg_no = forms.CharField(label='Registration Number', required=True)
    reg_no.widget.attrs['class'] = 'form-control'
    reg_no.widget.attrs['placeholder'] = 'P012345'

    name = forms.CharField(label='Name', required=False)
    name.widget.attrs['class'] = 'form-control'

    date_of_registration = forms.DateField(initial=datetime.date.today, required=False,
                                           widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_of_registration.widget.attrs['class'] = 'form-control'
    date_of_registration.widget.attrs['placeholder'] = 'dd/mm/yyyy'

    date_of_birth = forms.DateField(initial=datetime.date.today, required=False,
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_of_birth.widget.attrs['class'] = 'form-control'

    GENDERS = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    sex = forms.ChoiceField(choices=GENDERS, widget=forms.RadioSelect(attrs={'class': 'radio radio-info'}), required=False)

    date_of_death = forms.DateField(initial=datetime.date.today, required=False,
                                           widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_of_death.widget.attrs['class'] = 'form-control'
    date_of_death.widget.attrs['placeholder'] = 'dd/mm/yyyy'

    mother = forms.CharField(required=False)

    father = forms.CharField(required=False)

    description = forms.CharField(widget=forms.Textarea, required=False)
    description.widget.attrs['class'] = 'form-control'

    note = forms.CharField(required=False)
    note.widget.attrs['class'] = 'form-control'


class AttributeForm(forms.Form):

    breed = forms.CharField(required=False)

    eggs_per_week = forms.IntegerField(required=False)
    eggs_per_week.widget.attrs['class'] = 'form-control'
    eggs_per_week.widget.attrs['data-plugin'] = 'vertical-spin'
    eggs_per_week.widget.attrs['data-bts-button-down-class-plugin'] = 'btn btn-secondary btn-outline'
    eggs_per_week.widget.attrs['data-bts-button-up-class'] = 'btn btn-secondary btn-outline'
    eggs_per_week.widget.attrs['value'] = 0

    prize_winning = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox checkbox-success'}), required=False)


class ImagesForm(forms.Form):

    upload_images = forms.ImageField(required=False)
    upload_images.widget.attrs['class'] = 'form-control'
    upload_images.widget.attrs['multiple'] = ''


class PedigreeEditForm(ModelForm):
    class Meta:
        model = Pedigree
        fields = '__all__'


class AttributesEditForm(ModelForm):
    class Meta:
        model = PedigreeAttributes
        fields = '__all__'


class ImagesEditForm(ModelForm):
    class Meta:
        model = PedigreeImage
        fields = '__all__'