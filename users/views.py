from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, UniversityMemberProfileUpdateForm

# Redirect to home page with message after logged out
def logout_request(request):
  logout(request)
  # Show success message
  messages.success(request, "You have logged out successfully!")
  # And send user back to home page
  return redirect("registrar-home")

# Login-required to see profile page
@login_required
def profile(request):

  # When user clicks update button
  if request.method == 'POST':
    user_update_form = UserUpdateForm(request.POST, instance=request.user)
    profile_update_form = UniversityMemberProfileUpdateForm(request.POST, request.FILES, instance=request.user.universitymemberprofile)
    # Only save the change if inputs are valid
    if user_update_form.is_valid() and profile_update_form.is_valid():
      user_update_form.save()
      profile_update_form.save()
      # Show success message
      messages.success(request, "Your profile has been updated!")
      # And send user back to profile page
      return redirect("profile")
  # Show user their current profile info
  else:
    user_update_form = UserUpdateForm(instance=request.user)
    profile_update_form = UniversityMemberProfileUpdateForm(instance=request.user.universitymemberprofile)

  context = {
    'user_update_form': user_update_form,
    'profile_update_form': profile_update_form,
  }

  return render(request, 'users/profile.html', context)