from django.db import models
from django.conf import settings
from django.urls import reverse

class Department(models.Model):
  department_id = models.CharField(max_length=5, primary_key=True, default='PMAJ')
  department_name = models.CharField(max_length=50)
  def __str__(self):
    return self.department_id

class FacultyTeachTeam(models.Model):
  teaching_team_id = models.PositiveSmallIntegerField(primary_key=True)
  faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

class Course(models.Model):
  subject = models.ForeignKey(Department, on_delete=models.SET_DEFAULT, default='PMAJ')
  course_number = models.CharField(max_length=4)
  course_name = models.TextField()
  credit = models.PositiveSmallIntegerField()
  drop_ddl = models.DateTimeField()
  class Meta:
    unique_together = ('subject', 'course_number')
  def __str__(self):
    return '%s %s' % (self.subject, self.course_number)

class Section(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  section_num = models.PositiveSmallIntegerField()
  capacity_limit = models.PositiveSmallIntegerField(default=30)
  teaching_team_id = models.ForeignKey(FacultyTeachTeam, blank=True, on_delete=models.SET_DEFAULT, default='')  
  def __str__(self):
    return '%s, Section %s' % (self.course, self.section_num)

class Assignment(models.Model):
  course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
  desc = models.TextField(blank=True, verbose_name='Assignment Description')
  detail = models.TextField(blank=True, verbose_name='Assignment Details')

  def get_absolute_url(self):
    return reverse('view-course-assignment', kwargs={'course_id': self.course_id.id})

class AssignmentGrade(models.Model):
  assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
  student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  grade = models.FloatField()

class EnrollRecord(models.Model):
  student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  course_section = models.ForeignKey(Section, on_delete=models.CASCADE)
  enroll_time = models.DateTimeField(auto_now_add=True)
  GRADES = (
      ('A', 'A'),
      ('A-', 'A-'),
      ('B+', 'B+'),
      ('B', 'B'),
      ('B-', 'B-'),
      ('C+', 'C+'),
      ('C', 'C'),
      ('D', 'D'),
      ('F', 'Failed'),
      ('IP', 'In Progress'),
    )
  grade = models.CharField(max_length=2, choices=GRADES, default='IP')

class Post(models.Model):
  course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
  post_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
  post_time = models.DateTimeField(auto_now_add=True)
  post_title = models.CharField(max_length=100, default='Untitled')
  post_content = models.TextField()

  def __str__(self):
    return self.id

  def get_absolute_url(self):
    return reverse('view-forum-post', kwargs={'pk': self.pk})

class Reply(models.Model):
  post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
  reply_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
  reply_time = models.DateTimeField(auto_now_add=True)
  reply_content = models.TextField()

  def __str__(self):
    return self.id

  def get_absolute_url(self):
    return reverse('view-forum-post', kwargs={'pk': self.post_id.id})

