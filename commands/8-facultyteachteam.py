import csv
from django.contrib.auth import get_user_model
from registrar.models import FacultyTeachTeam

# Import Student's data as University Member and Student Profiles
with open('scripts/FacultyTeachTeam.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    # Create corresponding faulty teaching entry
    faculty = get_user_model().objects.get(access_id=row[0])
    faculty_teach = FacultyTeachTeam.objects.create(faculty = faculty,
                                        teaching_team_id = row[1]
                                        )
