import csv
from django.contrib.auth import get_user_model
from registrar.models import Department

# Import Zipcode Information
with open('../2-data_parser/6-Depts.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    record = Department.objects.create(department_id=row[0], department_name = row[1])
    record.save()
