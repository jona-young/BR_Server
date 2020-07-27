import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from courtinfractions.models import contactInfo

class sportOptions(models.Model):
    sportName = models.CharField(max_length=200)

    def __str__(self):
        return str(self.sportName)


class memberRecord(models.Model):
    name = models.ForeignKey(contactInfo, on_delete=models.PROTECT)
    age = models.IntegerField()
    joinDate = models.DateField(default=timezone.now)
    sportPrefs = models.ManyToManyField(sportOptions)
    followUp1 = models.DateField(default=timezone.now()+datetime.timedelta(days=91))
    followUp2 = models.DateField(default=timezone.now()+datetime.timedelta(days=182))
    followUp3 = models.DateField(default=timezone.now()+datetime.timedelta(days=365))
    notes = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return "{} or {}".format(self.name, self.name_id)

    def get_absolute_url(self):
        return reverse('ME-summary')
