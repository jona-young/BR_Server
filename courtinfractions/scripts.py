from .models import courtInf, contactInfo
from django.core.mail import send_mail

#TODO - adjust email var in each sendmail() to infInfo and contactInfo email...

staffList = [
    'eric@thebandr.com',
    'catherine@thebandr.com',
    'kira@thebandr.com',
    'tom@thebandr.com',
    'jonathan@thebandr.com',
]

def emailAutomation(list):
    for pk in list:
        infInfo = courtInf.objects.get(pk=pk)
        infCount = courtInf.objects.filter(name_id=infInfo.name_id).filter(infraction=infInfo.infraction).count()
        contact = contactInfo.objects.get(pk=infInfo.name_id)
        # TODO - fill this into the recipient list but for now, leave blank
        #email = contact.email
        email = ['jonathanster.young@me.com']

        if infInfo.infraction == 'NS1' and infCount == 1:
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*
                
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
                
                Jonathan Young | Sports Administrator
                The Badminton and Racquet Club of Toronto
                25 St. Clair Avenue West, Toronto ON M4V 1K6
                E jonathan@thebandr.com W thebandr.com
                
                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime)
            send_mail(
                subject='B&R Court Booking Infraction - No Show',
                message=body,
                from_email=None,
                recipient_list=email,
                fail_silently=False
            )
        elif infInfo.infraction == 'NS1' and infCount == 2:
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

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

                Jonathan Young | Sports Administrator
                The Badminton and Racquet Club of Toronto
                25 St. Clair Avenue West, Toronto ON M4V 1K6
                E jonathan@thebandr.com W thebandr.com

                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime)
            send_mail(
                subject='B&R Court Booking Infraction - No Show (2nd Offense)',
                message=body,
                from_email=None,
                recipient_list=email,
                fail_silently=False
            )
        elif infInfo.infraction == 'NS1' and infCount >= 3:
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

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

                Jonathan Young | Sports Administrator
                The Badminton and Racquet Club of Toronto
                25 St. Clair Avenue West, Toronto ON M4V 1K6
                E jonathan@thebandr.com W thebandr.com

                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime)
            send_mail(
                subject='B&R Court Booking Infraction - No Show (Over 2 Offenses)',
                message=body,
                from_email=None,
                #TODO Place 'staffList' under recipientlist
                recipient_list=email,
                fail_silently=False
            )
        elif infInfo.infraction =='LC1' and infCount == 1:
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

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

                Jonathan Young | Sports Administrator
                The Badminton and Racquet Club of Toronto
                25 St. Clair Avenue West, Toronto ON M4V 1K6
                E jonathan@thebandr.com W thebandr.com

                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime)
            send_mail(
                subject='B&R Court Booking Infraction - Late Cancel',
                message=body,
                from_email=None,
                recipient_list=email,
                fail_silently=False
            )
        elif infInfo.infraction == 'LC1' and infCount == 2:
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

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

                Jonathan Young | Sports Administrator
                The Badminton and Racquet Club of Toronto
                25 St. Clair Avenue West, Toronto ON M4V 1K6
                E jonathan@thebandr.com W thebandr.com

                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime)
            send_mail(
                subject='B&R Court Booking Infraction - Late Cancel (2nd Offense)',
                message=body,
                from_email=None,
                recipient_list=email,
                fail_silently=False
            )
        elif infInfo.infraction == 'LC1' and infCount >= 3:
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

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

                Jonathan Young | Sports Administrator
                The Badminton and Racquet Club of Toronto
                25 St. Clair Avenue West, Toronto ON M4V 1K6
                E jonathan@thebandr.com W thebandr.com

                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime)
            send_mail(
                subject='B&R Court Booking Infraction - Late Cancel (Over 2 Offenses)',
                message=body,
                from_email=None,
                #TODO Place 'staffList' under recipientlist
                recipient_list=email,
                fail_silently=False
            )
        elif infInfo.infraction == 'SD1' and infCount == 1:
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

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

                Jonathan Young | Sports Administrator
                The Badminton and Racquet Club of Toronto
                25 St. Clair Avenue West, Toronto ON M4V 1K6
                E jonathan@thebandr.com W thebandr.com

                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime)
            send_mail(
                subject='B&R Court Booking Infraction - Singles to Doubles',
                message=body,
                from_email=None,
                recipient_list=email,
                fail_silently=False
            )
        elif infInfo.infraction == 'SD1' and infCount == 2:
            body = """
                    *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*
    
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
    
                    Jonathan Young | Sports Administrator
                    The Badminton and Racquet Club of Toronto
                    25 St. Clair Avenue West, Toronto ON M4V 1K6
                    E jonathan@thebandr.com W thebandr.com
    
                    *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*
    
                        """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime)
            send_mail(
                subject='B&R Court Booking Infraction - Singles to Doubles (2nd Offense)',
                message=body,
                from_email=None,
                recipient_list=email,
                fail_silently=False
            )
        elif infInfo.infraction == 'SD1' and infCount >= 3:
            body = """
                    *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

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

                    Jonathan Young | Sports Administrator
                    The Badminton and Racquet Club of Toronto
                    25 St. Clair Avenue West, Toronto ON M4V 1K6
                    E jonathan@thebandr.com W thebandr.com

                    *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

                        """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime)
            send_mail(
                subject='B&R Court Booking Infraction - Singles to Doubles (Over 2 Offenses)',
                message=body,
                from_email=None,
                # TODO Place 'staffList' under recipientlist
                recipient_list=email,
                fail_silently=False
            )
        elif infInfo.infraction == 'GN1':
            body = """
                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

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

                Jonathan Young | Sports Administrator
                The Badminton and Racquet Club of Toronto
                25 St. Clair Avenue West, Toronto ON M4V 1K6
                E jonathan@thebandr.com W thebandr.com

                *This is an automated email.  If you have questions or concerns, please forward them to jonathan@thebandr.com*

                    """.format(name=infInfo.name, date=infInfo.date, time=infInfo.courtTime)
            send_mail(
                subject='B&R Court Booking Infraction - Guest Name',
                message=body,
                from_email=None,
                recipient_list=email,
                fail_silently=False
            )
        else:
            send_mail(
                subject='B&R Court Booking Infraction - Test',
                message='test',
                from_email=None,
                recipient_list=email,
                fail_silently=False
            )