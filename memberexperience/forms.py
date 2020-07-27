from django.forms import ModelMultipleChoiceField
from django.forms import CheckboxSelectMultiple
from django.forms import ModelForm
from .models import memberRecord, sportOptions

class createForm(ModelForm):
    sportPrefs = ModelMultipleChoiceField(
                label='Sport Preferences',
                queryset=sportOptions.objects.filter(),
                widget=CheckboxSelectMultiple
            )

    class Meta:
        model = memberRecord
        fields = [
            'name',
            'age',
            'joinDate',
            'sportPrefs',
            'followUp1',
            'followUp2',
            'followUp3',
            'notes'
        ]
        labels = {
            'followUp1': 'Follow Up Date (3 Months)',
            'followUp2': 'Follow Up Date (6 Months)',
            'followUp3': 'Follow Up Date (1 Year)'
        }


