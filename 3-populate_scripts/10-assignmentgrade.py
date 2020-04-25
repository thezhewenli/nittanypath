import csv
from django.contrib.auth import get_user_model
from registrar.models import Assignment, AssignmentGrade, Course, Department

with open('../2-data_parser/10-AssignmentsAndGrades.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    # For each assignment grade record, check if the assignment exist
    # Create one if not exist
    dept = Department.objects.get(department_id = row[4])
    course = Course.objects.get(subject=dept, course_number=row[5])
    assignment = Assignment.objects.get_or_create(course_id=course, desc=row[1], detail=row[2])

    # And create a grade entry
    student = get_user_model().objects.get(access_id=row[0])
    assignment_grade = AssignmentGrade.objects.create(assignment = assignment[0], 
                                                      student = student,
                                                      grade = row[3]
                                                      )
