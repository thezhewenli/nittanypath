from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.conf import settings
from users.models import FacultyProfile, TAProfile
from .models import *
from users.models import TAProfile
from django.contrib.auth.decorators import login_required
from .filters import CourseFilter, SectionFilter
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from datetime import datetime
import pytz

# identify current user's role in a given course
def testAuthorized(course_id, user):
  # select all affiliated sections
  sections = Section.objects.filter(course=course_id)
  # identify user's role with the course
  facultycount = 0
  TAcount = 0
  ifEnrolled = 0
  for section in sections:
    facultycount += FacultyTeachTeam.objects.filter(teaching_team_id=section.teaching_team_id.teaching_team_id, faculty=user).count()
    TAcount += TAProfile.objects.filter(teaching_team=section.teaching_team_id.teaching_team_id, user=user).count()
    ifEnrolled += EnrollRecord.objects.filter(student=user, course_section=section).count()

  if ifEnrolled > 0:
    return 'student'
  elif TAcount > 0:
    return 'TA'
  elif facultycount > 0:
    return 'faculty'
  # user neither enrolled nor teaching team member, i.e. permission denied
  elif (facultycount+TAcount+ifEnrolled) == 0:
    return 'none'

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

class FilteredListView(ListView):
  filterset_class = None

  def get_queryset(self):
    # Get the queryset however you usually would.  For example:
    queryset = super().get_queryset()
    # Then use the query parameters and the queryset to
    # instantiate a filterset and save it as an attribute
    # on the view instance for later.
    self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
    # Return the filtered queryset
    return self.filterset.qs.distinct()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # Pass the filterset to the template - it provides the form.
    context['filter'] = self.filterset
    return context

class CourseListView(FilteredListView):
  model = Course
  context_object_name = 'courses'
  ordering = ['subject']
  filterset_class = CourseFilter

class CourseDetailView(DetailView):
  model = Course
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super().get_context_data(**kwargs)
    # Query all its affiliated sections and faculty info
    context['sections'] = Section.objects.select_related('teaching_team_id').filter(course=self.object)
    return context

@login_required
def FacultyDetailView(request, access_id):
  user = get_user_model().objects.get(access_id=access_id)
  context = {
    'faculty': user,
    'object': FacultyProfile.objects.get(user=user),
  }
  return render(request, 'registrar/facultyprofile_detail.html', context)

# block unrelated users
@login_required
def course_forum_list(request, course_id):
  if testAuthorized(course_id=course_id, user=request.user) == 'none':
    raise PermissionDenied

  # for authorized visitor
  course = Course.objects.get(id=course_id)
  posts = Post.objects.filter(course_id=course_id)
  context = {
    'posts': posts,
    'course': course,
  }
  return render(request, 'registrar/course_forum.html', context)

# block unrelated users
class PostDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
  model = Post
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super().get_context_data(**kwargs)
    # Query all its affiliated sections and faculty info
    context['reply'] = Reply.objects.filter(post_id=self.object).order_by('reply_time')
    context['role'] = testAuthorized(course_id=self.get_object().course_id, user=self.request.user)
    return context
  def test_func(self):
    post = self.get_object()
    if testAuthorized(course_id=post.course_id, user=self.request.user) == 'none':
      return False
    return True

# block unrelated users
class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Post
  fields = ['post_title', 'post_content']

  def form_valid(self, form):
    course = Course.objects.get(id=self.kwargs['pk'])
    form.instance.course_id = course
    form.instance.post_author = self.request.user
    return super().form_valid(form)

  def test_func(self):
    if testAuthorized(course_id=self.kwargs['pk'], user=self.request.user) == 'none':
      return False
    return True

# Only author and teaching team members can update
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  fields = ['post_title', 'post_content']

  def test_func(self):
    post = self.get_object()
    # allow post author to update
    if self.request.user == post.post_author:
      return True
    else:
      # allow teaching faculty and TA
      role = testAuthorized(course_id=post.course_id, user=self.request.user)
      if role == 'TA' or role == 'faculty':
        return True
      # block unrelated users
      return False

