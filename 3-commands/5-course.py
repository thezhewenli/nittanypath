import csv
from registrar.models import Department, Course

# Import Student's data as University Member and Student Profiles
with open('scripts/CoursesTable.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    # Create corresponding Course entry
    dept = Department.objects.get(department_id = row[2])
    course = Course.objects.create(course_id = row[4],
                                        subject = dept,
                                        course_number = row[3],
                                        course_name = row[0],
                                        credit = row[1],
                                        drop_ddl = row[5],
                                        )
