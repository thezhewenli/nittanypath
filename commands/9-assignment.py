import csv
from registrar.models import Assignment, Course

# Import Student's data as University Member and Student Profiles
with open('scripts/Assignments.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    # Create corresponding assignment entry
    course = Course.objects.get(course_id=row[3])
    assignment = Assignment.objects.create(assignment = row[2], 
                                           course_id = course,
                                           desc = row[0],
                                           detail = row[1]
                                          )
