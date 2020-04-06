from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UniversityMember

# Form for users' self-service to change profile pic
class UniversityMemberProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UniversityMember
        fields = ['image']

# Forms for Django admin page
class UniversityMemberCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UniversityMember
        fields = ('access_id', 'legal_name', 'age', 'legal_gender', 'primary_affiliation', 'image')

class UniversityMemberChangeForm(UserChangeForm):
    class Meta:
        model = UniversityMember
        fields = ('access_id', 'legal_name', 'age', 'legal_gender', 'primary_affiliation', 'image')
