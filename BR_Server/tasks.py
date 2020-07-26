from __future__ import absolute_import, unicode_literals
import datetime
from time import sleep
from celery import shared_task
from django.core.mail import send_mail
from courtinfractions.models import contactInfo
from memberexperience.models import memberRecord
from BR_Server import secrets
from BR_Server.celeryapp import app

'''
Homebrew commands to start Rabbitmq
    brew services start rabbitmq
    brew services stop rabbitmq
    brew services restart rabbitmq
    brew services list
    
Celery command to start a worker node
    celery -A BR_Server worker --loglevel=info
Celery command to stop the worker...didn't work on MacOS maybe on Linux...
    pkill -9 -f 'celery worker'
    ps auxww | awk '/celery worker/ {print $2}' | xargs kill -9
Celery command to stop worker on Mac OS
    Ctrl + C ...but apparently it does not stop processes according to
    StackOverflow???


Progress - Figured out how to setup a local Rabbitmq server,
           setup celery configuration (celeryapp.py, tasks.py,
           settings.py), and tested tasks through Python Shell

Up Next - Turn the member_email function into a Periodic Task
          function..ideally occuring at the beginning of the day
          but you can use as a test for shorter intervals as well
'''

#Test function for celery...
@shared_task
def reverse(text):
    sleep(5)
    return text[::-1]

#Works if I run it from shell
@shared_task
def member_email():
    memberStaff = secrets.memberStaff
    staffList = secrets.staffList

    threeMth = memberRecord.objects.filter(followUp1=datetime.datetime.today())
    sixMth = memberRecord.objects.filter(followUp2=datetime.datetime.today())
    oneYr = memberRecord.objects.filter(followUp3=datetime.datetime.today())
    followUp = dict()
    followUp['3-mth'] = threeMth
    followUp['6-mth'] = sixMth
    followUp['1-yr'] = oneYr

    for k, v in followUp.items():
        for entry in v:
            contact = contactInfo.objects.get(pk=entry.name_id)
            emailAdd = contact.email

            sportList = list()
            for sport in entry.sportPrefs.all():
                sportList.append(str(sport))

            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to {emailStaff}*

                {name} has reached their {follUp} follow-up period.  Their email is {email}.

                Here are their sport preferences,

                {sports}

                Here are notes on this member,

                {notes}

                """.format(name=entry.name, follUp=k, email=emailAdd, notes=entry.notes, sports=sportList,
                           emailStaff=memberStaff)
            send_mail(
                subject='B&R Member Experience - {follUp} Follow-Up'.format(follUp=k),
                message=body,
                from_email=None,
                recipient_list=memberStaff,
                fail_silently=False
            )

