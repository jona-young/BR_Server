from django import forms
from django.forms import ModelForm
from .models import memberRecord, sportOptions

class createForm(ModelForm):
    sportPreference = forms.ModelMultipleChoiceField(
        queryset=sportOptions.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = memberRecord
        fields = [
            'name',
            'age',
            'joinDate',
            'sportPreference',
            'followUp1',
            'followUp2',
            'followUp3',
            'notes'
        ]