import csv
from django.contrib.auth import get_user_model
from registrar.models import Assignment, AssignmentGrade

with open('scripts/AssignmentGrades.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    # Create corresponding grade entry
    assignment = Assignment.objects.get(assignment=row[2])
    student = get_user_model().objects.get(access_id=row[0])
    assignment_grade = AssignmentGrade.objects.create(assignment = assignment, 
                                                      student = student,
                                                      grade = row[1]
                                                      )
