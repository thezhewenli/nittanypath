import pandas as pd
from os import path

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Given a dataframe `df`
# Check if `df` has any record violates `given` -> `determined`
def checkFDViolation(df, given, filepath_tosave):
  df_nodup = df.drop_duplicates()
  resultdf = df_nodup[df_nodup.sort_values(given).duplicated()]
  if resultdf.empty:
    # removed all duplicates
    # and save to new file
    df_nodup.to_csv(filepath_tosave, index=False, header=False)
    return True
  else:
    return False

def parseStudentProfile(df, filepath_tosave):
  # Normalize email to access id
  df['Email'] = df['Email'].str[:6]
  df.to_csv(filepath_tosave, index=False, header=False)
  return True


def main():
  # make sure all three files exist
  if not (path.exists('Students_TA.csv') and path.exists('Posts_Comments.csv') and path.exists("Professors.csv")):
    return (bcolors.WARNING + "Error. Cannot Find All Three Files!")
  
  df1 = pd.read_csv('Students_TA.csv', sep=',')
  df2 = pd.read_csv('Professors.csv', sep=',')
  df3 = pd.read_csv('Posts_Comments.csv', sep=',')
  
  # Select Zipcode-related columns
  zipdf = df1.iloc[:,[3,6,7]]
  # Return error if FD violation exists
  # Or save processed data to a new csv
  if not checkFDViolation(zipdf, 'Zip', 'Zipcodes.csv'):
    return (bcolors.WARNING + "Error. FD Violations exist!")
  print (bcolors.OKGREEN + "Zipcode data parsed and file created.")

  # Select student profile related columns and normalize email to access id
  studentdf = df1.iloc[:,[0,1,2,3,4,5,8,9,10,44]]
  studentdf['Email'] = studentdf['Email'].str[:6]
  studentdf.to_csv('StudentProfiles.csv', index=False, header=False)
  print (bcolors.OKGREEN + "Student Profile data parsed and file created.")

  # Parse course and teaching team data
  course1df = df1.iloc[:,[11,12,13]]
  course1df = course1df.rename(columns={"Courses 1": "course", "Course 1 Name": "course_name", "Course 1 Details": "course_credit"})
  course2df = df1.iloc[:,[22,23,24]]
  course2df = course2df.rename(columns={"Courses 2": "course", "Course 2 Name": "course_name", "Course 2 Details": "course_credit"})
  course3df = df1.iloc[:,[33,34,35]]
  course3df = course3df.rename(columns={"Courses 3": "course", "Course 3 Name": "course_name", "Course 3 Details": "course_credit"})

  # Parse course and section offering data
  course1sectiondf = df1.iloc[:,[11,14,15]]
  course1sectiondf = course1sectiondf.rename(columns={"Courses 1": "course", "Course 1 Section": "section", "Course 1 Section Limit": "limit"})
  course2sectiondf = df1.iloc[:,[22,25,26]]
  course2sectiondf = course2sectiondf.rename(columns={"Courses 2": "course", "Course 2 Section": "section", "Course 2 Section Limit": "limit"})
  course3sectiondf = df1.iloc[:,[33,36,37]]
  course3sectiondf = course3sectiondf.rename(columns={"Courses 3": "course", "Course 3 Section": "section", "Course 3 Section Limit": "limit"})
  temp_secframes = [course1sectiondf, course2sectiondf, course3sectiondf]
  tempsecdf = pd.concat(temp_secframes)
  course_section_df = tempsecdf.drop_duplicates()

  temp_frames = [course1df, course2df, course3df]
  tempcoursedf = pd.concat(temp_frames)
  tempcoursedf = tempcoursedf.drop_duplicates()
  tempcoursedf['course_credit'] = tempcoursedf['course_credit'].str[:1]
  
  course_teach_team = df2.iloc[:,9:11]
  coursedf = pd.merge(left=tempcoursedf, right=course_teach_team, how='left', left_on='course', right_on='Teaching')
  coursedf = coursedf.iloc[:,:-1]
  coursedf['subject'] = coursedf['course'].str[:-3]
  coursedf['course_num'] = coursedf['course'].str[-3:]
  coursedf.loc[coursedf['subject']=='CMPSC4','course_num'] = '431W'
  coursedf.loc[coursedf['subject']=='CMPSC4','subject'] = 'CMPSC'
  coursedf['course_pk'] = range(1, len(coursedf)+1)

  course_ddl_df = df3.iloc[:,[0,1]]
  coursedf = pd.merge(left=coursedf, right=course_ddl_df, how='left', left_on='course', right_on='Courses')

  # Extract to Course and Section tables
  result_df = pd.merge(left=coursedf, right=course_section_df, how='right', left_on='course', right_on='course')
  course_section_df = result_df.iloc[:,[3,6,9,10]]
  course_db_df = coursedf.iloc[:,[1,2,4,5,6,8]]
  # And create files
  course_db_df.to_csv('CoursesTable.csv', index=False, header=False)
  course_section_df.to_csv('CoursesSection.csv', index=False, header=False)
  print (bcolors.OKGREEN + "Course and Section data parsed and file created.")

  # Parse student enrollment data
  enroll1df = df1.iloc[:,[1,11,14]]
  enroll1df = enroll1df.rename(columns={"Email":"access_id", "Courses 1": "course", "Course 1 Section":"section"})
  enroll2df = df1.iloc[:,[1,22,25]]
  enroll2df = enroll2df.rename(columns={"Email":"access_id", "Courses 2": "course", "Course 2 Section":"section"})
  enroll3df = df1.iloc[:,[1,33,36]]
  enroll3df = enroll3df.rename(columns={"Email":"access_id", "Courses 3": "course", "Course 3 Section":"section"})
  
  temp_enroll_frames = [enroll1df, enroll2df, enroll3df]
  temp_enroll_frames = pd.concat(temp_enroll_frames)
  enroll_df = temp_enroll_frames.drop_duplicates()

  enroll_df['access_id'] = enroll_df['access_id'].str[:6]
  enroll_df = pd.merge(left=enroll_df, right=coursedf, how='left', left_on='course', right_on='course')
  enroll_df.iloc[:,[0,2,8]].to_csv('Enrollment.csv', index=False, header=False)
  print (bcolors.OKGREEN + "Course Enrollment data parsed and file created.")
  
  # Populate Department table
  df2.iloc[:,[5,7]].drop_duplicates().to_csv('Depts.csv', index=False, header=False)

  # Populate FacultyTeachingTeam table
  faulty_teachteam_df = df2.iloc[:,[1,-2]]
  faulty_teachteam_df['Email'] = faulty_teachteam_df['Email'].str[:-12]
  faulty_teachteam_df.drop_duplicates().to_csv('FacultyTeachTeam.csv', index=False, header=False)

  # Populate Faculty Profile table
  faculty_info_df = df2.iloc[:,[0,1,2,3,4,5,6,8]].drop_duplicates()
  faculty_info_df['Email'] = faculty_info_df['Email'].str[:-12]
  faculty_info_df.drop_duplicates().to_csv('FacultyProfiles.csv', index=False, header=False)

  # Populate Post & Reply data
  post_reply_df = pd.merge(left=df3, right=coursedf, how='left', left_on='Courses', right_on='course')
  post_reply_df = post_reply_df.iloc[:,[2,3,4,5,-3]].dropna()
  post_reply_df['Post 1 By'] = post_reply_df['Post 1 By'].str[:-12]
  post_reply_df['Comment 1 By'] = post_reply_df['Comment 1 By'].str[:-12]
  post_reply_df.to_csv('PostsReplys.csv', index=False, header=False)

  # Populate Assignments data
  asmnt_course1 = df1.iloc[:,[1,11,16,17,18]]
  exam_course1 = df1.iloc[:,[1,11,19,20,21]]
  asmnt_course2 = df1.iloc[:,[1,22,27,28,29]]
  exam_course2 = df1.iloc[:,[1,22,30,31,32]]
  asmnt_course3 = df1.iloc[:,[1,33,38,39,40]]
  exam_course3 = df1.iloc[:,[1,33,41,42,43]]

  asmnt_course1 = asmnt_course1.rename(columns={"Courses 1": "course_name", "Course 1 HW_No": "asmnt_type", "Course 1 HW_Details": "asmnt_detail", "Course 1 HW_Grade": "grade"})
  asmnt_course2 = asmnt_course2.rename(columns={"Courses 2": "course_name", "Course 2 HW_No": "asmnt_type", "Course 2 HW_Details": "asmnt_detail", "Course 2 HW_Grade": "grade"})
  asmnt_course3 = asmnt_course3.rename(columns={"Courses 3": "course_name", "Course 3 HW_No": "asmnt_type", "Course 3 HW_Details": "asmnt_detail", "Course 3 HW_Grade": "grade"})

  exam_course1 = exam_course1.rename(columns={"Courses 1": "course_name", "Course 1 EXAM_No": "asmnt_type", "Course 1 Exam_Details": "asmnt_detail", "Course 1 EXAM_Grade": "grade"})
  exam_course2 = exam_course2.rename(columns={"Courses 2": "course_name", "Course 2 EXAM_No": "asmnt_type", "Course 2 Exam_Details": "asmnt_detail", "Course 2 EXAM_Grade": "grade"})
  exam_course3 = exam_course3.rename(columns={"Courses 3": "course_name", "Course 3 EXAM_No": "asmnt_type", "Course 3 Exam_Details": "asmnt_detail", "Course 3 EXAM_Grade": "grade"})

  HWs = pd.concat([asmnt_course1, asmnt_course2, asmnt_course3])
  EXAMs = pd.concat([exam_course1, exam_course2, exam_course3])
  HWs['asmnt_type'] = 'HW'
  EXAMs['asmnt_type'] = 'Exam'
  assginment_grades_df = pd.concat([HWs, EXAMs])
  assginment_grades_df = assginment_grades_df.dropna()
  assginment_grades_df['grade_id'] = range(1, len(assginment_grades_df)+1)
  assignment_df = assginment_grades_df.iloc[:,[1,2,3,5]]
  assignment_df = assignment_df.drop_duplicates(subset=['course_name','asmnt_type'])
  assignment_df['asmnt_id'] = range(1, len(assignment_df)+1)
  temp = pd.merge(left=assginment_grades_df, right=assignment_df, how='left', left_on=['course_name','asmnt_type','asmnt_detail'], right_on=['course_name','asmnt_type','asmnt_detail'])
  assginment_grades_df = temp.iloc[:,[0,1,2,3,4,5,7]]
  assginment_grades_df = pd.merge(left=assginment_grades_df, right=coursedf.iloc[:,[0,6]], how='left', left_on='course_name', right_on='course')

  file_asnmt_df = assginment_grades_df.iloc[:,[2,3,6,8]].drop_duplicates()
  file_asnmt_grade_df = assginment_grades_df.iloc[:,[0,4,6,8]]
  file_asnmt_grade_df['Email'] = file_asnmt_grade_df['Email'].str[:-12]

  file_asnmt_df.to_csv('Assignments.csv', index=False, header=False)
  file_asnmt_grade_df.to_csv('AssignmentGrades.csv', index=False, header=False)

if __name__ == "__main__":
  print(main())
