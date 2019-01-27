from django import forms
import datetime

from .models import Breeder

class PedigreeForm(forms.Form):

    breeder = forms.ModelChoiceField(queryset=Breeder.objects.all())
    breeder.widget.attrs['class'] = 'selectpicker mb-3 mr-2'
    breeder.widget.attrs['data-style'] = 'btn-light'

    current_owner = forms.ModelChoiceField(queryset=Breeder.objects.all())
    current_owner.widget.attrs['class'] = 'selectpicker mb-3 mr-2'
    current_owner.widget.attrs['data-style'] = 'btn-light'

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
    # sex.widget.attrs['class'] = 'radio radio-info'


    date_of_death = forms.DateField(initial=datetime.date.today, required=False,
                                           widget=forms.widgets.DateInput(format="%d/%m/%Y", attrs={'type': 'date'}))
    date_of_death.widget.attrs['class'] = 'form-control'
    date_of_death.widget.attrs['placeholder'] = 'dd/mm/yyyy'

    mother = forms.ModelChoiceField(queryset=Breeder.objects.all())
    mother.widget.attrs['class'] = 'selectpicker mb-3 mr-2'
    mother.widget.attrs['data-style'] = 'btn-light'

    father = forms.ModelChoiceField(queryset=Breeder.objects.all())
    father.widget.attrs['class'] = 'selectpicker mb-3 mr-2'
    father.widget.attrs['data-style'] = 'btn-light'