# Only author and teaching team members can delete
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  success_url = reverse_lazy('my-teachings')

  def test_func(self):
    post = self.get_object()
    # allow post author to update
    if self.request.user == post.post_author:
      return True
    # allow teaching faculty and TA
    role = testAuthorized(course_id=post.course_id, user=self.request.user)
    if role == 'TA' or role == 'faculty':
      return True
    # block unrelated users
    return False

# block unrelated users to reply
class ReplyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Reply
  fields = ['reply_content']

  def form_valid(self, form):
    post = Post.objects.get(id=self.kwargs['pk'])
    form.instance.post_id = post
    form.instance.reply_author = self.request.user
    return super().form_valid(form)

  def test_func(self):
    post = Post.objects.get(id=self.kwargs['pk'])
    if testAuthorized(course_id=post.course_id, user=self.request.user) == 'none':
      return False
    return True

@login_required
def my_enrollment(request):
  now = datetime.now()
  context = {
    'enrollments': EnrollRecord.objects.filter(student_id=request.user),
    'now': now,
  }
  return render(request, 'registrar/my_courses.html', context)

@login_required
def my_teachings(request):
  # for student TAs
  if request.user.primary_affiliation == '2':
    # deny entry if not teaching
    try:
      ifTA  = TAProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
      return redirect('my-enrollment')
    # if TA, return which section
    teaching_team = FacultyTeachTeam.objects.get(teaching_team_id=ifTA.teaching_team)
    context = {
      'teachings': Section.objects.filter(teaching_team_id=teaching_team),
    }
  # for faculty
  else:
    context = {
      'teachings': Section.objects.select_related('teaching_team_id').filter(teaching_team_id__in=FacultyTeachTeam.objects.filter(faculty=request.user)),
    }
  return render(request, 'registrar/my_teachings.html', context)

# block unrelated users to view assignment list
@login_required
def course_assignment_list(request, course_id):
  # block unrelated users
  role = testAuthorized(course_id=course_id, user=request.user)
  if role == 'none':
    raise PermissionDenied

  # for authorized visitor
  course = Course.objects.get(id=course_id)
  assignments = Assignment.objects.filter(course_id=course)
  context = {
    'assignments': assignments,
    'course': course,
    'role': role,
  }
  return render(request, 'registrar/course_assignment.html', context)

# Only enrolled students can view assignment detail
# Teaching team members will be prompted to use gradebook
class AssignmentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
  model = Assignment
  def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    context = super().get_context_data(**kwargs)
    # Query all its affiliated sections and faculty info
    context['grade'] = AssignmentGrade.objects.get(assignment=self.object, student=self.request.user)
    role = testAuthorized(course_id=self.get_object().course_id, user=self.request.user)
    # redirect teaching team to gradebook
    context['role'] = role
    return context
  def test_func(self):
    asmnt = self.get_object()
    role = testAuthorized(course_id=asmnt.course_id, user=self.request.user)
    if role == 'none':
      return False
    return True

# Only teaching faculty can delete assignments
class AssignmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Assignment
  success_url = reverse_lazy('my-teachings')

  def test_func(self):
    asmnt = self.get_object()
    if testAuthorized(course_id=asmnt.course_id, user=self.request.user) == 'faculty':
      return True
    return False

# Only teaching faculty can create assignments
class AssignmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Assignment
  fields = ['desc', 'detail']

  def form_valid(self, form):
    course = Course.objects.get(id=self.kwargs['pk'])
    form.instance.course_id = course
    return super().form_valid(form)

  def test_func(self):
    if testAuthorized(course_id=self.kwargs['pk'], user=self.request.user) == 'faculty':
      return True
    return False

# Only teaching faculty can update assignments
class AssignmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Assignment
  fields = ['desc', 'detail']

  def test_func(self):
    assignment = Assignment.objects.get(id=self.kwargs['pk'])
    if testAuthorized(course_id=assignment.course_id, user=self.request.user) == 'faculty':
      return True
    return False

# Only teaching faculty can delete assignments
class EnrollmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = EnrollRecord
  success_url = reverse_lazy('my-enrollment')

  def test_func(self):
    enrollment = self.get_object()
    utc = pytz.utc
    # only self can drop course
    if enrollment.student != self.request.user:
      return False
    # only allow drop before ddl
    elif datetime.now(tz=utc) < enrollment.course_section.course.drop_ddl.astimezone(utc):
      return True
    return False

