from django.db import models
from django.conf import settings

class Department(models.Model):
  department_id = models.CharField(max_length=5, primary_key=True, default='PMAJ')
  department_name = models.CharField(max_length=50)

class Course(models.Model):
  course_id = models.SmallIntegerField(primary_key=True, unique=True)
  subject = models.ForeignKey(Department, on_delete=models.SET_DEFAULT, default='PMAJ')
  course_number = models.CharField(max_length=4)
  course_name = models.TextField()
  credit = models.PositiveSmallIntegerField()
  drop_ddl = models.CharField(max_length=8)

class Section(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  section_num = models.PositiveSmallIntegerField()
  capacity_limit = models.PositiveSmallIntegerField(default=30)
  teaching_team_id = models.PositiveSmallIntegerField()

class Assignment(models.Model):
  assignment = models.SmallIntegerField(primary_key=True)
  course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
  desc = models.TextField(blank=True, verbose_name='Assignment Description')
  detail = models.TextField(blank=True, verbose_name='Assignment Details')

class AssignmentGrade(models.Model):
  assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
  student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  grade = models.FloatField()

class FacultyTeachTeam(models.Model):
  faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
  teaching_team_id = models.PositiveSmallIntegerField()

class EnrollRecord(models.Model):
  student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  course_section = models.ForeignKey(Section, on_delete=models.CASCADE)
  enroll_time = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
  course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
  post_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
  post_time = models.DateTimeField(auto_now_add=True)
  post_title = models.CharField(max_length=100, default='Untitled')
  post_content = models.TextField()

class Reply(models.Model):
  post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
  reply_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
  reply_time = models.DateTimeField(auto_now_add=True)
  reply_content = models.TextField()
