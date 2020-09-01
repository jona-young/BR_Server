from __future__ import absolute_import, unicode_literals
import os
import datetime
from celery import shared_task
from memberexperience.models import memberRecord
from courtinfractions.models import courtInf, contactInfo
from django.core.mail import send_mail
from BR_Server.celeryapp import app as c_app


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

Celery command to start a beat schedule node
    celery -A BR_Server beat
'''

member_staff = os.environ['member_staff']

@c_app.task
def member_email():
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
                           emailStaff=member_staff)
            send_mail(
                subject='B&R Member Experience - {follUp} Follow-Up'.format(follUp=k),
                message=body,
                from_email=None,
                recipient_list=member_staff,
                fail_silently=False
            )


#Court Infractions Email Automation script that sends emails based on specific
#infraction code and counter of that infraction
@shared_task
def email_automation(list):
    for pk in list:
        infInfo = courtInf.objects.get(pk=pk)
        infCount = courtInf.objects.filter(name_id=infInfo.name_id).filter(infraction=infInfo.infraction).count()
        contact = contactInfo.objects.get(pk=infInfo.name_id)
        # TODO - fill this into the recipient list but for now, leave blank
        # email = contact.email

        if infInfo.infraction == 'NS1' and infCount == 1:
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to {email}*

                Hello {name},

                Our records indicate that you did not show for your court reservation on {date} at {time}.

                As this is your first time not showing for your reservation, this is just a friendly reminder of our rules :

                    No shows or late cancellations within 8am the day of game time:  
                    a) the booking Member should contact the Pro Shop to get help finding other players 
                    prior to 24 hours of game time; and 
                    b) if no one signs up to the join the court prior to 24 hours of game time then the BOOKIING
                    MEMBER should cancel the court booking; and
                    c) if the court is left unused without a 24 hour cancellation, then a $25 charge will be applied 
                    to the BOOKING MEMBER; and

                We will not be charging your account, as this is your first time.  Please note, however, that if you do not show for
                another booked court time, you will notice a charge of $25 on your account to reflect this.

                This is all in an effort to provide fair and equitable access to our tennis courts for all our Members.

                Thank you for your understanding,

                {s1}
                {s2}
                {s3}
                {s4}

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime, email=member_staff,
                               s1=os.environ['sig1'], s2=os.environ['sig2'], s3=os.environ['sig3'], s4=os.environ['sig4'])
            send_mail(
                subject='B&R Court Booking Infraction - No Show',
                message=body,
                from_email=None,
                recipient_list=member_staff,
                fail_silently=False
            )
        elif infInfo.infraction == 'NS1' and infCount == 2:
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to {email}*

                Hello {name},

                Our records indicate that you did not show for your court reservation on {date} at {time}.

                    As this is your second occurrence, your name has been added to a monthly tracking list which will
                    be reviewed by our Director of Athletics. Further infractions will be reviewed by our Sports and Activity Committee,
                    leading to potential suspension of booking privileges.  Please note, you will notice a charge of $25 on your account.

                    This is just a friendly reminder of our rules :

                        No shows or late cancellations within 8am the day of game time:  
                        a) the booking Member should contact the Pro Shop to get help finding other players 
                        prior to 24 hours of game time; and 
                        b) if no one signs up to the join the court prior to 24 hours of game time then the BOOKIING
                        MEMBER should cancel the court booking; and
                        c) if the court is left unused without a 24 hour cancellation, then a $25 charge will be applied 
                        to the BOOKING MEMBER

                This is all in an effort to provide fair and equitable access to our tennis courts for all our Members.

                Thank you for your understanding,

                {s1}
                {s2}
                {s3}
                {s4}

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime, email=member_staff,
                               s1=os.environ['sig1'], s2=os.environ['sig2'], s3=os.environ['sig3'], s4=os.environ['sig4'])
            send_mail(
                subject='B&R Court Booking Infraction - No Show (2nd Offense)',
                message=body,
                from_email=None,
                recipient_list=member_staff,
                fail_silently=False
            )
        elif infInfo.infraction == 'NS1' and infCount >= 3:
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to {email}*

                Hello {name},

                Our records indicate that you did not show for your court reservation on {date} at {time}.

                    As this is your third occurrence, this court booking No-Show will be reviewed by our Director of Athletics. Further
                    infractions will be reviewed by our Sports and Activity Committee, leading to potential suspension of booking
                    privileges.  Please note, you will notice a charge of $25 on your account.

                    This is just a friendly reminder of our rules :

                        No shows or late cancellations within 8am the day of game time:  
                        a) the booking Member should contact the Pro Shop to get help finding other players 
                        prior to 24 hours of game time; and 
                        b) if no one signs up to the join the court prior to 24 hours of game time then the BOOKIING
                        MEMBER should cancel the court booking; and
                        c) if the court is left unused without a 24 hour cancellation, then a $25 charge will be applied 
                        to the BOOKING MEMBER

                This is all in an effort to provide fair and equitable access to our tennis courts for all our Members.

                Thank you for your understanding,

                {s1}
                {s2}
                {s3}
                {s4}

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime, email=member_staff,
                               s1=os.environ['sig1'], s2=os.environ['sig2'], s3=os.environ['sig3'], s4=os.environ['sig4'])
            send_mail(
                subject='B&R Court Booking Infraction - No Show (Over 2 Offenses)',
                message=body,
                from_email=None,
                recipient_list=member_staff,
                fail_silently=False
            )
        elif infInfo.infraction == 'LC1' and infCount == 1:
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to {email}*

                Hello {name},

                Our records indicate that you cancelled your court reservation on {date} at {time}.

                As this is your first time cancelling a court, this is just a friendly reminder of our rules :

                    15.5 The Pro Shop must be informed of court cancellations before 8am of the game day or    
                    a $10.00 fee will be applied to the accounts of ALL MEMBERS and Associates who were 
                    booked for play

                We will not be charging your account, as this is your first time.  Please note, however, that if a late cancellation
                is made in the future, you will notice a charge of $10 on your account to reflect this cancellation.

                This is all in an effort to provide fair and equitable access to our tennis courts for all our Members.

                Thank you for your understanding,

                {s1}
                {s2}
                {s3}
                {s4}

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime, email=member_staff,
                               s1=os.environ['sig1'], s2=os.environ['sig2'], s3=os.environ['sig3'], s4=os.environ['sig4'])
            send_mail(
                subject='B&R Court Booking Infraction - Late Cancel',
                message=body,
                from_email=None,
                recipient_list=member_staff,
                fail_silently=False
            )
        elif infInfo.infraction == 'LC1' and infCount == 2:
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to {email}*

                Hello {name},

                Our records indicate that you cancelled your court reservation on {date} at {time}.

                As this is your second occurrence, your name has been added to a monthly tracking list which will be reviewed by
                our Director of Athletics. Further infractions will be reviewed by our Sports and Activity Committee, leading to
                potential suspension of booking privileges. You will notice a charge of $10 on your account.

                This is just a friendly reminder of our rules :

                    15.5 The Pro Shop must be informed of court cancellations before 8am of the game day or    
                    a $10.00 fee will be applied to the accounts of ALL MEMBERS and Associates who were 
                    booked for play

                This is all in an effort to provide fair and equitable access to our tennis courts for all our Members.

                Thank you for your understanding,

                {s1}
                {s2}
                {s3}
                {s4}

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime, email=member_staff,
                               s1=os.environ['sig1'], s2=os.environ['sig2'], s3=os.environ['sig3'], s4=os.environ['sig4'])
            send_mail(
                subject='B&R Court Booking Infraction - Late Cancel (2nd Offense)',
                message=body,
                from_email=None,
                recipient_list=member_staff,
                fail_silently=False
            )
        elif infInfo.infraction == 'LC1' and infCount >= 3:
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to {email}*

                Hello {name},

                Our records indicate that you cancelled your court reservation on {date} at {time}.

                As this is your third occurrence, this court booking Late Cancel will be reviewed by our Director of Athletics.
                Further infractions will be reviewed by our Sports and Activity Committee, leading to potential suspension of
                booking privileges. You will notice a charge of $10 on your account.

                This is just a friendly reminder of our rules :

                    15.5 The Pro Shop must be informed of court cancellations before 8am of the game day or    
                    a $10.00 fee will be applied to the accounts of ALL MEMBERS and Associates who were 
                    booked for play

                This is all in an effort to provide fair and equitable access to our tennis courts for all our Members.

                Thank you for your understanding,

                {s1}
                {s2}
                {s3}
                {s4}

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime, email=member_staff,
                               s1=os.environ['sig1'], s2=os.environ['sig2'], s3=os.environ['sig3'], s4=os.environ['sig4'])
            send_mail(
                subject='B&R Court Booking Infraction - Late Cancel (Over 2 Offenses)',
                message=body,
                from_email=None,
                recipient_list=member_staff,
                fail_silently=False
            )
        elif infInfo.infraction == 'SD1' and infCount == 1:
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to {email}*

                Hello {name},

                Our records indicate that you changed your court reservation from singles to doubles on {date} at {time}.

                As this is your first time adjusting the court booking from singles to doubles, this is just a friendly reminder
                of our rules :

                    15.2    Changing Singles to Doubles
                    “Same Day” Singles to Doubles switching will result in a $10/Member charge for all players 
                    on the court.

                We will not be charging your account, as this is your first time.  Please note, however, that if if a switch to a
                court booking from singles to doubles is made on the day-of, you will notice a charge of $10 on your account to
                reflect.

                This is all in an effort to provide fair and equitable access to our tennis courts for all our Members.

                Thank you for your understanding,

                {s1}
                {s2}
                {s3}
                {s4}

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime, email=member_staff,
                               s1=os.environ['sig1'], s2=os.environ['sig2'], s3=os.environ['sig3'], s4=os.environ['sig4'])
            send_mail(
                subject='B&R Court Booking Infraction - Singles to Doubles',
                message=body,
                from_email=None,
                recipient_list=member_staff,
                fail_silently=False
            )
        elif infInfo.infraction == 'SD1' and infCount == 2:
            body = """
                    *This is an automated email.  If you have questions or concerns, please forward them to {email}*

                    Hello {name},

                    Our records indicate that you changed your court reservation from singles to doubles on {date} at {time}.

                    As this is your second occurrence,your name has been added to a monthly tracking list which will be reviewed by our
                    Director of Athletics. Further infractions will be reviewed by our Sports and Activity Committee, leading to a
                    potential suspension of booking privileges.  You will notice a $10 charge on your account

                    This is just a friendly reminder of our rules :

                        15.2    Changing Singles to Doubles
                        “Same Day” Singles to Doubles switching will result in a $10/Member charge for all players 
                        on the court.

                    This is all in an effort to provide fair and equitable access to our tennis courts for all our Members.

                    Thank you for your understanding,

                    {s1}
                    {s2}
                    {s3}
                    {s4}

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime, email=member_staff,
                               s1=os.environ['sig1'], s2=os.environ['sig2'], s3=os.environ['sig3'], s4=os.environ['sig4'])
            send_mail(
                subject='B&R Court Booking Infraction - Singles to Doubles (2nd Offense)',
                message=body,
                from_email=None,
                recipient_list=member_staff,
                fail_silently=False
            )
        elif infInfo.infraction == 'SD1' and infCount >= 3:
            body = """
                    *This is an automated email.  If you have questions or concerns, please forward them to {email}*

                    Hello {name},

                    Our records indicate that you changed your court reservation from singles to doubles on {date} at {time}.

                    As this is your third occurrence, this court booking Singles-to-Doubles will be reviewed by our Director of Athletics.
                    Further infractions will be reviewed by our Sports and Activity Committee, leading to a potential suspension of
                    booking privileges.  You will notice a $10 charge on your account

                    This is just a friendly reminder of our rules :

                        15.2    Changing Singles to Doubles
                        “Same Day” Singles to Doubles switching will result in a $10/Member charge for all players 
                        on the court.

                    This is all in an effort to provide fair and equitable access to our tennis courts for all our Members.

                    Thank you for your understanding,

                    {s1}
                    {s2}
                    {s3}
                    {s4}

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime, email=member_staff,
                               s1=os.environ['sig1'], s2=os.environ['sig2'], s3=os.environ['sig3'], s4=os.environ['sig4'])
            send_mail(
                subject='B&R Court Booking Infraction - Singles to Doubles (Over 2 Offenses)',
                message=body,
                from_email=None,
                recipient_list=member_staff,
                fail_silently=False
            )
        elif infInfo.infraction == 'GN1':
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to {email}*

                Hello {name},

                Our records indicate that you booked a court on {date} at {time} without a guest name. Please note
                that all guests MUST be booked with their first and last name.

                In an attempt to comply with the Club's tennis court booking policy, any court that has GUEST
                TBA should be updated to reflect the name(s) of your guest(s).

                If you would kindly email us in the future to let us know the name of your guest(s), or contact the
                Pro Shop directly, we would be happy to update your court.

                Please let us know within at least 24 hours notice. Otherwise, the GUEST TBA will be removed and your
                court will be open for others to join.

                This is all in an effort to provide fair and equitable access to our tennis courts for all our Members.

                Thank you for your understanding,

                {s1}
                {s2}
                {s3}
                {s4}

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime, email=member_staff,
                               s1=os.environ['sig1'], s2=os.environ['sig2'], s3=os.environ['sig3'], s4=os.environ['sig4'])
            send_mail(
                subject='B&R Court Booking Infraction - Guest Name',
                message=body,
                from_email=None,
                recipient_list=member_staff,
                fail_silently=False
            )
        else:
            send_mail(
                subject='B&R Court Booking Infraction - Test',
                message='test',
                from_email=None,
                recipient_list=member_staff,
                fail_silently=False
            )