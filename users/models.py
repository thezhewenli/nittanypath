from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from PIL import Image

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

    access_id = models.CharField(max_length=6, verbose_name="Access ID", unique=True)
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



# home_zipcode = models.CharField(max_length=5)
# home_street_address = models.TextField()


# class InternProfile(models.Model):
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, null=True, related_name='intern_profile')
#     bio = models.CharField(max_length=30, blank=True)
#     location = models.CharField(max_length=30, blank=True)


# class HRProfile(models.Model):
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, null=True, related_name='hr_profile')
#     company_name = models.CharField(max_length=100, blank=True)
#     website = models.CharField(max_length=100, blank=True)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     print('****', created)
#     if instance.is_intern:
#         InternProfile.objects.get_or_create(user=instance)
#     else:
#         HRProfile.objects.get_or_create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     print('_-----')
#     # print(instance.internprofile.bio, instance.internprofile.location)
#     if instance.is_intern:
#         instance.intern_profile.save()
#     else:
#         HRProfile.objects.get_or_create(user=instance)

