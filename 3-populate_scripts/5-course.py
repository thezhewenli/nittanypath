import csv
import datetime 
from registrar.models import Department, Course
from pytz import timezone

eastern = timezone('US/Eastern')
# Import Student's data as University Member and Student Profiles
with open('../2-data_parser/3-Courses.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    # Create corresponding Course entry
    dept = Department.objects.get(department_id = row[2])
    year = '20%s' % row[4][6:8]
    month = row[4][0:2]
    day = row[4][3:5]
    d = datetime.datetime(int(year), int(month), int(day), 23, 59, 59, tzinfo=eastern)
    course = Course.objects.create(subject = dept,
                                        course_number = row[3],
                                        course_name = row[0],
                                        credit = row[1],
                                        drop_ddl = d,
                                        )
    course.save()
