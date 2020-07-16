from django import forms
from .models import courtInf


class multipleForm(forms.Form):
    class Meta:
        model = courtInf
        fields = ['Choices']

    Choices = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=courtInf.objects.all())
