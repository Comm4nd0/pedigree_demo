from django import forms
from .models import Pedigree, PedigreeAttributes, PedigreeImage


class PedigreeForm(forms.ModelForm):

    class Meta:
        model = Pedigree
        fields = '__all__'

class AttributeForm(forms.ModelForm):

    class Meta:
        model = PedigreeAttributes
        fields = '__all__'


class ImageForm(forms.ModelForm):
    class Meta:
        model = PedigreeImage
        fields = '__all__'
