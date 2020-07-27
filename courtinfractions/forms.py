from django.forms import ModelMultipleChoiceField
from django.forms import CheckboxSelectMultiple
from courtinfractions.models import courtInf
from datetime import datetime as dt
from datetime import date

class multipleForm(forms.Form):
    class Meta:
        model = courtInf
        fields = ['Choices']

    #If the date is Monday all court infraction objects pulled from the past week
    if date.today().weekday() == 0:
        Choices = ModelMultipleChoiceField(widget=CheckboxSelectMultiple,
                                           queryset=courtInf.objects.filter(
                                               date__range=[(dt.today() + dt.timedelta(days=-7)), dt.today()]))
    #If the date is not Monday, all court infractions still pulled from past week starting Monday
    else:
        day_mod = date.today().weekday()
        Choices = ModelMultipleChoiceField(widget=CheckboxSelectMultiple,
                                           queryset=courtInf.objects.filter(
                                               date__range=[(dt.today() + dt.timedelta(days=-(7+day_mod))),
                                                            (dt.today() + dt.timedelta(days=-day_mod))]))
