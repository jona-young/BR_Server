from django import forms
from .models import courtInf
import datetime

class multipleForm(forms.Form):
    class Meta:
        model = courtInf
        fields = ['Choices']

    #If the date is Monday all court infraction objects pulled from the past week
    if datetime.date.today().weekday() == 0:
        Choices = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                 queryset=courtInf.objects.filter(
                                                     date__range=[
                                                         (datetime.datetime.today() + datetime.timedelta(days=-7)),
                                                         datetime.datetime.today()]))
    #If the date is not Monday, all court infractions still pulled from past week starting Monday
    else:
        day_mod = datetime.date.today().weekday()

        Choices = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                 queryset=courtInf.objects.filter(
                                                     date__range=[
                                                         (datetime.datetime.today() + datetime.timedelta(days=-(7+day_mod))),
                                                        (datetime.datetime.today() + datetime.timedelta(days=-day_mod))]))
