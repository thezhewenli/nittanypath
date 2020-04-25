import csv
from django.contrib.auth import get_user_model
from users.models import StudentProfile, TAProfile, ZipcodeInfo
from registrar.models import Department

# Import Student's data as University Member and Student Profiles
with open('scripts/StudentProfiles.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:

    # Create a user for the student
    extra_fields = {
      'legal_name': row[0],
      'age': row[2],
      'legal_gender': row[5],
      'primary_affiliation': '2',
    }
    user = get_user_model().objects.create_user(access_id=row[1], 
      password=row[6], **extra_fields)
    user.save()

    # Create corresponding Student Profile
    dept = Department.objects.get(department_id = row[8])
    home_zipcode = ZipcodeInfo.objects.get(zipcode = row[3])
    stu_profile = StudentProfile.objects.create(user=user, major_id = dept, 
                                                phone = row[4], home_zipcode=home_zipcode,
                                                home_street_address=row[7])
    
    # If student's also a TA
    # Create corresponding TA Profile
    if row[9] != '':
      ta_profile = TAProfile.objects.create(user=user, teaching_team=float(row[9]))