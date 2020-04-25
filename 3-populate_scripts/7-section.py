import csv
from registrar.models import Section, Course, Department, FacultyTeachTeam

# Import Student's data as University Member and Student Profiles
with open('../2-data_parser/4-Sections.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    # Create corresponding Section entry
    dept = Department.objects.get(department_id = row[2])
    course = Course.objects.get(subject=dept, course_number=row[3])
    teachteam = FacultyTeachTeam.objects.get(teaching_team_id=row[4])
    section = Section.objects.create(course = course,
                                        section_num = float(row[0]),
                                        capacity_limit = row[1],
                                        teaching_team_id = teachteam
                                        )
