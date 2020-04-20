from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.conf import settings
from .models import Course, Section

# Default landing page for anonymous user
def landing(request):
  if request.user.is_authenticated:
    return redirect('registrar-home')
  return render(request, 'registrar/landing.html')

def home(request):
  # Show landing page for anonymous user
  if not request.user.is_authenticated:
    return redirect('landing')
  return render(request, 'registrar/home.html')

class CourseSectionListView(ListView):
  model = Course
  template_name = 'registrar/course_list.html'
  context_object_name = 'courses'
  ordering = ['subject']