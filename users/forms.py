from django import forms
from django.contrib.auth.models import User
from .models import UniversityMemberProfile

# Form allowing University Member to change personal info
class UserUpdateForm(forms.ModelForm):
  email = forms.EmailField()

  class Meta:
    model = User
    fields = ['email']

# Form allowing University Member to change profile pictures
class UniversityMemberProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = UniversityMemberProfile
    fields = ['image', 'home_zipcode', 'home_street_address']