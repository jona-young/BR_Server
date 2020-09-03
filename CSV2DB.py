import os, csv
from courtinfractions.models import contactInfo
from .BR_Server.settings import BASE_DIR

CSV_PATH = '{}nameemail.csv'.format(BASE_DIR)      # Csv file path


with open(CSV_PATH, newline='', encoding="mac_roman") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar=',')
    for row in spamreader:
        contactInfo.objects.create(memberName=row[0], email=row[1])