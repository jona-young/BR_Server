from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class contactInfo(models.Model):
    memberName = models.CharField(max_length=200)
    email = models.CharField(max_length=254)

    def __str__(self):
        return self.memberName


class courtInf(models.Model):

    codeInf=[
        ('LC1', 'Late Cancel'),
        ('NS1', 'No Show'),
        ('SD1', 'Singles to Doubles'),
        ('GN1', 'Guest Name'),
        ('OTH', 'Other (Please specify in notes)'),
    ]
    codeTime=[
        ('5:40 AM', '5:40 AM'),
        ('6:00 AM', '6:00 AM'),
        ('6:20 AM', '6:20 AM'),
        ('7:00 AM', '7:00 AM'),
        ('7:40 AM', '7:40 AM'),
        ('8:00 AM', '8:00 AM'),
        ('8:20 AM', '8:20 AM'),
        ('9:00 AM', '9:00 AM'),
        ('9:40 AM', '9:40 AM'),
        ('10:00 AM', '10:00 AM'),
        ('10:20 AM', '10:20 AM'),
        ('11:00 AM', '11:00 AM'),
        ('11:40 AM', '11:40 AM'),
        ('12:00 PM', '12:00 PM'),
        ('12:15 PM', '12:15 PM'),
        ('12:20 PM', '12:20 PM'),
        ('1:00 PM', '1:00 PM'),
        ('1:15 PM', '1:15 PM'),
        ('1:40 PM', '1:40 PM'),
        ('2:00 PM', '2:00 PM'),
        ('2:15 PM', '2:15 PM'),
        ('2:20 PM', '2:20 PM'),
        ('3:00 PM', '3:00 PM'),
        ('3:30 PM', '3:30 PM'),
        ('3:40 PM', '3:40 PM'),
        ('4:00 PM', '4:00 PM'),
        ('4:20 PM', '4:20 PM'),
        ('4:30 PM', '4:30 PM'),
        ('5:00 PM', '5:00 PM'),
        ('5:30 PM', '5:30 PM'),
        ('5:40 PM', '5:40 PM'),
        ('6:00 PM', '6:00 PM'),
        ('6:20 PM', '6:20 PM'),
        ('6:30 PM', '6:30 PM'),
        ('7:00 PM', '7:00 PM'),
        ('7:30 PM', '7:30 PM'),
        ('7:40 PM', '7:40 PM'),
        ('8:00 PM', '8:00 PM'),
        ('8:20 PM', '8:20 PM'),
        ('8:30 PM', '8:30 PM'),
        ('9:00 PM', '9:00 PM'),
        ('9:30 PM', '9:30 PM'),
        ('9:40 PM', '9:40 PM'),
        ]

    #Drop down list would switch name to ForeignKey link with contactInfo model 'name'
    name = models.ForeignKey(contactInfo, on_delete=models.PROTECT)
    sport = models.CharField(max_length=2, choices=[
        ('TN', 'Tennis'), ('SQ', 'Squash'), ('BM', 'Badminton'),
        ('PB', 'Pickleball'), ('PT', 'Platform Tennis')
    ])
    infraction = models.CharField(max_length=3, choices=codeInf)
    date = models.DateField(default=timezone.now)
    courtTime = models.CharField(max_length=8, choices=codeTime)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    #Returns the infraction of a court infraction when it is called in the shell
    def __str__(self):
        return '{}({}) on {} at {}'.format(self.name, self.infraction,
                                           self.date, self.courtTime)

    def get_absolute_url(self):
        return reverse('CI-summary')
