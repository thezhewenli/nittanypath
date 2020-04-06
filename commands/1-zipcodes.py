import csv
from django.contrib.auth import get_user_model
from users.models import ZipcodeInfo

# Import Zipcode Information
with open('scripts/Zipcodes.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    record = ZipcodeInfo.objects.create(zipcode=row[0], city = row[1], state = row[2])
    record.save()
