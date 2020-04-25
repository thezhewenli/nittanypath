import csv
from registrar.models import Section, Course

# Import Student's data as University Member and Student Profiles
with open('scripts/CoursesSection.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    # Create corresponding Section entry
    course = Course.objects.get(course_id = row[0])
    section = Section.objects.create(course = course,
                                        section_num = float(row[2]),
                                        capacity_limit = row[3],
                                        teaching_team_id = row[1]
                                        )
