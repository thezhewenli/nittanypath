import csv
from django.contrib.auth import get_user_model
from registrar.models import EnrollRecord, Section, Course

# Import Student's data as University Member and Student Profiles
with open('scripts/Enrollment.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    # Create corresponding enrollment entry
    student = get_user_model().objects.get(access_id=row[0])
    course = Course.objects.get(course_id=row[2])
    section = Section.objects.get(course = course, section_num=float(row[1]))
    enroll = EnrollRecord.objects.create(student = student,
                                        course_section = section
                                        )
