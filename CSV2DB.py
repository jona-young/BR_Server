import csv
from courtinfractions.models import contactInfo

CSV_PATH = '/Users/jonathanyoung/Documents/Django/nameemail.csv'      # Csv file path


with open(CSV_PATH, newline='', encoding="mac_roman") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar=',')
    for row in spamreader:
        contactInfo.objects.create(memberName=row[0], email=row[1])