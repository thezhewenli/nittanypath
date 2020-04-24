from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from PIL import Image

from .managers import CustomUserManager
from registrar.models import Department


# Custom user model as 'University Member' table
class UniversityMember(AbstractBaseUser, PermissionsMixin):

    ROLES = (
        ('1', 'Faculty'),
        ('2', 'Student'),
    )

    LEGAL_GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    # Fields needed for Django
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    access_id = models.CharField(
        max_length=6, verbose_name="Access ID", unique=True)
    legal_name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    legal_gender = models.CharField(max_length=1, choices=LEGAL_GENDERS)
    primary_affiliation = models.CharField(max_length=1, choices=ROLES)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    USERNAME_FIELD = 'access_id'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.access_id

    # Auto resize image for user-uploads
    # Code Snippet from CoreyMS, cited in Readme, under MIT license
    def save(self, *args, **kwargs):
        super(UniversityMember, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 100 or img.width > 100:
            output_size = (100, 100)
            img.thumbnail(output_size)
            img.save(self.image.path)

# Table storing zipcode information
class ZipcodeInfo(models.Model):
    zipcode = models.CharField(max_length=5, primary_key=True)
    state = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=50)
    def __str__(self):
        return self.zipcode

# Profiles for each role of University Member
class StudentProfile(models.Model):
    user = models.OneToOneField(UniversityMember, on_delete=models.CASCADE, related_name='student_profile')
    major_id = models.ForeignKey(Department, default='PMAJ', on_delete=models.SET_DEFAULT, verbose_name='Major ID', related_name='stu_major')
    minor_id = models.ForeignKey(Department, null=True, on_delete=models.SET(''), verbose_name='Minor ID', related_name='optional_minor')
    phone = models.CharField(max_length=10)
    home_zipcode = models.ForeignKey(ZipcodeInfo, on_delete=models.DO_NOTHING)
    home_street_address = models.TextField()

class FacultyProfile(models.Model):
    user = models.OneToOneField(UniversityMember, on_delete=models.CASCADE, related_name='faculty_profile')
    department_id = models.ForeignKey(Department, on_delete=models.SET_DEFAULT, default='PMAJ')
    title = models.CharField(max_length=50)
    office = models.CharField(max_length=100)

class TAProfile(models.Model):
    user = models.OneToOneField(UniversityMember, on_delete=models.CASCADE, related_name='TA_profile')
    teaching_team = models.PositiveSmallIntegerField()
    office_hours = models.TextField(blank=True)
    office_location = models.CharField(max_length=50, blank=True)
