from django import forms
import datetime

from .models import Breeder, Pedigree

class PedigreeForm(forms.Form):

    breeder = forms.ModelChoiceField(queryset=Breeder.objects.all())
    breeder.widget.attrs['class'] = 'selectpicker mb-3 mr-2'
    breeder.widget.attrs['data-style'] = 'btn-success'

    current_owner = forms.ModelChoiceField(queryset=Breeder.objects.all())
    current_owner.widget.attrs['class'] = 'selectpicker mb-3 mr-2'
    current_owner.widget.attrs['data-style'] = 'btn-success'

    reg_no = forms.CharField(label='Registration Number', required=True)
    reg_no.widget.attrs['class'] = 'form-control'
    reg_no.widget.attrs['placeholder'] = 'P012345'

    name = forms.CharField(label='Name', required=True)
    name.widget.attrs['class'] = 'form-control'

    date_of_registration = forms.DateField(initial=datetime.date.today, required=False,
                                           widget=forms.widgets.DateInput(format="%d/%m/%Y", attrs={'type': 'date'}))
    date_of_registration.widget.attrs['class'] = 'form-control'
    date_of_registration.widget.attrs['placeholder'] = 'dd/mm/yyyy'

    date_of_birth = forms.DateField(initial=datetime.date.today, required=True,
                                    widget=forms.widgets.DateInput(format="%d/%m/%Y", attrs={'type': 'date'}))
    date_of_birth.widget.attrs['class'] = 'form-control'

    GENDERS = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    sex = forms.ChoiceField(choices=GENDERS, widget=forms.RadioSelect(attrs={'class': 'radio radio-info'}), initial=1)

    date_of_death = forms.DateField(initial=datetime.date.today, required=False,
                                           widget=forms.widgets.DateInput(format="%d/%m/%Y", attrs={'type': 'date'}))
    date_of_death.widget.attrs['class'] = 'form-control'
    date_of_death.widget.attrs['placeholder'] = 'dd/mm/yyyy'

    mother = forms.ModelChoiceField(queryset=Pedigree.objects.all())
    mother.widget.attrs['class'] = 'selectpicker mb-3 mr-2'
    mother.widget.attrs['data-style'] = 'btn-primary'

    father = forms.ModelChoiceField(queryset=Pedigree.objects.all())
    father.widget.attrs['class'] = 'selectpicker mb-3 mr-2'
    father.widget.attrs['data-style'] = 'btn-info'

    description = forms.CharField(widget=forms.Textarea, required=False)

    note = forms.CharField(required=False)
    note.widget.attrs['class'] = 'form-control'


class AttributeForm(forms.Form):

    eggs_per_week = forms.IntegerField()
    eggs_per_week.widget.attrs['class'] = 'form-control'
    eggs_per_week.widget.attrs['data-plugin'] = 'vertical-spin'
    eggs_per_week.widget.attrs['data-bts-button-down-class-plugin'] = 'btn btn-secondary btn-outline'
    eggs_per_week.widget.attrs['data-bts-button-up-class'] = 'btn btn-secondary btn-outline'

    prize_winning = forms.ChoiceField(widget=forms.CheckboxInput(attrs={'class': 'checkbox checkbox-success'}))
