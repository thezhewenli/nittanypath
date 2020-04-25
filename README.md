# NittanyPath Project

###### Author: Eric Zhewen Li <br>Contact: eric@zhewenli.com<br>&copy; 2020. Under MIT License. All Rights Reserved.

- [0. Introduction](#0-Introduction)
- [1. Control Flow](#1-Control-Flow)
- [2. Anonymous User](#2-Anonymous-User)
- [3. Logged-in User](#3-Logged-in-User)
- [4. Admin User](#4-Admin-User)
- [5. Copyright Statement](#5-Copyright-Statement)
- [6. Citations](#6-Citations)

## 0. Introduction

NittanyPath is a University and Course Manangement System, created using Django. The system is designed for Nittany State University, as a part of the capstone project for CMPSC 431W course, taught by [Prof. Wang-Chien Lee](https://sites.psu.edu/wlee/) at [Penn State University](https://www.psu.edu/). This report describes the overall control flow and detailed functionalities of the system, categorized by three different types of users - anonymous, logged-in, and admin users.

## 1. Control Flow

![NittanyPath-ControlFlow](/controlflow.png)

### How to Start the System?

NittanyPath is created and powered by Django. Make sure you have Python 3, Django, Django-crisp-form and pillow packages installed. Then go to the directory at terminal and run `python manage.py runserver`. The web app will start at the default location. You can then access the system using your browser.

## 2. Anonymous User

### 2.1. Landing Page

If a user is logged-in (anonymous) and opens NittanyPath home page, the system will redirect the user to the landing page (`/landing`). The landing page shows a picture of Westgate building and prompts user to log-in with a button.

### 2.2. Log-in

If an anonymous user inputs a correct combination of Access ID (in the form of `ab1234`) and password (hashed), NittanyPath will redirect user to home page (section 3.1).

### 2.2. Course Directory

A list of all the courses offered at Nittany State University is shown on this page, including its abbreviation (subject + course number), course name, and credit number. Log-in is not required to access this page. A filter function is also available - when user puts in their desired filter criteria(s) and hit search button, a refined list will be shown on this page.

## 3. Logged-in User

### 3.1. Home Page

Signed-in users will be automatically redirect to the registrar app homepage, showing a picture of the Millennium Science Complex, and a welcome message. The login and logout features are inherited from Django's default functions and views, with some alterations. Three buttons are available on this page - My Enrollments (section 3.2), My Teachings (section 3.3) and Update Profile (section 3.4), each redirecting user to the corresponding page.

### 3.2. My Courses / Enrollment Record

For students, this page shows all the courses they're current enrolled and its grades (default grade is IP for In Progress). In this list, each course will have two buttons to direct students to their forum and assignment pages (section 3.5). If no enrollment record can be found (e.g. for faculty), no table will be shown in this section with a message indicating that.

On the side of each enrollment record, three action buttons are provided - Forum and Assignment (section 3.5), and Drop. The "Drop" button is provided for students to drop their enrollment(s) before the drop deadline. After the deadline for the course (stored in the database), such action will be blocked with an error message returned.

### 3.3. My Teachings

For faculty members and TAs, this page shows all the courses they're currently teaching. In this list, each course will have two buttons to direct students to their forum and assignment pages (section 3.5). There is another "Gradebook" button (section 3.6) redirecting teaching team members to grade each assignment for each enrolled student. The teaching team members also have privileges to create, edit and delete posts in forum, and update grades for assignments. Only faculty teachers can create an assignment.

For students who are TAing any course, when they attempt to access "My Teaching" page, they will be redirected to "My Enrollments" page instead.

### 3.4. My Profile

After logged in, user can also click to view their University Member Profile, including their legal name, university-affiliated email address, gender, age, and primary affiliation. If a user is faculty, their department, office, and title is also shown here. If the user is student, their phone, major, address (with city and state) is shown on this page. In addition, a form to change their profile picture is also shown. User can also change their password by clicking on the button. All passwords are hashed (by Django) and not stored in plain text in the database.

### 3.5. Course Forum & Assignment

Each course will have its own forum, where all participants can view and comment on existing posts, and create new posts. Course forum is restricted to course participants only, i.e. enrolled students (across all sections), teaching faculty and TAs. All other users will be blocked (403 Forbidden) if attempt to access the course forum. Privileged users (authors, teaching team members) can also edit and delete any post of the forum.

Similar to the forum, all course participants can access the Assignment page, where students can see a list of assignments affiliated with the course, and their grades for each assignment if they are graded. And for teaching team members, a grade book (section 3.6) button will be shown for them to update each student's grade for each assignment.

### 3.6. Gradebook



### 3.7. Log-out

This is implemented with help from Django's default logout function. When logged-in user clicks on this button (on the top right corner of the system), NittanyPath will logout the current user and redirect to anonymous user's landing page (section 2.1).

## 4. Admin User

### 4.1. Migrate and Populate Data

A data parser is designed and available at `/2-data_parser/data_parser.py`. This program is designed very specifically to parse the three csv files provided by CMPSC 431W teaching team, i.e. the dataset (default file-readin-location at `/1-dataset/`). The program will create 10 new csv files in the same directory. A list of these generated-files and their column descriptions is shown below:

| Generated File Name         | Target Population Script | Column Descriptions                                          |
| --------------------------- | ------------------------ | ------------------------------------------------------------ |
| 1-Zipcodes.csv              |                          | Zipcode, City, State                                         |
| 2-StudentProfiles.csv       |                          | Name, Access ID, Age, Zipcode, Phone, Gender, Password, Address, Major, Teaching Team ID |
| 3-Courses.csv               |                          | Course Full Name, Credit, Subject / Offered Department, Course Number, Drop Deadline |
| 4-Sections.csv              |                          | Section Number, Seat Capacity, Subject, Course Number        |
| 5-Enrollments.csv           |                          | Student Access ID, Section, Subject, Course Number           |
| 6-Depts.csv                 |                          | Department Abbreviation, Department Name                     |
| 7-FacultyProfiles.csv       |                          | Name, Access ID, Password, Age, Gender, Affiliated Department, Office Location, Title |
| 8-FacultyTeachTeam.csv      |                          | Faculty Access ID, Teaching Team Number                      |
| 9-PostsReplys.csv           |                          | Post Content, Post Author ID, Reply Content, Reply Author ID, Subject, Course Number |
| 10-AssignmentsAndGrades.csv |                          | Student Access ID, Assignment Type, Assignment Detail, Score, Subject, Course Number |

After running the data parser and having new csv files generated, there are 11 scripts under `/3-populate_scripts` directory, and they will automatically populate the database using data from the pre-parsed csv files. There is a preferred order to run these scripts and they are named by numbers. To use the script, simply type the following command to your terminal:

```bash
python manage.py shell < replace_with_script_name.py
```

### 4.2. Manage Data in NittanyPath

The default admin page is at `/admin`, and users with superuser privilege will be able to access the page. It is recommended that when the system is deployed, the path changes to some non-typical address to increase security. For demonstration purposes, a sample admin account is created with username `admin` and password `plasmodiumfalciparum`. Admin page can directly manage all objects associated with models defined in both registrar and user app.

## 5. Copyright Statement

All rights reserved. This project is open-sourced under MIT License. Please include a copy of the license to reuse the codes.

## 6. Citations

I learned a lot of basics about Django using an YouTube playlist[^1], created by Corey Schafer. Some of the code snippets are from his GitHub repo and properly cited. The usage of his codes are licensed under MIT License.

I also gained a lot of knowledge through reading Django's official documentation[^2].

### Cited MIT License

MIT License

Copyright (c) [2018] [Corey Schafer]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[^1]: https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
[^2]: https://docs.djangoproject.com/en/3.0/
