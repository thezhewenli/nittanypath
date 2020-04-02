from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class UniversityMemberProfile(models.Model):
  LEGAL_GENDERS = (
      ('M', 'Male'),
      ('F', 'Female'),
  )

  user         = models.OneToOneField(User, on_delete=models.CASCADE)
  legal_name   = models.TextField()
  age          = models.PositiveSmallIntegerField()
  legal_gender = models.CharField(max_length=1, choices=LEGAL_GENDERS)
  home_zipcode = models.CharField(max_length=5)
  home_street_address = models.TextField()
  image        = models.ImageField(default='default.jpg', upload_to='profile_pics')
  
  def __str__(self):
    return f'{self.user.username} University Member Profile'

  # Auto resize image for user-uploads
  # Code Snippet from CoreyMS, cited in Readme, under MIT license
  def save(self, *args, **kwargs):
    super(UniversityMemberProfile, self).save(*args, **kwargs)

    img = Image.open(self.image.path)

    if img.height > 100 or img.width > 100:
      output_size = (100, 100)
      img.thumbnail(output_size)
      img.save(self.image.path)
