from django.shortcuts import redirect, render
from django.conf import settings

# Default landing page for anonymous user
def landing(request):
  if request.user.is_authenticated:
    return redirect('registrar-home')
  return render(request, 'registrar/landing.html')

def home(request):
  # Ask anonymous user to log in to view home page
  if not request.user.is_authenticated:
    return redirect('login')
  return render(request, 'registrar/home.html')