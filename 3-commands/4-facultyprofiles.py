import csv
from django.contrib.auth import get_user_model
from users.models import FacultyProfile
from registrar.models import Department

# Import Student's data as University Member and Student Profiles
with open('scripts/FacultyProfiles.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:

    # Create a user for the student
    extra_fields = {
      'legal_name': row[0],
      'age': row[3],
      'legal_gender': row[4],
      'primary_affiliation': '1',
    }
    user = get_user_model().objects.create_user(access_id=row[1], 
      password=row[2], **extra_fields)
    user.save()

    # Create corresponding Faculty Profile
    dept = Department.objects.get(department_id = row[5])
    faculty_profile = FacultyProfile.objects.create(user=user, department_id=dept, office=row[6], title=row[7])
