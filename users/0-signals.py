# Code Snippet from CoreyMS, cited in Readme, under MIT license

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UniversityMemberProfile

@receiver(post_save, sender=User)
def create_university_member_profile(sender, instance, created, **kwargs):
  if created:
    UniversityMemberProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
  instance.universitymemberprofile.save()