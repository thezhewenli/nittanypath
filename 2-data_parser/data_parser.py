import pandas as pd
from os import path

# Color labels for printout messages
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

def main():
  student_ta_path = '../1-dataset/Students_TA.csv'
  prof_path = '../1-dataset/Professors.csv'
  post_comments_path = '../1-dataset/Posts_Comments.csv'
  
  # make sure all three files exist
  if not (path.exists(student_ta_path) and path.exists(prof_path) and path.exists(post_comments_path)):
    print(bcolors.WARNING + "Error. Cannot Find All Three Files!")
    return 1 # return error
  
  df1 = pd.read_csv(student_ta_path, sep=',')
  df2 = pd.read_csv(prof_path, sep=',')
  df3 = pd.read_csv(post_comments_path, sep=',')
  
  # --- 1: Parse Zipcode Data and Save to '1-Zipcodes.csv' ---
  zipdf = df1.iloc[:,[3,6,7]].copy()
  # Return error if FD violation exists
  # Or save processed data to a new csv
  if not checkFDViolation(zipdf, 'Zip', '1-Zipcodes.csv'):
    print(bcolors.WARNING + "Error. FD Violations exist!")
    return 1 # return error
  print(bcolors.OKGREEN + "1/10 Done: Zipcode data parsed and file created.")
  
  # --- 2: Parse Student Info and Save to '2-StudentProfiles.csv' ---
  # Select student profile related columns and normalize email to access id
  studentdf = df1.iloc[:,[0,1,2,3,4,5,8,9,10,44]].copy()
  studentdf['Email'] = studentdf['Email'].str[:6]
  studentdf.to_csv('2-StudentProfiles.csv', index=False, header=False)
  print(bcolors.OKGREEN + "2/10 Done: Student Profile data parsed and file created.")
  
  # --- Parse Course, Section, and Enrollment Info ---
  course1df = df1.iloc[:,[1,11,12,13,14,15]].copy()
  course1df = course1df.rename(columns={
    "Courses 1": "course", 
    "Course 1 Name": "course_name", 
    "Course 1 Details": "course_credit", 
    "Course 1 Section": "section", 
    "Course 1 Section Limit": "limit"})
  course2df = df1.iloc[:,[1,22,23,24,25,26]].copy()
  course2df = course2df.rename(columns={
    "Courses 2": "course", 
    "Course 2 Name": "course_name", 
    "Course 2 Details": "course_credit", 
    "Course 2 Section": "section", 
    "Course 2 Section Limit": "limit"})
  course3df = df1.iloc[:,[1,33,34,35,36,37]].copy()
  course3df = course3df.rename(columns={
    "Courses 3": "course", 
    "Course 3 Name": "course_name", 
    "Course 3 Details": "course_credit", 
    "Course 3 Section": "section", 
    "Course 3 Section Limit": "limit"})
  
  allcourses = pd.concat([course1df, course2df, course3df])
  allcourses['course_credit'] = allcourses['course_credit'].str[:1]
  allcourses['Email'] = allcourses['Email'].str[:6]
  allcourses['subject'] = allcourses['course'].str[:-3]
  allcourses['course_num'] = allcourses['course'].str[-3:]
  allcourses.loc[allcourses['subject']=='CMPSC4','course_num'] = '431W'
  allcourses.loc[allcourses['subject']=='CMPSC4','subject'] = 'CMPSC'

  # --- 3: Get Course Info and Save to '3-Courses.csv' ---
  coursesdf = allcourses.iloc[:,[1,2,3,6,7]].copy().drop_duplicates()
  dropddldf = df3.iloc[:,[0,1]].copy().drop_duplicates()
  courses_and_ddl_df = pd.merge(left=coursesdf, right=dropddldf, how='left', left_on='course', right_on='Courses')
  courses_and_ddl_df.iloc[:,[1,2,3,4,6]].to_csv('3-Courses.csv', index=False, header=False)
  # --- 4: Get Section Info and Save to '4-Sections.csv' ---
  sectionsdf = allcourses.iloc[:,[1,4,5,6,7]].copy()
  course_teachteam_df = df2.iloc[:,-2:]
  section_team_df = pd.merge(left=sectionsdf, right=course_teachteam_df, how='left', left_on='course', right_on='Teaching')
  section_team_df.iloc[:,[1,2,3,4,5]].drop_duplicates().to_csv('4-Sections.csv', index=False, header=False)
  # --- 5: Get Enrollment Records and Save to '5-Enrollments.csv' ---
  enrollmentsdf = allcourses.iloc[:,[0,4,6,7]].copy()
  enrollmentsdf.drop_duplicates().to_csv('5-Enrollments.csv', index=False, header=False)
  print(bcolors.OKGREEN + "3~5/10 Done. Files Created.")
  
  # --- 6: Get Dept Info and Save to '6-Depts.csv' ---
  deptsdf = df2.iloc[:,[5,7]].copy()
  deptsdf.drop_duplicates().to_csv('6-Depts.csv', index=False, header=False)
  print(bcolors.OKGREEN + "6/10 Done. Department File Created.")
  
  # --- 7: Get Faculty Profile Info and Save to '7-FacultyProfiles.csv' ---
  faculty_info_df = df2.iloc[:,[0,1,2,3,4,5,6,8]].copy().drop_duplicates()
  faculty_info_df['Email'] = faculty_info_df['Email'].str[:-12]
  faculty_info_df.drop_duplicates().to_csv('7-FacultyProfiles.csv', index=False, header=False)
  print(bcolors.OKGREEN + "7/10 Done. Faculty Profile File Created.")
  
  # --- 8: Get Faculty and Teaching Team Info and Save to '8-FacultyTeachTeam.csv' ---
  faulty_teachteam_df = df2.iloc[:,[1,-2]].copy()
  faulty_teachteam_df['Email'] = faulty_teachteam_df['Email'].str[:-12]
  faulty_teachteam_df.drop_duplicates().to_csv('8-FacultyTeachTeam.csv', index=False, header=False)
  print(bcolors.OKGREEN + "8/10 Done. Faculty Teach Team File Created.")
  
  # --- 9: Get Post & Reply Data and Save to '9-PostsReplys.csv' ---
  post_reply_df = df3.iloc[:,[0,2,3,4,5]].copy()
  post_reply_df['Post 1 By'] = post_reply_df['Post 1 By'].str[:-12]
  post_reply_df['Comment 1 By'] = post_reply_df['Comment 1 By'].str[:-12]
  post_reply_df['subject'] = post_reply_df['Courses'].str[:-3]
  post_reply_df['course_num'] = post_reply_df['Courses'].str[-3:]
  post_reply_df.loc[post_reply_df['subject']=='CMPSC4','course_num'] = '431W'
  post_reply_df.loc[post_reply_df['subject']=='CMPSC4','subject'] = 'CMPSC'
  post_reply_df.iloc[:,1:8].to_csv('9-PostsReplys.csv', index=False, header=False)
  print(bcolors.OKGREEN + "9/10 Done. Post and Reply File Created.")
  
  # --- Parse Assignments (HW+Exam) and Grades Data ---
  
  # --- 10: Get Assignment and Grades Data and Save to '10-AssignmentsAndGrades.csv' ---
  asmnt_course1 = df1.iloc[:,[1,11,16,17,18]].copy()
  exam_course1 = df1.iloc[:,[1,11,19,20,21]].copy()
  asmnt_course2 = df1.iloc[:,[1,22,27,28,29]].copy()
  exam_course2 = df1.iloc[:,[1,22,30,31,32]].copy()
  asmnt_course3 = df1.iloc[:,[1,33,38,39,40]].copy()
  exam_course3 = df1.iloc[:,[1,33,41,42,43]].copy()

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
  assginment_grades_df['Email'] = assginment_grades_df['Email'].str[:-12]
  assginment_grades_df['subject'] = assginment_grades_df['course_name'].str[:-3]
  assginment_grades_df['course_num'] = assginment_grades_df['course_name'].str[-3:]
  assginment_grades_df.loc[assginment_grades_df['subject']=='CMPSC4','course_num'] = '431W'
  assginment_grades_df.loc[assginment_grades_df['subject']=='CMPSC4','subject'] = 'CMPSC'
  assginment_grades_df.iloc[:,[0,2,3,4,5,6]].to_csv('10-AssignmentsAndGrades.csv', index=False, header=False)
  print(bcolors.OKGREEN + "10/10 Done. Assignemnts and Grades File Created.")
  
if __name__ == "__main__":
  main()