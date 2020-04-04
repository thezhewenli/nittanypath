from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UniversityMember

class UniversityMemberProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UniversityMember
        fields = ['image']
